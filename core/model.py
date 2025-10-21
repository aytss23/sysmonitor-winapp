import psutil
import wmi 
from gfx.view import SystemMonitorUI
        
class SystemMonitorModel:
    def __init__(self): 
        self.wmi_api = None
        self.psutil_api = None

        self.start_psutil_service()
        self.start_wmi_service()
        
        # okunan tüm veriler geçici burada tutulacak tekrardan sürekli okumamak için.
        self.hardw_data_cache = [] 
        
    def start_psutil_service(self):
        try: self.psutil_api = psutil # psutil kütüphanesini başlat.
        except Exception as e: return False
        
        return self.psutil_api
    
    def start_wmi_service(self):
        try: self.wmi_api = wmi.WMI() #WMI servisine bağlan. 
        except Exception as e: self.wmi_api = False # Bağlanılamadıysa False döner.

        return self.wmi_api

    def check_cpu_type(self): pass 


    def get_inst_data(self, inst_data): return inst_data

    def get_cpu_data(self):
        
        processor_data = self.wmi_api.Win32_Processor()[0]

        if not processor_data: return ()

        processor_data = ( processor_data.Name,
                           processor_data.Manufacturer,
                           processor_data.SocketDesignation,
                           processor_data.NumberOfCores,
                           processor_data.NumberOfLogicalProcessors,
                           processor_data.L2CacheSize,
                           processor_data.L3CacheSize,
                           processor_data.CurrentVoltage,
                           processor_data.CurrentClockSpeed,
                           processor_data.MaxClockSpeed,
                         )
        
        return processor_data
    
    def get_gpu_data(self)-> list: 
        video_controller_data = self.wmi_api.Win32_VideoController()

        if not video_controller_data: return []

        video_controllers_data = []
        for gpu_id, gpu_data in enumerate(video_controller_data, start=0):
            video_controllers_data.append(( gpu_id, 
                                            gpu_data.Name,
                                            gpu_data.VideoProcessor,
                                            gpu_data.AdapterRAM, 
                                            gpu_data.Status,
                                            gpu_data.MaxRefreshRate,
                                            gpu_data.CurrentRefreshRate,
                                            gpu_data.DriverDate,
                                            gpu_data.DriverVersion,
                                                                    ))

        return video_controllers_data

    def get_memory_data(self) -> list:
        memh_data = self.wmi_api.Win32_PhysicalMemory()
        if not memh_data: return []

        physical_memory_data = []
        for ram_id, ram_data in enumerate(memh_data, start=0):
            physical_memory_data.append(( ram_id,
                                          ram_data.Tag,
                                          ram_data.Manufacturer,
                                          ram_data.Capacity,
                                          ram_data.ConfiguredClockSpeed,
                                          ram_data.ConfiguredVoltage))        
        return physical_memory_data    

    def get_storage_data(self):
        try:
            storh_data = self.wmi_api.Win32_DiskDrive()[0]
            storl_data = self.wmi_api.Win32_LogicalDisk()

            storage_data = [ (storh_data.Size,
                             storh_data.Model,
                             storh_data.Manufacturer,
                             storh_data.Status)]

            for volume_id, volume_data in enumerate(storl_data, start=0):
                storage_data.append((volume_id,
                                     volume_data.DeviceID,
                                     int(volume_data.Size) - int(volume_data.FreeSpace),
                                     volume_data.FreeSpace,
                                     volume_data.FileSystem,
                                     int(volume_data.FreeSpace) / int(volume_data.Size) ))
            return storage_data
        except Exception as exc: return 0
        
    def get_network_data(self):
        netwh_data = self.wmi_api.Win32_NetworkAdapterConfiguration(IPEnabled=True)[0]

        return (netwh_data.Description,
                netwh_data.IPAddress,
                netwh_data.MACAddress)
        
    def get_mainboard_data(self):
        # genelde bi anakart olur da fazla olursa sonradan ekleriz.
        mainboard_data = self.wmi_api.Win32_BaseBoard()[0] 

        return (mainboard_data.Manufacturer,
                mainboard_data.Product,
                mainboard_data.Version,
                mainboard_data.Status)
    
    def get_battery_data(self):
        batth_data = self.wmi_api.Win32_Battery()[0]
        #wmi_root = wmi.WMI(namespace="ROOT\\WMI")
        
        return (batth_data.Caption,
                batth_data.EstimatedChargeRemaining,
                batth_data.EstimatedRunTime)
                #wmi_root.BatteryFullChargedCapacity()[0].FullChargedCapacity / wmi_root.BatteryStaticData()[0].DesignCapacity,
                #wmi_root.BatteryCycleCount()[0].CycleCount)
                
        
    def get_system_data(self):
        system_data = self.wmi_api.Win32_BIOS()[0]
        os_data = self.wmi_api.Win32_OperatingSystem()[0]   
        
        return (system_data.Manufacturer,
                system_data.SMBIOSBIOSVersion,
                os_data.Caption,
                os_data.Version,
                os_data.OSArchitecture,
                os_data.Status,
                os_data.CSName
                )
    
