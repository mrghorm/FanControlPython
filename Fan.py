class Fan:

    class_registry = []

    input_suffix = "_input"
    output_suffix = "_output"
    label_suffix = "_label"
    min_suffix = "_min"
    max_suffix = "_max"
    manual_suffix = "_manual"

    def __init__(self, name, loc, prefix):

        Fan.class_registry.append(self)

        # Class Internal Vars
        #### Fan Ints
        self.fan_current_rpm = 0
        self.fan_min_rpm = 0
        self.fan_max_rpm = 0
        self.requested_rpm = -1

        ### Fan Strings
        self.name = name
        self.file_location = loc
        self.prefix = prefix

        ### Files
        self.input_file = self.file_location + self.prefix + self.input_suffix
        self.output_file = self.file_location + self.prefix + self.output_suffix
        self.label_file = self.file_location + self.prefix + self.label_suffix
        self.min_file = self.file_location + self.prefix + self.min_suffix
        self.max_file = self.file_location + self.prefix + self.max_suffix
        self.manual_file = self.file_location + self.prefix + self.manual_suffix

        self.file_list = [self.input_file, self.output_file, self.label_file, self.min_file, self.max_file, self.manual_file]

        # Check all files

        for f in self.file_list:

            try:
                o = open(f)

            except IOError:
                print("Error:  File not accessible")
                print(f)
                o.close()
                exit(1)

            finally:
                o.close()


        # Pull values from files into working variables
        self.fan_current_rpm = int(read_single_line_file(self.input_file))
        self.fan_min_rpm = int(read_single_line_file(self.min_file))
        self.fan_max_rpm = int(read_single_line_file(self.max_file))


    # Request fan set to certain percentage (percentage between min and max)
    def request_set_percentage(self, percent):
        percent_to_rpm = int(((self.fan_max_rpm - self.fan_min_rpm) * percent / 100) + self.fan_min_rpm)

        self.request_set_rpm(percent_to_rpm)


    def request_set_rpm(self, rpm):
        # Only submit request if "asking request" is greater than the current
        # request registered with the fan
        if rpm > self.requested_rpm:
            self.requested_rpm = rpm

    # Returns max RPM of the fan
    def get_max_rpm(self):
        return int(self.fan_max_rpm)

    # Returns min RPM of the fan
    def get_min_rpm(self):
        return int(self.fan_min_rpm)

    # Returns current RPM value in object variable
    def get_current_rpm(self):
        return self.fan_current_rpm

    # Reads current RPM of fan from driver file
    def read_current_rpm(self):

        i = 0

        # Try casting to int, return last known-good value if failed, return new value if success
        try:
            i = int(read_single_line_file(self.input_file))

        # Catch for integer casting error, attempt to continue
        except ValueError as e:
            print("Value Error casting to an integer, file may be empty or may have received an input/output error.")
            print("Error:  {0}\nLocation:  {1}".format(str(e), str(self.input_file)))
            print("Using last known good RPM")

            ##### REMOVE WHEN DONE #####
            input("Press Enter to continue...")

            return self.fan_current_rpm

        # Catch for other errors, attempt to continue, return last known-good value
        except Exception as e:
            print(str(e))
            print("#### Attempting to continue...\n\n")

            ##### REMOVE WHEN DONE #####
            input("Press Enter to continue...")

            return self.fan_current_rpm

        # Else return casted value if try is a success
        else:
            return i



    # Reads current RPM then writes value to current_rpm variable and returns the value
    def update_current_rpm(self):
        c = self.read_current_rpm()
        self.fan_current_rpm = c
        return c

    # Sets the fan[N]_manual file to desired value (should be 1 or 0)
    def set_manual(self, manual):
        overwrite_file(self.manual_file, manual)
        



    # Class method to submit all requested RPMs
    #   Desc:  Any values 0 or greater in the object_Fan "requested_rpm" variable
    #   is considered by this method to be a request to update the fan RPM values.
    #   If the requested_rpm value is above the max in the fan's max file, the
    #   requested RPM value will be set to the maximum value found in the file.
    #   Minimum values will also be brought up to the minimum value.
    #
    #   The request is then updated to the Fan's output file
    @classmethod
    def write_request(cls):
        for obj in cls.class_registry:

            req_rpm = obj.requested_rpm

            # Only write requested RPM to fan if requested RPM is greater than 0
            # IE:  any values of -1 wont be written
            if req_rpm >= 0:

                min_req = obj.get_min_rpm()
                max_req = obj.get_max_rpm()

                # If req_rpm is less than the minimum rpm in the fan's file, then
                # set the req_rpm to that minimum value
                if req_rpm < min_req:
                    req_rpm = min_req

                # If req_rpm is greater than the maximum in the fan's file, then
                # set the req_rpm to that maximum value
                if req_rpm > max_req:
                    req_rpm = max_req

                # Write request to file
                overwrite_file(obj.output_file, str(req_rpm))

            # Set requested_rpm back to a non-request state
            obj.requested_rpm = -1

    # Iterate through all current Fan objects and update current RPM value
    @classmethod
    def update_current_rpms(cls):
        for obj in cls.class_registry:
            obj.update_current_rpm()


### FUNCTIONS ###

# Read single line from file
def read_single_line_file(f):
    with open(f, 'r') as file_open:

        line = ""

        # Try to read the line from the file
        try:
            line = file_open.readline()

        # Catch for OSError Errno 5:
        # Sometimes, the applesmc driver fails to read from the applesmc.  In this case, reading the file results in
        # OSError errno 5.  The file may be accessible after waiting and attempting to read the file again.
        except OSError as e:
            if e.errno == 5:
                print("Error reading {0}:  Input/output error, retry next cycle".format(f))

                ##### REMOVE WHEN DONE #####
                input("Press Enter to continue...")

                return "-1"
            else:
                print("Error reading {0}:  Errno {1}".format(f, e.errno))

                ##### REMOVE WHEN DONE #####
                input("Press Enter to continue...")

                return "-1"

        # General exception catch.  Attempt to continue even if file is not readable.
        except Exception as e:
            print(str(e))
            print("#### Attempting to continue...\n\n")

            ##### REMOVE WHEN DONE #####
            input("Press Enter to continue...")

            return "-1"

        # If try statement runs successfully, continue as normal
        else:

            # Pull newlines & spaces out of output
            line = line.rstrip()
            return line

# TRUNCATE & Write File
def overwrite_file(f, message):

    # open file with write permissions
    with open(f, 'w') as file_open:

        try:
            # Truncate removes the current contents of the file
            file_open.truncate()

            # Write value to file
            file_open.write("{0}".format(message))

        # Catch for OSError Errno 5:
        # Sometimes, the applesmc driver fails to write to the applesmc.  In this case, writing the file results in
        # OSError errno 5.  The file may be accessible after waiting and attempting to writing the file again.
        except OSError as e:
            if e.errno == 5:
                print("Error writing {0}:  Input/output error, retry next cycle".format(f))
                ##### REMOVE WHEN DONE #####
                input("Press Enter to continue...")
            else:
                print("Error reading {0}:  Errno {1}".format(f, e.errno))
                ##### REMOVE WHEN DONE #####
                input("Press Enter to continue...")

        # Catch other exceptions and try to continue
        except Exception as e:
            print(str(e))
            print("Error writing {0}".format(f))
            print("#### Attempting to continue...\n\n")

            ##### REMOVE WHEN DONE #####
            input("Press Enter to continue...")


