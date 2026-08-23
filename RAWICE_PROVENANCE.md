# `rawice.py` provenance

The vendored file [`data_analysis_notebooks/rawice.py`](data_analysis_notebooks/rawice.py) comes from [`WVURAIL/rawice`](https://github.com/WVURAIL/rawice) at the following immutable revision:

- Commit: [`d6e3c3c0b650c978962921d44e5a54aaf6967583`](https://github.com/WVURAIL/rawice/commit/d6e3c3c0b650c978962921d44e5a54aaf6967583)
- Source path: `rawice.py`
- Upstream Git blob: `bdde3a39b4b85c1604c5cde190ddbf48dda1170b`
- Upstream raw-file SHA-256: `c3db7af5090d88d8c5ed96fc6d53984d3b9132d7d42a7ef7c29f75ebca92af02`
- Vendored Git blob: `74d8a28e160e0c948b1150957d3bcaf8699ff3f2`
- Vendored Git-blob SHA-256: `00e5d1c4d6cd649e95b4cad3cb538cbc7c05c9a573164d891016cd867965e27c`

The two repository objects contain the same 510 logical lines and both use LF line endings. The sole blob-level difference is a final newline added to the vendored copy. After removing that final newline, both hash to `c3db7af5090d88d8c5ed96fc6d53984d3b9132d7d42a7ef7c29f75ebca92af02`. No semantic source difference was found. A local checkout may use different working-tree line endings depending on Git configuration; those checkout bytes are not used for provenance.

## License

The pinned upstream revision predates the license file in `WVURAIL/rawice`.
WVURAIL has since completed the intended MIT license for rawice and records the
same terms for this vendored snapshot in [LICENSE.rawice](LICENSE.rawice). That
path-specific MIT license applies to `data_analysis_notebooks/rawice.py`; the
root BSD-3-Clause license governs this repository's own material where no
separate terms or file-level notices apply.

## Reviewed update policy

Updates are manual and revision-pinned; this repository must not automatically follow an upstream branch.

1. Select and record a full upstream commit SHA.
2. Compare the proposed source against both the pinned upstream file and the current vendored file, ignoring line endings only when explicitly documented.
3. Review every semantic difference and its effect on the PEACC analysis notebooks.
4. Run the relevant analysis checks with representative data.
5. Update this document with the new commit, blob, hashes, and an explanation of accepted differences in the same reviewed change.
