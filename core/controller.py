from gfx.view import SystemMonitorUI
from core.model import SystemMonitorModel
from PyQt5.QtCore import QThread
from core.thread import SystemMonitorThread, SystemMonitorUIThread

class SystemMonitorController():

    def __init__(self): 
        # model ve view sınıflarından nesne türet. 
        self.sysmonitor_model = SystemMonitorModel()
        self.sysmonitor_ui = SystemMonitorUI()

        self.start_model_thread() # Thread'i başlat.
        
        self.set_signals() # sinyalleri eşle.

        self.set_defaults() # varsayılan ayarları yap.

        # verileri doldur.

        # CPU verilerini al ve arayüzü güncelle.
        self.sysmonitor_ui.update_cpu_data(self.sysmonitor_model.get_cpu_data()) 

        # GPU verilerini al ve arayüzü güncelle.
        #self.sysmonitor_ui.update_gpu_data(self.sysmonitor_model.get_gpu_data(), self.sysmonitor_ui.gpu_s_combo_box.currentData()) 

        # anakart verilerini al ve arayüzü güncelle.
        self.sysmonitor_ui.update_mainboard_data(self.sysmonitor_model.get_mainboard_data())  

        # sistem ve bios verilerini al ve arayüzü güncelle.
        self.sysmonitor_ui.update_system_data(self.sysmonitor_model.get_system_data()) 

        #ağ verilerini al ve arayüzü güncelle.
        self.sysmonitor_ui.update_network_data(self.sysmonitor_model.get_network_data())
        
        # ram bilgilerini al ve arayüzü güncelle.
        #self.sysmonitor_ui.update_memory_data(self.sysmonitor_model.get_memory_data(), self.sysmonitor_ui.ram_slot_s_combo_box.currentData())

        # depolama bilgilerini al ve arayüzü güncelle.
        #self.sysmonitor_ui.update_storage_data(self.sysmonitor_model.get_storage_data(), self.sysmonitor_ui.storage_volume_s_combo_box.currentData())

        #batarya bilgilerini al.
        self.sysmonitor_ui.update_battery_data(self.sysmonitor_model.get_battery_data())

        self.start_ui_thread() # UI thread'ini başlat.

    def start_ui_thread(self):
        self.ui_thread = QThread() # Yeni bir thread oluştur.
        
        self.ui_thread_model = SystemMonitorUIThread() # SystemMonitorUIThread sınıfından bir nesne oluştur
    
        self.ui_thread_model.moveToThread(self.ui_thread) # ui_thread_model nesnesini ui_thread'e taşı.

        self.ui_thread.started.connect(self.ui_thread_model.update_ui) # ui_thread başlatıldığında update_ui metodunu çağır.

        self.ui_thread_model._update_ui_signal.connect(self.sysmonitor_ui.update_floating_texts) # _update_ui_signal sinyalini arayüzün update_inst_data metoduna bağla.
    
        self.ui_thread_model._finished.connect(self.ui_thread_model.stop_thread) # _finished sinyalini stop_thread metoduna bağla.

        self.ui_thread.start() # UI thread'ini başlat.
    def start_model_thread(self): 
        self.data_thread = QThread() # Yeni bir thread oluştur.
        self.data_thread_model = SystemMonitorThread() # SystemMonitorThread sınıfından bir nesne oluştur

        self.data_thread_model.moveToThread(self.data_thread) # thread_model nesnesini thread'e taşı.

        self.data_thread.started.connect(self.data_thread_model.start_updating_curr_data) # thread başlatıldığında thread_model'in start_updating_curr_data metodunu çağır.

        # thread_model'in _inst_data_updated sinyalini get_inst_data metoduna bağla.
        self.data_thread_model._inst_data_updated.connect(self.get_inst_data)
        
        # thread_model'ni _finished sinyalini stop_thread metoduna bağla. 
        self.data_thread_model._finished.connect(self.data_thread_model.stop_thread)

        self.data_thread.start() # thread'i başlat.
    def get_inst_data(self, inst_data):
        self.sysmonitor_ui.update_inst_data(inst_data) # Anlık verileri al ve arayüzü güncelle.
        
    def set_signals(self): 
        self.sysmonitor_ui.gpu_s_combo_box.currentIndexChanged.connect(self.gpu_combo_box_changed)
        self.sysmonitor_ui.ram_slot_s_combo_box.currentIndexChanged.connect(self.ram_combo_box_changed)
        self.sysmonitor_ui.storage_volume_s_combo_box.currentIndexChanged.connect(self.storage_combo_box_changed)

        self.sysmonitor_ui.extract_push_button.clicked.connect(self.sysmonitor_model.extract_all_data)
        self.sysmonitor_ui.refresh_rate_push_button.clicked.connect(self.data_thread_model.set_thread_interval)
    def set_defaults(self):
        try:
            #gpu combobox ayarı yap. 
            for gpu_data in self.sysmonitor_model.get_gpu_data():
                self.sysmonitor_ui.gpu_s_combo_box.addItem(gpu_data[1], gpu_data[0]) #GPU Adı : GPU ID
            #self.sysmonitor_ui.gpu_s_combo_box.setCurrentIndex(0)

            for ram_data in self.sysmonitor_model.get_memory_data():
                self.sysmonitor_ui.ram_slot_s_combo_box.addItem(ram_data[1], ram_data[0]) #RAM Slot : Slot ID
            #self.sysmonitor_ui.ram_slot_s_combo_box.setCurrentIndex(0)

            for vol_data in self.sysmonitor_model.get_storage_data()[1:]:
                self.sysmonitor_ui.storage_volume_s_combo_box.addItem(vol_data[1],vol_data[0])
            #self.sysmonitor_ui.storage_volume_s_combo_box.setCurrentIndex(0)
        except Exception as exc: pass 

    def gpu_combo_box_changed(self): 
        self.sysmonitor_ui.update_gpu_data(self.sysmonitor_model.get_gpu_data(), self.sysmonitor_ui.gpu_s_combo_box.currentData()) # GPU verilerini al ve arayüzü güncelle.
    def ram_combo_box_changed(self):
        self.sysmonitor_ui.update_memory_data(self.sysmonitor_model.get_memory_data(), self.sysmonitor_ui.ram_slot_s_combo_box.currentData())# RAM verilerini al ve arayüzü güncelle.
    def storage_combo_box_changed(self):
        self.sysmonitor_ui.update_storage_data(self.sysmonitor_model.get_storage_data(), self.sysmonitor_ui.storage_volume_s_combo_box.currentData()) # depolama 

    def app_closed(self): 

        self.data_thread_model.stop_thread()
        self.ui_thread_model.stop_thread()
        
        self.ui_thread.quit()
        self.data_thread.quit()
        
        self.sysmonitor_ui.close()

        
