__author__ = "David Northcote"
__organisation__ = "The Univeristy of Strathclyde"
__support__ = "https://github.com/strath-sdr/rfsoc_radio"

## Adapted from the StrathSDR group at the University of Strathclyde
## Modified by Kalyani Bhopi, West Virginia University 
## Support at -- "https://github.com/WVURAIL/Digital_Noise_Source"

from pynq import Overlay
from pynq import allocate
import xrfclk
import xrfdc
import os
import numpy as np
import ipywidgets as ipw
import time
from IPython.display import display
from rfsoc4x2 import oled

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
        dac_fc = ipw.FloatText(
            value=np.round(self.dac_block.MixerSettings["Freq"], 3),
            description='DAC Frequency (MHz):',
            style={'description_width': 'initial'},
            disabled=False
        )
        
        dac_fc.observe(dac_callback, names='value')
        
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