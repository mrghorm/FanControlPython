import time
import datetime

from Fan import Fan
from Temp import Temp
from CPU import CPU

from Fan import read_single_line_file
from Fan import overwrite_file

######  DEFINITIONS  ######

coretemp0_parent_dir = "/sys/devices/platform/coretemp.0/hwmon/hwmon1/"
coretemp1_parent_dir = "/sys/devices/platform/coretemp.1/hwmon/hwmon2/"

fan_parent_dir = "/sys/devices/platform/applesmc.768/"

###########################

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

    # Write requested fan RPM to driver files
    Fan.write_request()

    frame = '''
########## BEGIN FRAME OUTPUT ##########
TIME:  {16}

        TEMPS
CPU 1:
  FULL:  {0}
  HIGH:  {1}
  AVG:   {2}
    
CPU 2:
  FULL:  {3}
  HIGH:  {4}
  AVG:   {5}
    
TN0D:    {6}
TN0H:    {7}
PS:      {8}
PCI:     {9}

        FANS
PS:      {10}
PCI:     {11}
INTAKE:  {12}
EXHAUST: {13}
BOOSTA:  {14}
BOOSTB:  {15}
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
    )

    print(frame)

    time.sleep(1)
