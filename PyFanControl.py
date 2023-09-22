import time
import datetime

from Fan import Fan
from Temp import Temp
from CPU import CPU

from Fan import read_single_line_file
from Fan import overwrite_file

######  DEFINITIONS  ######

coretemp0_parent_dir = "/sys/devices/platform/coretemp.0/hwmon/hwmon0/"
coretemp1_parent_dir = "/sys/devices/platform/coretemp.1/hwmon/hwmon1/"

fan_parent_dir = "/sys/devices/platform/applesmc.768/"

logfile = "fanctl_log.txt"

###########################

# Function to write logfile
def write_log(logfile,frame):
    try:
        f = open(logfile, 'a')
        f.write(frame)

    except Exception as e:
        print("Error writing to logfile")
        print(e)
        print("Attempting to continue...")

    finally:
        f.close()

# Initialize Fans
fan_boosta = Fan("BOOSTA", fan_parent_dir, "fan5")
fan_boostb = Fan("BOOSTB", fan_parent_dir, "fan6")
fan_intake = Fan("INTAKE", fan_parent_dir, "fan4")
fan_exhaust = Fan("EXHAUST", fan_parent_dir, "fan3")
fan_ps = Fan("PS", fan_parent_dir, "fan2")
fan_pci = Fan("PCI", fan_parent_dir, "fan1")

# Set fans to manual control
fan_boosta.set_manual(1)
fan_boostb.set_manual(1)
fan_ps.set_manual(1)
fan_pci.set_manual(1)
fan_intake.set_manual(1)
fan_exhaust.set_manual(1)

#### Initialize Sensors ####
# CPU 1
cpu1 = CPU("cpu1", coretemp0_parent_dir, "temp")
cpu1.set_max(80)
cpu1.set_min(50)

# CPU 2
cpu2 = CPU("cpu2", coretemp1_parent_dir, "temp")
cpu2.set_max(80)
cpu2.set_min(50)

# Power Supply
ps_temp = Temp("Tp0C", fan_parent_dir, "temp72")
ps_temp.set_min_temp(30)
ps_temp.set_max_temp(50)

# PCI Bay
pci_temp = Temp("Te1P", fan_parent_dir, "temp57")
pci_temp.set_min_temp(30)
pci_temp.set_max_temp(50)

# Northbridge Diode
northbridge_diode_temp = Temp("TN0D", fan_parent_dir, "temp53")
northbridge_diode_temp.set_min_temp(60)
northbridge_diode_temp.set_max_temp(90)

# Northbridge Heatsink
northbridge_heatsink_temp = Temp("TN0H", fan_parent_dir, "temp54")
northbridge_heatsink_temp.set_min_temp(50)
northbridge_heatsink_temp.set_max_temp(80)



# Main Loop
while True:

    # Read all sensors and fans for inputs before performing logic
    Fan.update_current_rpms()
    Temp.update_all_current_temps()

    # Northbridge Diode Logic
    nbd_p = northbridge_diode_temp.get_current_percentage()
    fan_intake.request_set_percentage(nbd_p)
    fan_exhaust.request_set_percentage(nbd_p)
    fan_boosta.request_set_percentage(nbd_p)
    fan_boostb.request_set_percentage(nbd_p)

    # CPU 1 Logic
    cpu1_tp = cpu1.get_current_percentage_highest()
    fan_intake.request_set_percentage(cpu1_tp)
    fan_exhaust.request_set_percentage(cpu1_tp)
    fan_boosta.request_set_percentage(cpu1_tp)

    # CPU 2 Logic
    cpu2_tp = cpu2.get_current_percentage_highest()
    fan_intake.request_set_percentage(cpu2_tp)
    fan_exhaust.request_set_percentage(cpu2_tp)
    fan_boostb.request_set_percentage(cpu2_tp)

    # PS Logic
    ps_tp = ps_temp.get_current_percentage()
    fan_ps.request_set_percentage(ps_tp)

    # PCI Logic
    pci_tp = pci_temp.get_current_percentage()
    fan_pci.request_set_percentage(pci_tp)

    frame = '''
########## BEGIN FRAME OUTPUT ##########
TIME:  {16}

    TEMPS
CPU 1:
  FULL:  {0} C
  HIGH:  {1} C
  AVG:   {2} C
    
CPU 2:
  FULL:  {3} C
  HIGH:  {4} C
  AVG:   {5} C
    
TN0D:    {6} C
TN0H:    {7} C
PS:      {8} C
PCI:     {9} C

    FANS CURRENT RPM [REQUESTED RPM]
PS:      {10} RPM   [{17}]
PCI:     {11} RPM   [{18}]
INTAKE:  {12} RPM   [{19}]
EXHAUST: {13} RPM   [{20}]
BOOSTA:  {14} RPM   [{21}]
BOOSTB:  {15} RPM   [{22}]
'''.format(
        cpu1.get_temps()
        ,cpu1.get_highest_temp()
        ,cpu1.get_average_temp()
        ,cpu2.get_temps()
        ,cpu2.get_highest_temp()
        ,cpu2.get_average_temp()
        ,northbridge_diode_temp.get_current_temp()
        ,northbridge_heatsink_temp.get_current_temp()
        ,ps_temp.get_current_temp()
        ,pci_temp.get_current_temp()
        ,fan_ps.get_current_rpm()
        ,fan_pci.get_current_rpm()
        ,fan_intake.get_current_rpm()
        ,fan_exhaust.get_current_rpm()
        ,fan_boosta.get_current_rpm()
        ,fan_boostb.get_current_rpm()
        ,str(datetime.datetime.now())
        ,fan_ps.requested_rpm
        ,fan_pci.requested_rpm
        ,fan_intake.requested_rpm
        ,fan_exhaust.requested_rpm
        ,fan_boosta.requested_rpm
        ,fan_boostb.requested_rpm
    )

    print(frame)
    #write_log(logfile, frame)

    # Write requested fan RPM to driver files
    Fan.write_request()

    time.sleep(1)


