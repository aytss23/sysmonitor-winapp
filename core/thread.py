import time
from PyQt5.QtCore import QObject, pyqtSignal
from core.model import SystemMonitorModel

class SystemMonitorThread(QObject, SystemMonitorModel):
    _inst_data_updated = pyqtSignal(tuple)
    _finished = pyqtSignal()
    
    def __init__(self, interval=1.0):
        super().__init__() #Üst sınıfların __init__ metodunu çağır.
        
        self._is_threading = True # Thread çalışıyor mu?
        self._thread_interval = interval # Thread çalışma aralığı (saniye)

        self.last_net_io = self.psutil_api.net_io_counters()
    
    def set_thread_interval(self):
        if self._thread_interval == 0.25: self._thread_interval = 1

        else: self._thread_interval -= 0.25    
    
    def start_updating_curr_data(self):
        while self._is_threading:
            try:
                mem_dat = self.psutil_api.virtual_memory()
                curr_net_io = self.psutil_api.net_io_counters()
                
                upload_speed = (curr_net_io.bytes_sent - self.last_net_io.bytes_sent) / self._thread_interval
                download_speed = (curr_net_io.bytes_recv - self.last_net_io.bytes_recv) / self._thread_interval
                
                self.last_net_io = curr_net_io

                self._inst_data_updated.emit((self.psutil_api.cpu_percent(interval=0),
                                              self.psutil_api.cpu_freq().current,
                                              mem_dat.used,
                                              mem_dat.free,
                                              mem_dat.percent,
                                              upload_speed,
                                              download_speed))
                
            except Exception as exc: print(exc)
            
            time.sleep(self._thread_interval) # Belirtilen aralıkta bekle.

        self._finished.emit()
        
    def stop_thread(self): self._is_threading = False # Thread'i durdur.
    
class SystemMonitorUIThread(QObject):
    _update_ui_signal = pyqtSignal(str)
    _finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._is_threading = True
        self._thread_interval = 0.1 # Hız
        
        self.cache_index = 0
        self.start_index = 0
        self.window_size = 30 # Kayan pencerenin genişliği 

        self.float_texts = [
            "Sisteminizi izliyoruz...",
            "Donanım bilgilerinizi topluyoruz...",
            "Performans verilerinizi analiz ediyoruz...",
            "Sistem kaynaklarınızı izliyoruz...",
            "Anlık verilerinizi güncelliyoruz...",
            "Sistem sağlığınızı kontrol ediyoruz...",
            "Performans optimizasyonu yapıyoruz...",
            "Sistem kararlılığınızı sağlıyoruz...",
            "Donanım bileşenlerinizi tanıyoruz...",
            "Sistem performansınızı artırıyoruz..."
        ]

    def update_ui(self):
        """
        Kayan yazı (marquee) efektini işleyen ana thread döngüsü.
        """
        while self._is_threading:
            # 1. Gösterilecek geçerli metni al
            if self.cache_index >= len(self.float_texts):
                self.cache_index = 0  # Liste bittiyse başa dön
            
            base_text = self.float_texts[self.cache_index]

            # 2. Akıcı "marquee" efekti için metni bir ayırıcı ile birleştir
            # Örn: "Metin...   Metin...   "
            scroll_text = base_text + "   " 
            display_text = scroll_text + scroll_text 

            # 3. Metnin sonuna gelip gelmediğimizi kontrol et
            # (scroll_text'in sonuna geldiysek başa sar)
            if self.start_index >= len(scroll_text):
                self.start_index = 0
                self.cache_index += 1 # Bir sonraki metne geç
                continue # Döngüye yeniden başla (yeni metni almak için)

            # 4. Gösterilecek dilimi hesapla ve gönder
            stop_index = self.start_index + self.window_size
            current_slice = display_text[self.start_index:stop_index]
            
            self._update_ui_signal.emit(current_slice)
            
            #print(self.start_index, stop_index, current_slice) # Hata ayıklama için
            
            # 5. Bir sonraki kare için pencereyi kaydır
            self.start_index += 1
            
            # 6. Bekle
            time.sleep(self._thread_interval)
            
        self._finished.emit()
    
    def stop_thread(self):
        """Thread'in ana döngüsünü güvenle durdurur."""
        self._is_threading = False