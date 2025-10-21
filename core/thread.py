import time
from PyQt5.QtCore import QObject, pyqtSignal
from core.model import SystemMonitorModel

class SystemMonitorThread(QObject, SystemMonitorModel):
    _inst_data_updated = pyqtSignal(tuple)
    _finished = pyqtSignal()
    
    def __init__(self, interval=0.2):
        super().__init__() #Üst sınıfların __init__ metodunu çağır.
        
        self._is_threading = True # Thread çalışıyor mu?
        self._interval = interval # Thread çalışma aralığı (saniye)

        self.last_net_io = self.psutil_api.net_io_counters()
        
    def start_updating_curr_data(self):
        str_index = 20
        str_max_index = 56
        
        while self._is_threading:
            try:
                mem_dat = self.psutil_api.virtual_memory()
                curr_net_io = self.psutil_api.net_io_counters()
                
                upload_speed = (curr_net_io.bytes_sent - self.last_net_io.bytes_sent) / self._interval
                download_speed = (curr_net_io.bytes_recv - self.last_net_io.bytes_recv) / self._interval
                
                self.last_net_io = curr_net_io

                if str_index != str_max_index:
                    str_index += 1
                else: str_index = 0

                self._inst_data_updated.emit((self.psutil_api.cpu_percent(interval=0),
                                              self.psutil_api.cpu_freq().current,
                                              mem_dat.used,
                                              mem_dat.free,
                                              mem_dat.percent,
                                              upload_speed,
                                              download_speed,
                                              str_index))
                
            except Exception as exc: print(exc)
            
            time.sleep(self._interval) # Belirtilen aralıkta bekle.

        self._finished.emit()
        
    def stop_thread(self): self._is_threading = False # Thread'i durdur.
    
