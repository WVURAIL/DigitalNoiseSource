"""Hardware-free integrity checks and synthetic time-utility regressions."""
import ast
import importlib.util
import json
from pathlib import Path
import unittest
import warnings

import nbformat
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


class RepositorySanity(unittest.TestCase):
    def test_notebook_schemas(self):
        notebooks = list(ROOT.rglob("*.ipynb"))
        self.assertGreater(len(notebooks), 0)
        for path in notebooks:
            with self.subTest(path=path.relative_to(ROOT)):
                notebook = json.loads(path.read_text())
                self.assertEqual(notebook["nbformat"], 4)
                # Older research notebooks predate cell IDs. Validate in memory only.
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", nbformat.warnings.MissingIDFieldWarning)
                    nbformat.validate(notebook)

    def test_current_python_sources_parse(self):
        paths = list((ROOT / "data_analysis_notebooks").glob("*.py"))
        paths += list((ROOT / "digital_cal_source/rfsoc_radio").rglob("*.py"))
        paths.append(ROOT / "digital_cal_source/setup.py")
        self.assertGreater(len(paths), 0)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                ast.parse(path.read_text(), filename=str(path))


class TimeUtilities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "data_analysis_notebooks/time_utils.py"
        spec = importlib.util.spec_from_file_location("time_utils", path)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_pulse_sampling_and_units(self):
        times, deltas, values = self.module.Pulsed_Data_Waveform(0.01, 4000, 2000)
        np.testing.assert_allclose(times, np.arange(11) / 1000)
        np.testing.assert_allclose([value.total_seconds() for value in deltas], times)
        # Sample away from transitions: 1/5/9 ms on, 3/7 ms off.
        np.testing.assert_array_equal(values[[1, 3, 5, 7, 9]], [1, 0, 1, 0, 1])
        self.assertTrue(set(values).issubset({0.0, 1.0}))

    def test_timestamp_interpolation_for_both_datcon_column_names(self):
        expected = pd.date_range("2024-01-01", periods=100, freq="200ms", tz="UTC")
        for gps, offset in [("gpsUsed", "offsetTime"),
                            ("osd_data:gpsUsed", "Clock:offsetTime")]:
            with self.subTest(gps=gps):
                frame = pd.DataFrame({gps: True, offset: np.arange(100) / 5,
                                      "GPS:dateTimeStamp": expected.strftime("%Y-%m-%dT%H:%M:%SZ")})
                result = self.module.interp_time(frame)
                np.testing.assert_array_equal(result["timestamp"], expected)
                np.testing.assert_array_equal(result["UTC"], expected)


if __name__ == "__main__":
    unittest.main()
