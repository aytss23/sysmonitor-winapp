from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class SystemMonitorUI(QMainWindow):
    def __init__(self): 
        super(SystemMonitorUI, self).__init__()
        self.load_ui('gfx\\main.ui') # arayüzü içeri aktar.

        self.show() # arayüzü göster. 
        self.add_str = "### UYGULAMA GELISTIRME ASAMASINDADIR. HATALAR OLABILIR. ###"
    def load_ui(self, ui_file): loadUi(ui_file, self)

    def update_floating_texts(self, floated_text_data): self.floating_text_label.setText(floated_text_data)

    # BU GUNCELLEME SEKİLLERİ BOYLE KALAMZ COK CİRKİN DEGİSTİR BUNLARI
    def update_inst_data(self, inst_data): 
        self.cpu_usage_data_label.setText(str(inst_data[0]) + " %") # CPU kullanım yüzdesi
        self.cpu_current_clock_speed_data_label.setText(str(inst_data[1]) + " MHz") # CPU güncel saat hızı
        self.ram_allocated_data_label.setText(str(round(int(inst_data[2] / 1024 / 1024), 2)) + " MB")
        self.ram_free_data_label.setText(str(round(int(inst_data[3] / 1024 / 1024), 2)) + " MB")
        self.ram_usage_data_label.setText(str(inst_data[4]) + " %")
        self.network_upload_data_label.setText(str(round(inst_data[5] / 1024 / 1024,2)) + " MB/s")
        self.network_download_data_label.setText(str(round(inst_data[6] / 1024 / 1024,2)) + " MB/s")
        
    def update_cpu_data(self, cpu_data: tuple): 
        self.cpu_name_data_label.setText(cpu_data[0]) # İşlemci adı
        self.cpu_manufacturer_data_label.setText(cpu_data[1]) # İşlemci üreticisi
        self.cpu_socket_data_label.setText(cpu_data[2]) # İşlemci soket tipi
        self.cpu_cores_data_label.setText(str(cpu_data[3])) # İşlemci çekirdek sayısı
        self.cpu_logical_processor_data_label.setText(str(cpu_data[4])) # İşlemci mantıksal işlemci sayısı
        self.cpu_l2_cache_data_label.setText(str(cpu_data[5]) + " KB") # İşlemci L2 önbellek boyutu
        self.cpu_l3_cache_data_label.setText(str(cpu_data[6]) + " KB") # İşlemci L3 önbellek boyutu
        self.cpu_current_clock_speed_data_label.setText(str(cpu_data[8]) + " MHz") # İşlemci güncel saat hızı
        self.cpu_max_clock_speed_data_label.setText(str(cpu_data[9]) + " MHz") # İşlemci maksimum saat hızı
        
    def update_memory_data(self, memh_data: list, mem_index : int=0):
        self.ram_manufacturer_data_label.setText(str(memh_data[mem_index][2])) # ram modül üretici
        self.ram_capacity_data_label.setText(str(round(int(memh_data[mem_index][3]) / 1024 / 1024 / 1024, 2)) + " GB") # ram kapasitesi
        self.ram_speed_data_label.setText(str(memh_data[mem_index][4])) # ram hız
        self.ram_voltage_data_label.setText(str(memh_data[mem_index][5])) # ram voltaj
        self.ram_total_capacity_data_label.setText(str(round(int(memh_data[-1]) / 1024 / 1024 / 1024, 2)) + " GB") # toplam ram kapasitesi

    def update_gpu_data(self, gpu_data : list, gpu_index: int=0):
        self.gpu_video_processor_data_label.setText(gpu_data[gpu_index][2]) # GPU işlemcisi 
        self.gpu_vram_data_label.setText(str(round(int(gpu_data[gpu_index][3]) / 1024 / 1024, 2)) + " MB") # GPU VRAM boyutu
        self.gpu_status_data_label.setText(gpu_data[gpu_index][4]) # GPU durumu
        self.gpu_max_refrate_data_label.setText(str(gpu_data[gpu_index][5]) + " Hz") # GPU maksimum yenileme hızı
        self.gpu_curr_refrate_data_label.setText(str(gpu_data[gpu_index][6]) + " Hz") # GPU güncel yenileme hızı
        self.gpu_driver_date_data_label.setText(gpu_data[gpu_index][7]) # GPU sürücü tarihi
        self.gpu_driver_version_data_label.setText(gpu_data[gpu_index][8]) # GPU sürücü versiyonu

    def update_storage_data(self, storage_data : list, volume_index : int = 0):
        self.storage_capacity_data_label.setText(str(round(int(storage_data[0][0]) / 1024 / 1024 / 1024, 2)) + " GB")
        self.storage_model_data_label.setText(storage_data[0][1])
        self.storage_manufacturer_data_label.setText(storage_data[0][2])
        self.storage_status_data_label.setText(storage_data[0][3])
        self.storage_volume_name_data_label.setText(str(storage_data[volume_index+1][0]))
        self.storage_allocated_data_label.setText(str(round(int(storage_data[volume_index+1][2]) / 1024 / 1024 / 1024, 2)) + " GB")
        self.storage_free_data_label.setText(str(round(int(storage_data[volume_index+1][3]) / 1024 / 1024 / 1024, 2)) + " GB")
        self.storage_file_system_data_label.setText(str(storage_data[volume_index+1][4]))
        #self.storage_data_label.setText(str(round(100 - storage_data[volume_index+1][5] * 100, 1)) + " %")
            
    def update_network_data(self, netw_data : tuple):
        self.network_adapter_data_label.setText(str(netw_data[0]))
        self.network_ip_address_data_label.setText(str(netw_data[1][0])) # "12.34.567.89"
        self.network_mac_address_data_label.setText(str(netw_data[2])) # "A1:B2:34:5C:67:89"
        
    def update_mainboard_data(self, mainboard_data : tuple):
        self.mainboard_model_data_label.setText(mainboard_data[0]) # anakart model
        self.mainboard_manufacturer_data_label.setText(mainboard_data[1]) # anakart üretici
        self.mainboard_version_data_label.setText(mainboard_data[2]) # anakart versiyon
        self.mainboard_status_data_label.setText(mainboard_data[3]) # anakart durum

    def update_system_data(self, system_data : tuple):
        self.bios_manufacturer_data_label.setText(system_data[0]) #BIOS Üreticisi
        self.bios_version_data_label.setText(system_data[1]) # BIOS Versiyon
        self.os_name_data_label.setText(system_data[2]) # OS ad
        self.os_version_data_label.setText(system_data[3]) # OS versiyon
        self.os_arch_data_label.setText(system_data[4]) # os mimarisi
        self.os_status_data_label.setText(system_data[5]) # os durum
        self.device_name_data_label.setText(system_data[6]) # cihaz adı

    def update_battery_data(self, batt_data : tuple):
        self.battery_model_data_label.setText(str(batt_data[0]))
        self.battery_charge_data_label.setText(str(batt_data[1]))
        self.battery_est_time_data_label.setText(str(batt_data[2]) + " min.")
