__author__ = "David Northcote"
__organisation__ = "The Univeristy of Strathclyde"
__support__ = "https://github.com/strath-sdr/rfsoc_radio"

from pynq import Overlay
from pynq import allocate
import xrfclk
import xrfdc
import os
import numpy as np
import ipywidgets as ipw
import time
import cffi
from IPython.display import display
from rfsoc4x2 import oled
from datetime import datetime

# Import overlay specific drivers
from .quick_widgets import Button, TransmitTerminal, ReceiveTerminal
from .receiver import Receiver
from .transmitter import Transmitter
from .data_inspector import DataInspector, DataInspectorCore
from .switch import Switch


class RadioOverlay(Overlay):
    
    def __init__(self, bitfile_name=None, init_rf_clks=True, run_test=True, debug_test=False, **kwargs):
        
        GEN3 = ['RFSoC4x2']
        GEN1 = ['RFSoC2x2', 'ZCU111']
        
        # Generate default bitfile name
        if bitfile_name is None:
            this_dir = os.path.dirname(__file__)
            bitfile_name = os.path.join(this_dir, 'bitstream', 'rfsoc_radio.bit')
            
        # Create Overlay
        super().__init__(bitfile_name, **kwargs)
        
        # Determine board and set PLL appropriately
        board = os.environ['BOARD']
        if board in GEN3:
            lmk_clk = 245.76
        elif board in GEN1:
            lmk_clk = 122.88
        else:
            raise RuntimeError('Platform not supported.') # shouldn't get here
        
        # Extract friendly dataconverter names
        self.rf = self.usp_rf_data_converter
        if board == 'RFSoC4x2':
            self.dac_tile = self.rf.dac_tiles[2]
            self.dac_block = self.dac_tile.blocks[0]
            self.adc_tile = self.rf.adc_tiles[2]
            self.adc_block = self.adc_tile.blocks[1]
        elif board == 'RFSoC2x2':
            self.dac_tile = self.rf.dac_tiles[1]
            self.dac_block = self.dac_tile.blocks[0]
            self.adc_tile = self.rf.adc_tiles[2]
            self.adc_block = self.adc_tile.blocks[0]
        elif board == 'ZCU111':
            self.dac_tile = self.rf.dac_tiles[1]
            self.dac_block = self.dac_tile.blocks[2]
            self.adc_tile = self.rf.adc_tiles[0]
            self.adc_block = self.adc_tile.blocks[0]
        else:
            raise RuntimeError('Unknown error occurred.') # shouldn't get here
        
        # Start up LMX clock
        if init_rf_clks:
            xrfclk.set_ref_clks(lmk_clk, 409.6)
            time.sleep(1)
        
        # Set ADC defaults
        self.adc_tile.DynamicPLLConfig(1, 409.6, 1024)
        self.adc_block.NyquistZone = 1
        self.adc_block.MixerSettings = {
            'CoarseMixFreq'  : xrfdc.COARSE_MIX_BYPASS,
            'EventSource'    : xrfdc.EVNT_SRC_TILE,
            'FineMixerScale' : xrfdc.MIXER_SCALE_1P0,
            'Freq'           : -101,
            'MixerMode'      : xrfdc.MIXER_MODE_R2C,
            'MixerType'      : xrfdc.MIXER_TYPE_FINE,
            'PhaseOffset'    : 0.0
        }
        self.adc_block.UpdateEvent(xrfdc.EVENT_MIXER)
        self.adc_tile.SetupFIFO(True)
        
        # Set DAC defaults
        self.dac_tile.DynamicPLLConfig(1, 409.6, 4096)
        self.dac_block.NyquistZone = 1
        self.dac_block.MixerSettings = {
            'CoarseMixFreq'  : xrfdc.COARSE_MIX_BYPASS,
            'EventSource'    : xrfdc.EVNT_SRC_IMMEDIATE,
            'FineMixerScale' : xrfdc.MIXER_SCALE_0P7,
            'Freq'           : 100,
            'MixerMode'      : xrfdc.MIXER_MODE_C2R,
            'MixerType'      : xrfdc.MIXER_TYPE_FINE,
            'PhaseOffset'    : 0.0
        }
        self.dac_block.UpdateEvent(xrfdc.EVENT_MIXER)
        self.dac_tile.SetupFIFO(True)
        
        # The receiver is coupled with an inspector
        self.radio_receiver = Receiver(self.axi_dma_rx, self.receiver, self.DataInspectorRx)
        
        # Receiver setup requirements - pull resets low
        self.radio_receiver.controller.coarse_passthrough = 0
        self.radio_receiver.controller.reset_time_sync = 0
        self.radio_receiver.controller.reset_phase_sync = 0
        self.radio_receiver.controller.reset_frame_sync = 0
        self.radio_receiver.controller.global_reset_sync = 0
        
        # The transmitter is coupled with an inspector
        self.radio_transmitter = Transmitter(self.axi_dma_tx, self.transmitter, self.DataInspectorTx)
        
        # Run synchronisation tests
        if run_test:
            self._synchronisation_test(debug_test)
        else:
            self.radio_receiver.controller.modulation = 1
            self.radio_transmitter.controller.modulation = 1
        self.radio_receiver.monitor.start()
        
        # Complete
        self.radio_transmitter.data('Received data will appear here...\r')
        self.radio_transmitter.start()
        
    def _synchronisation_test(self, debug_test=False):
        
        def run_test(test_data):
            recv_data = []
            for idx in range(8):
                lidx = int(idx*32)
                ridx = int(idx*32+32)
                send_data = test_data[lidx:ridx]
                self.radio_transmitter.data(send_data)
                self.radio_transmitter.start()
                time.sleep(0.5)
                if self.radio_receiver.controller.receive_size > 0:
                    self.radio_receiver._transfer()
                    payload = list(self.radio_receiver.frame['payload'])
                    recv_data.extend(payload)
            return recv_data
        
        # test_data must be length 256 as run_test() sends 8 frames of 32 length
        test_data = np.arange(0, 256)
        
        print('Running BPSK Synchronisation Test...\r')
        for idx in range(3):
            if debug_test == True:
                print(''.join([' BPSK Synchronisation Test ', str(idx + 1), '\r']))
            recv_data = run_test(test_data)
            if not np.array_equal(np.array(recv_data), test_data):
                if debug_test == True:
                    print(''.join([u'\033[91m BPSK Synchronisation Test ', str(idx + 1), ' Failed \u274C \x1b[0m \r']))
                    print(''.join([' Sent Data: ', str(test_data), '\r']))
                    print(''.join([' Received Data: ', str(recv_data), '\r']))
                recv_data = []
                if idx < 2:
                    self.radio_receiver.controller.global_reset_sync = 1
                    time.sleep(0.25)
                    self.radio_receiver.controller.global_reset_sync = 0
                else:
                    print(u'\033[91m BPSK Synchronisation Test Failed \u274C \x1b[0m')
                    print('\033[91m Please check the loopback connection. \x1b[0m \r\n')
            else:
                print(u'\033[92m BPSK Synchronisation Successful! \u2714 \x1b[0m \r\n')
                break
                
        self.radio_receiver.controller.modulation = 1
        self.radio_transmitter.controller.modulation = 1
        
        print('Running QPSK Synchronisation Test...\r')
        for idx in range(3):
            if debug_test == True:
                print(''.join([' QPSK Synchronisation Test ', str(idx + 1), '\r']))
            recv_data = run_test(test_data)
            if not np.array_equal(np.array(recv_data), test_data):
                if debug_test == True:
                    print(''.join([u'\033[91m QPSK Synchronisation Test ', str(idx + 1), ' Failed \u274C \x1b[0m \r']))
                    print(''.join([' Sent Data: ', str(test_data), '\r']))
                    print(''.join([' Received Data: ', str(recv_data), '\r']))
                recv_data = []
                if idx < 2:
                    self.radio_receiver.controller.global_reset_sync = 1
                    time.sleep(1)
                    self.radio_receiver.controller.global_reset_sync = 0
                else:
                    print(u'\033[91m QPSK Synchronisation Test Failed \u274C \x1b[0m \r')
                    print('\033[91m Please check the loopback connection. \x1b[0m \r\n')
            else:
                print(u'\033[92m QPSK Synchronisation Successful! \u2714 \x1b[0m \r\n')
                break
        
    def dashboard(self):
        
        def dashboard_callback(value, button_id = 0):
            if button_id == 0:
                self.radio_transmitter.controller.enable_transmitter = int(value)
            elif button_id == 1:
                self.radio_receiver.controller.coarse_passthrough = int(not value)
            elif button_id == 2:
                self.radio_receiver.controller.reset_time_sync = int(not value)
            elif button_id == 3:
                self.radio_receiver.controller.reset_phase_sync = int(not value)
            elif button_id == 4:
                self.radio_receiver.controller.reset_frame_sync = int(not value)
            else:
                pass
            
        def adc_callback(change):
            self.radio_receiver.controller.global_reset_sync = 1
            self.adc_block.MixerSettings["Freq"] = -change['new']
            self.adc_block.UpdateEvent(xrfdc.EVENT_MIXER)
            self.radio_receiver.controller.global_reset_sync = 0
            time.sleep(0.1)
            freq_label.value = 'Reported Frequency Offset: ' + \
                                str(self.radio_receiver.controller.freq_offset)
            
        def dac_callback(change):
            self.radio_receiver.controller.global_reset_sync = 1
            self.dac_block.MixerSettings["Freq"] = change['new']
            self.dac_block.UpdateEvent(xrfdc.EVENT_MIXER)
            self.radio_receiver.controller.global_reset_sync = 0
            time.sleep(0.1)
            freq_label.value = 'Reported Frequency Offset: ' + \
                                str(self.radio_receiver.controller.freq_offset)
            
        def modulation_callback(change):
            self.radio_receiver.controller.global_reset_sync = 1
            if change['new'] == 'BPSK':
                self.radio_transmitter.controller.modulation = 0
                self.radio_receiver.controller.modulation = 0
            else:
                self.radio_transmitter.controller.modulation = 1
                self.radio_receiver.controller.modulation = 1
            self.radio_receiver.controller.global_reset_sync = 0
            
        def dac_power_callback(change):
            new_pow= int(change['new']) #Dac expects current value in int -- float value will yell at you
            self.dac_block.SetDACVOP(new_pow)
            
        # Read current DAC output to initialize tha power field --
        try:
            currout_ptr=cffi.FFI().new("unsigned int *")
            self.dac_block.GetOutputCurr(currout_ptr)
            currout=currout_ptr[0]
            init_pow=float(currout)
        except Exception:
            init_pow=0.0
        
        # Create button descriptions
        desc_b = ['Transmit Enable', 
                  'Coarse Sync', 
                  'Time Sync', 
                  'Carrier Sync', 
                  'Frame Sync']
        
        buttons = [None]*5
        widgets = [None]*5
        
        # Create buttons
        for i in range(5):
            buttons[i] = Button(description=desc_b[i],
                                state=True,
                                callback=dashboard_callback,
                                button_id=i)
            
        # Create float text objects for entering the ADC & DAC mixer frequencies
        adc_fc = ipw.FloatText(
            value=np.round(-self.adc_block.MixerSettings["Freq"], 3),
            description='ADC Frequency (MHz):',
            style={'description_width': 'initial'},
            disabled=False
        )
        dac_fc = ipw.FloatText(
            value=np.round(self.dac_block.MixerSettings["Freq"], 3),
            description='DAC Frequency (MHz):',
            style={'description_width': 'initial'},
            disabled=False
        )
        adc_fc.observe(adc_callback, names='value')
        dac_fc.observe(dac_callback, names='value')
        
        # Newly adding -- DAC power output control
        dac_pow = ipw.FloatText(
            value=init_pow,
            description='DAC POWER (uA):',
            style={'description_width': 'initial'},
            disabled=False
        )
        
        dac_pow.observe(dac_power_callback, names='value')
        
        # Create dropdown object for modulation selection
        mod_dd = ipw.Dropdown(
            value='QPSK',
            options=['BPSK', 'QPSK'],
            description='Modulation:',
            style={'description_width': 'initial'},
            disabled=False
        )
        mod_dd.observe(modulation_callback, names='value')
        
        layout = ipw.Layout(display='inline-flex',
                justify_content='flex-start',
                align_items='flex-start',
                align_content='flex-start')
        
        freq_label =  ipw.Label('Reported Frequency Offset: ' + \
                                str(self.radio_receiver.controller.freq_offset) + \
                                    ' Hz')
        display(freq_label)

        button_container = ipw.VBox([ipw.HBox([buttons[1].get_widget(), buttons[2].get_widget()]),
                               ipw.HBox([buttons[3].get_widget(), buttons[4].get_widget()])])

        dashboard = ipw.VBox(children=[
                         ipw.HBox(children=[dac_fc,
                                            buttons[0].get_widget()],
                                  layout=layout),
                         ipw.HBox(children=[dac_pow],
                                  layout=layout),
                         ipw.HBox(children=[adc_fc,
                                            button_container], 
                                  layout=layout),
                         ipw.HBox(children=[mod_dd],
                                  layout=layout),
                                  freq_label
                                 ],
                        layout=layout
                       )

        dashboard_accordion = ipw.Accordion(children=[dashboard])
        dashboard_accordion.set_title(0, 'System Control')
        
        return dashboard_accordion

    def _radio_generator(self):
        sidebar = ipw.VBox([self.dashboard(), self.radio_receiver.visualise()])
        msgbar = ipw.VBox([self.radio_transmitter.terminal(), self.radio_receiver.terminal()])
        return ipw.HBox([sidebar, msgbar])

    def radio_application(self):
        return self._radio_generator()
    
    def save_temp_voltages(self, stop_flag):
        
        temp_path="/sys/bus/iio/devices/iio:device0/in_temp2_pl_temp_raw"
        temp_offset_path="/sys/bus/iio/devices/iio:device0/in_temp2_pl_temp_offset"
        temp_scale_path="/sys/bus/iio/devices/iio:device0/in_temp2_pl_temp_scale"
        vccint_path = "/sys/bus/iio/devices/iio:device0/in_voltage0_vcc_pspll0_raw"
        vccint_scale_path="/sys/bus/iio/devices/iio:device0/in_voltage0_vcc_pspll0_scale"
        
        # Create new file with start timestamp
        start_time=datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file=f"/home/xilinx/temp_vcc_log_{start_time}.csv"

        #print(f"Logging to: {log_file}")

        with open(log_file, 'w') as f:
            f.write("timestamp,pl_temp_c,vcc_psplls0_v\n")
            
        while not stop_flag["stop"]:
            try:
                # temperature read
                with open(temp_path, 'r') as f:
                    raw_temp= int(f.read().strip())
                with open(temp_offset_path, 'r') as f:
                    offset= int(f.read().strip())
                with open(temp_scale_path, 'r') as f:
                    scale= float(f.read().strip())

                # converting raw temp values to celsius
                pl_temp_c= (raw_temp+offset) * scale / 1000
                #print(f"PL temperature: {pl_temp_c:.2f} deg Celsius")

                # voltage read
                with open(vccint_path, 'r') as f:
                    vccint_raw= float(f.read().strip())
                with open(vccint_scale_path, 'r') as f:
                    vccint_scale= float(f.read().strip())

                # converting raw voltage values to volts
                vccint_v= vccint_raw*vccint_scale / 1000
                #print(f"VCCINT_PSPLL0: {vccint_v:.3f}V")

                ts= datetime.now().isoformat(timespec="seconds")
                #print(f"{ts} PL temp = {pl_temp_c:.3f} deg Celsius, VCC_PSPLL0 = {vccint_v:.4f}V")

                # appending to new file
                with open(log_file, 'a') as f:
                    f.write(f"{ts},{pl_temp_c:.3f},{vccint_v:.4f}\n")

            except FileNotFoundError:
                print("SYSMON not accessible via sysfs")
            except Exception as e:
                print(f"Error reading sensors: {e}")

            time.sleep(10)    
