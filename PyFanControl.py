import time
import datetime

from Fan import Fan
from Temp import Temp
from CPU import CPU

from Fan import read_single_line_file
from Fan import overwrite_file

# ### FUNCTIONS ###
#
# # Read single line from file
# def read_single_line_file(f):
#     with open(f, 'r') as file_open:
#         line = file_open.readline()
#         line = line.rstrip()
#
#         return line
#
# # TRUNCATE & Write File
# def overwrite_file(f, message):
#
#     with open(f, 'w') as file_open:
#         file_open.truncate()
#         file_open.write(message)


def get_highest_temp_from_cpu(cpu_list):
    highest = 0
    for i in cpu_list:
        x = int(i.get_current_temp())
        if x > highest:
            highest = x

    return highest


######  DEFINITIONS  ######

coretemp0_parent_dir = "/sys/devices/platform/coretemp.0/hwmon/hwmon1/"
coretemp1_parent_dir = "/sys/devices/platform/coretemp.1/hwmon/hwmon2/"

fan_parent_dir = "/sys/devices/platform/applesmc.768/"

###########################



cpu_a_temps = []
for i in range(2,8):
    if(i==5):
        x = 10
    elif(i==6):
        x = 11
    elif(i== 7):
        x = 12
    else:
        x = i

    cpu_a_temps.append(Temp("cpua_{}".format(x), coretemp0_parent_dir, "temp{}".format(x)))


for i in cpu_a_temps:
    Temp.update_current_temps()
    print(i.name)
    print(i.get_current_temp())

print("Highest: {0}".format(get_highest_temp_from_cpu(cpu_a_temps)))

fan_boosta = Fan("BOOSTA", fan_parent_dir, "fan5")
fan_boostb = Fan("BOOSTB", fan_parent_dir, "fan6")
fan_intake = Fan("INTAKE", fan_parent_dir, "fan4")
fan_exhaust = Fan("EXHAUST", fan_parent_dir, "fan3")
fan_ps = Fan("PS", fan_parent_dir, "fan2")
fan_pci = Fan("PCI", fan_parent_dir, "fan1")

fan_boosta.set_manual(1)
fan_boostb.set_manual(1)

cpu1 = CPU("cpu1", coretemp0_parent_dir, "temp")
cpu2 = CPU("cpu2", coretemp1_parent_dir, "temp")
cpu1.set_max(45)
cpu1.set_min(30)
cpu2.set_max(45)
cpu2.set_min(30)

ps_temp = Temp("Tp0C", fan_parent_dir, "temp72")
pci_temp = Temp("Te1P", fan_parent_dir, "temp57")
southbridge_diode_temp = Temp("TN0D", fan_parent_dir, "temp53")
southbridge_heatsink_temp = Temp("TN0H", fan_parent_dir, "temp54")


while True:

    # This function should be depreciated
    Temp.update_current_temps()


    #print("CPU 1: {0}".format(cpu1.get_temps()))
    #print("CPU 2: {0}".format(cpu2.get_temps()))
    temp_percent = cpu1.get_current_percentage_highest()

    #print("CPU 1 Highest {0}".format(cpu1.get_highest_temp()))
    #print("CPU 2 Highest {0}".format(cpu2.get_highest_temp()))

#    temp_percent = temp_convert_to_percentage(40, 60, highest)

    #print("Percentage " + str(cpu1.get_current_percentage_highest()))
    #fan_boosta.request_set_percentage(cpu1.get_current_percentage_highest())
    #fan_boostb.request_set_percentage(cpu1.get_current_percentage_highest())

    #print("BOOSTA RPM {0}".format(fan_boosta.get_current_rpm()))
    #print("BOOSTB RPM {0}".format(fan_boostb.get_current_rpm()))

    Fan.write_request()

#    print("Fan RPM: {0}".format(realfan1.get_current_rpm()))
#    print("Coretemp 10: {0}".format(realtemp1.get_current_temp()))



    ### Begin Frame Output ###


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
        ,southbridge_diode_temp.get_current_temp()
        ,southbridge_heatsink_temp.get_current_temp()
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
