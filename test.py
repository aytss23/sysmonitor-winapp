import wmi
import time
wmi_api = wmi.WMI()

DEVICE_DATA = []

def cpu_data():
    return wmi_api.Win32_Processor()

def gpu_data():
    return wmi_api.Win32_VideoController()

def mem_data():
    return wmi_api.Win32_PhysicalMemory()

def storage_data():
    return wmi_api.Win32_DiskDrive()

def virt_storage_data():
    return wmi_api.Win32_LogicalDisk()

def os_data():
    return wmi_api.Win32_OperatingSystem()

def netw_data():
    return wmi_api.Win32_NetworkAdapterConfiguration(IPEnabled=True)

def batt_data():
    wmi_root = wmi.WMI(namespace="ROOT\\WMI")
    return wmi_root.Win32_Battery()[0]

def mainb_data():
    return wmi_api.Win32_BaseBoard()

def extract_all():

    hardws = ["CPU", "GPU", "RAM", "DISK", "OS", "NETWORK", "BATTERY", "BASEBOARD"]

    hardw_data = [cpu_data(), gpu_data(), mem_data(),
                  storage_data(),virt_storage_data(), os_data(), netw_data(),
                  batt_data(), mainb_data(),]
    
    with open("systemd.txt","w") as systemd_file:
        for _hardws in hardw_data:
            for _devid, _devdat in enumerate(_hardws):
                systemd_file.writelines(str(_devid))
                systemd_file.writelines(str(_devdat))
            systemd_file.writelines("\n\n")
                    
        systemd_file.close()

def get_cpu_clocks():
    for i in range(0,5,1):
        print(wmi_api.Win32_Processor()[0].CurrentClockSpeed)
        print("\n\n\n\n")
        sleep(1)

extract_all()
          
    
