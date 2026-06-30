__author__ = "David Northcote"
__organisation__ = "The Univeristy of Strathclyde"
__support__ = "https://github.com/strath-sdr/rfsoc_radio"

import threading
import asyncio
import ipywidgets as ipw
import time

def default_callback():
    pass
    
class AsyncRadioTx():
    """Class for executing radio data transfer functions for the transmitter.
    """    
    def __init__(self,
                 rate = 1,
                 callback=[default_callback],
                 timer_callback=default_callback):
        """Create new radio transmitter class
        """
        self._timer_callback = timer_callback
        self.callback = callback
        self.is_running = False
        self._stopping = True
        self.rate = rate
        
    def _do(self):
        while not self._stopping:
            next_timer = time.time() + self.rate
            self._timer_callback()
            for i in range(len(self.callback)):
                self.callback[i]()
            sleep_time = next_timer - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            
    def start(self):
        if self._stopping:
            self._stopping = False
            self.is_running = True
            for i in range(len(self.callback)):
                self.callback[i]()
            self._thread = threading.Thread(target=self._do)
            self._thread.start()
            
    def stop(self):
        self._stopping = True
        self.is_running = False
