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
from .quick_widgets import Button, TransmitTerminal 
#from .receiver import Receiver
from .transmitter import Transmitter
#from .data_inspector import DataInspector, DataInspectorCore
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
            #lmk_clk = 245.76
            lmk_clk = 200 # changed in new zdm mode 
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
        
        # Set DAC defaults
        self.dac_tile.DynamicPLLConfig(1, 409.6, 3686.4)
        self.dac_block.NyquistZone = 1
        self.dac_block.MixerSettings = {
            'CoarseMixFreq'  : xrfdc.COARSE_MIX_BYPASS,
            'EventSource'    : xrfdc.EVNT_SRC_IMMEDIATE,
            'FineMixerScale' : xrfdc.MIXER_SCALE_0P7,
            'Freq'           : 900,
            'MixerMode'      : xrfdc.MIXER_MODE_C2R,
            'MixerType'      : xrfdc.MIXER_TYPE_FINE,
            'PhaseOffset'    : 0.0
        }
        self.dac_block.UpdateEvent(xrfdc.EVENT_MIXER)
        self.dac_tile.SetupFIFO(True)
        
        # The transmitter is coupled with an inspector
        self.radio_transmitter = Transmitter(self.axi_dma_tx, self.transmitter) # self.DataInspectorTx
        
        self.radio_transmitter.start()
        self.radio_transmitter.controller.modulation = 1
        
        
    def dashboard(self):
        
        def dashboard_callback(value, button_id = 0):
            if button_id == 0:
                self.radio_transmitter.controller.enable_transmitter = int(value)
            #elif button_id == 1:
            #    self.radio_receiver.controller.coarse_passthrough = int(not value)
            else:
                pass
            
        def dac_callback(change):
            self.dac_block.MixerSettings["Freq"] = change['new']
            self.dac_block.UpdateEvent(xrfdc.EVENT_MIXER)
            time.sleep(0.1)
        
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
        desc_b = ['Transmit Enable']
        
        buttons = [None]*1
        widgets = [None]*1
        
        # Create buttons
        for i in range(1):
            buttons[i] = Button(description=desc_b[i],
                                state=True,
                                callback=dashboard_callback,
                                button_id=i)
        # DAC frequency control
        dac_fc = ipw.FloatText(
            value=np.round(self.dac_block.MixerSettings["Freq"], 3),
            description='DAC Frequency (MHz):',
            style={'description_width': 'initial'},
            disabled=False
        )
        
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
        #mod_dd = ipw.Dropdown(
        #    value='QPSK',
        #    options=['BPSK', 'QPSK'],
        #    description='Modulation:',
        #    style={'description_width': 'initial'},
        #    disabled=False
        #)
        #mod_dd.observe(modulation_callback, names='value')
        
        layout = ipw.Layout(display='inline-flex',
                justify_content='flex-start',
                align_items='flex-start',
                align_content='flex-start')
        
        freq_label =  ipw.Label('Initial Reported Frequency: ' + \
                                str(np.round(self.dac_block.MixerSettings["Freq"], 3)) + \
                                    ' MHz')
        display(freq_label)


        dashboard = ipw.VBox(children=[
                         ipw.HBox(children=[dac_fc,
                                            dac_pow,
                                            buttons[0].get_widget()],
                                  layout=layout)])

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
        
        #path for processing system (low power domain) temperature sensor register
        pslpd_temp_path="/sys/bus/iio/devices/iio:device0/in_temp0_ps_temp_raw"
        pslpd_temp_offset_path="/sys/bus/iio/devices/iio:device0/in_temp0_ps_temp_offset"
        pslpd_temp_scale_path="/sys/bus/iio/devices/iio:device0/in_temp0_ps_temp_scale"
        #path for processing system (high power domain) temperature sensor register
        pshpd_temp_path="/sys/bus/iio/devices/iio:device0/in_temp1_remote_temp_raw"
        pshpd_temp_offset_path="/sys/bus/iio/devices/iio:device0/in_temp1_remote_temp_offset"
        pshpd_temp_scale_path="/sys/bus/iio/devices/iio:device0/in_temp1_remote_temp_scale"
        #path for PL fabric die temperature sensor register
        pl_temp_path="/sys/bus/iio/devices/iio:device0/in_temp2_pl_temp_raw"
        pl_temp_offset_path="/sys/bus/iio/devices/iio:device0/in_temp2_pl_temp_offset"
        pl_temp_scale_path="/sys/bus/iio/devices/iio:device0/in_temp2_pl_temp_scale"
        #path for PL core supply voltage sensor register
        pl_vccint_path = "/sys/bus/iio/devices/iio:device0/in_voltage2_vccint_raw"
        pl_vccint_scale_path="/sys/bus/iio/devices/iio:device0/in_voltage2_vccint_scale"
        #path for PL aux voltage sensor register 
        pl_vccaux_path = "/sys/bus/iio/devices/iio:device0/in_voltage25_vccplaux_raw"
        pl_vccaux_scale_path="/sys/bus/iio/devices/iio:device0/in_voltage25_vccplaux_scale"
        
        # Create new file with start timestamp
        start_time=datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file=f"/home/xilinx/temp_vcc_log_{start_time}.csv"

        #print(f"Logging to: {log_file}")

        with open(log_file, 'w') as f:
            f.write("timestamp,ps_lpd_temp_c,ps_hpd_temp_c,pl_temp_c,pl_core_voltage_v,pl_aux_voltage_v\n")
            
        while not stop_flag["stop"]:
            try:
                # temperature read
                with open(pslpd_temp_path, 'r') as f:
                    raw_temp1=int(f.read().strip())
                with open(pslpd_temp_offset_path, 'r') as f:
                    offset1= int(f.read().strip())
                with open(pslpd_temp_scale_path, 'r') as f:
                    scale1= float(f.read().strip())

                # converting raw temp values to celsius
                ps_lpd_temp_c= (raw_temp1+offset1) * scale1 / 1000
                #print(f"PS (low power domain) temperature: {ps_lpd_temp_c:.2f} deg Celsius")

                #-------------------------------------------#

                with open(pshpd_temp_path, 'r') as f:
                    raw_temp2= int(f.read().strip())
                with open(pshpd_temp_offset_path, 'r') as f:
                    offset2= int(f.read().strip())
                with open(pshpd_temp_scale_path, 'r') as f:
                    scale2= float(f.read().strip())

                ps_hpd_temp_c= (raw_temp2+offset2) * scale2 / 1000
                #print(f"PS (high power domain) temperature: {ps_hpd_temp_c:.2f} deg Celsius")

                #-------------------------------------------#

                with open(pl_temp_path, 'r') as f:
                    raw_temp3= int(f.read().strip())
                with open(pl_temp_offset_path, 'r') as f:
                    offset3= int(f.read().strip())
                with open(pl_temp_scale_path, 'r') as f:
                    scale3= float(f.read().strip())

                # converting raw temp values to celsius
                pl_temp_c= (raw_temp3+offset3) * scale3 / 1000
                #print(f"PL temperature: {pl_temp_c:.2f} deg Celsius")

                #-------------------------------------------#

                # voltage read
                with open(pl_vccint_path, 'r') as f:
                    pl_vccint_raw= float(f.read().strip())
                with open(pl_vccint_scale_path, 'r') as f:
                    pl_vccint_scale= float(f.read().strip())

                # converting raw voltage values to volts
                pl_vccint_v= pl_vccint_raw*pl_vccint_scale / 1000
                #print(f"PL core voltage: {pl_vccint_v:.3f}V")

                #-----------------------------------------#

                with open(pl_vccaux_path, 'r') as f:
                    pl_vccaux_raw= float(f.read().strip())
                with open(pl_vccaux_scale_path, 'r') as f:
                    pl_vccaux_scale= float(f.read().strip())

                # converting raw voltage values to volts
                pl_vccaux_v= pl_vccaux_raw*pl_vccaux_scale / 1000
                #print(f"PL aux voltage: {pl_vccaux_v:.3f}V")

                ts= datetime.now().isoformat(timespec="seconds")

                # appending to new file
                with open(log_file, 'a') as f:
                    f.write(f"{ts},{ps_lpd_temp_c:.3f}deg C,{ps_hpd_temp_c:.3f}deg C,{pl_temp_c:.3f}deg C,{pl_vccint_v:.4f}V,{pl_vccaux_v:.4f}V\n")
       

            except FileNotFoundError:
                print("SYSMON not accessible via sysfs")
            except Exception as e:
                print(f"Error reading sensors: {e}")

            time.sleep(10)    