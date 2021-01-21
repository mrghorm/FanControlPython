import time

from Fan import Fan
from Temp import Temp

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
        x = i.get_current_temp()
        if x > highest:
            highest = x

    return highest


######  DEFINITIONS  ######

coretemp0_parent_dir = "/sys/devices/platform/coretemp.0/hwmon/hwmon1/"
coretemp1_parent_dir = "/sys/devices/platform/coretemp.1/hwmon/hwmon1/"

fan_parent_dir = "/sys/devices/platform/applesmc.768/"

###########################

def temp_convert_to_percentage(temp_min, temp_max, temp_current):
    if(temp_current <= temp_min):
        return 0

    elif(temp_current >= temp_max):
        return 100

    else:
        return (((temp_current - temp_min)*100) / (temp_max - temp_min))

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


while True:

    Temp.update_current_temps()

    print("{0} {1} {2} {3} {4} {5}".format(cpu_a_temps[0].get_current_temp(), cpu_a_temps[1].get_current_temp(), cpu_a_temps[2].get_current_temp(), cpu_a_temps[3].get_current_temp(), cpu_a_temps[4].get_current_temp(), cpu_a_temps[5].get_current_temp()))
    highest = get_highest_temp_from_cpu(cpu_a_temps)
    print("Highest {0}".format(highest))

    temp_percent = temp_convert_to_percentage(40, 60, highest)

    fan_boosta.request_set_percentage(temp_percent)

    print("RPM {0}".format(fan_boosta.get_current_rpm()))

    Fan.write_request()

#    print("Fan RPM: {0}".format(realfan1.get_current_rpm()))
#    print("Coretemp 10: {0}".format(realtemp1.get_current_temp()))

    time.sleep(1)
    

