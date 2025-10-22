from wmi import WMI

def extract():
    wmi_api = WMI()

    hardw_data = [wmi_api.Win32_Processor(),
                  wmi_api.Win32_VideoController(),
                  wmi_api.Win32_PhysicalMemory(),
                  wmi_api.Win32_DiskDrive(),
                  wmi_api.Win32_LogicalDisk(),
                  wmi_api.Win32_OperatingSystem(),
                  wmi_api.Win32_NetworkAdapterConfiguration(IPEnabled=True),
                  wmi_api.Win32_Battery(),
                  wmi_api.Win32_BaseBoard()]
        
    with open("systemd.txt","w") as systemd_file:
        for _hardws in hardw_data:
            for _devid, _devdat in enumerate(_hardws):
                    
                systemd_file.writelines(str(_devid))
                systemd_file.writelines(str(_devdat))
            systemd_file.writelines("\n\n")
                        
        systemd_file.close()
      
    
