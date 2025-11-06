import wmi

wmi_api = wmi.WMI()
storl_data = wmi_api.Win32_LogicalDisk()

print(type(storl_data[0].FreeSpace))