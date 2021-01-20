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


######  DEFINITIONS  ######



###########################


testfan = Fan("testfan", "/home/mrghorm/git/FanControlBash/testfan/", "testfan")

print(read_single_line_file("{0}".format(testfan.label_file)))

#testfan.request_set_percentage(50)
#Fan.write_request()
#testfan.request_set_percentage(75)
#Fan.write_request()
#print(read_single_line_file(testfan.output_file))

#testsensor1 = Temp("testsensor1", "/home/mrghorm/git/FanControlBash/testsensor/", "testsensor")
'''testsensor1 = Temp("testsensor1", "/home/mrghorm/git/FanControlBash/testsensor/", "testsensor")
>>>>>>> e7ff3babab81f6dd94d4519a2f6dcd32e49a5653
testsensor2 = Temp("testsensor2", "/home/mrghorm/git/FanControlBash/testsensor/", "testsensor2")

while True:

    Temp.update_current_temps()
    Fan.update_current_rpms()

    sensortemp = testsensor1.temp_current
    sensor2temp = testsensor2.temp_current
    fanrpm = testfan.get_current_rpm()

    testfan.request_set_rpm(sensortemp * 2)
    testfan.request_set_rpm(sensor2temp * 2)

    Fan.write_request()

    print("{0},{1},{2}".format(testsensor1.temp_current, testsensor2.temp_current, read_single_line_file(testfan.output_file)))

    time.sleep(1)


print("yup this is me trying to fix git")
    
    time.sleep(1)
'''

realfan1 = Fan("realfan1", "/sys/devices/platform/applesmc.768/", "fan1")

realfan1.request_set_rpm(2500)

Fan.write_request()

while True:

    print(realfan1.get_current_rpm())
    time.sleep(1)
    

