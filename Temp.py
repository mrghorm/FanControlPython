class Temp:

    class_registry = []

    input_suffix = "_input"
    label_suffix = "_label"
    max_suffix = "_max"

    def __init__(self, name, loc, prefix):

        Temp.class_registry.append(self)

        self.temp_current = 0
        self.temp_min = 0
        self.temp_max = 0

        ### Fan Strings
        self.name = name
        self.file_location = loc
        self.prefix = prefix

        ### Files
        self.input_file = self.file_location + self.prefix + self.input_suffix
        self.label_file = self.file_location + self.prefix + self.label_suffix
        #self.max_file = self.file_location + self.prefix + self.max_suffix

        #self.file_list = [self.input_file, self.label_file, self.max_file]
        self.file_list = [self.input_file, self.label_file]

        # Check all files

        for f in self.file_list:

            try:
                o = open(f)

            except IOError:
                print("Error:  File not accessible")
                print(f)
                exit(1)

            finally:
                o.close()

    # Returns current temp stored in sensors temperature variable
    def get_current_temp(self):
        return self.temp_current

    # Returns current temperature found from sensors input file
    def read_current_temp(self):
        #return round(int(read_single_line_file(self.input_file)) / 1000)

        i = 0

        # Try to cast the value to an int, divide by 1000, and round to nearest 1
        try:
            i = round(int(read_single_line_file(self.input_file)) / 1000)

        # Catch for integer casting error, attempt to continue.  Return last good value in this event
        except ValueError as e:
            print("Value Error casting to an integer, file may be empty or may have received an input/output error.")
            print("Error:  {0}\nLocation:  {1}".format(str(e), str(self.input_file)))
            print("Using last known good temperature value")
            return self.temp_current

        # Catch for other errors, attempt to continue, return last known-good value
        except Exception as e:
            print(str(e))
            print("#### Attempting to continue...\n\n")
            return self.temp_current

        # Else return casted value if try is a success
        else:
            return i

    # Read and update current temperature from input file
    def update_current_temp(self):
        c = self.read_current_temp()
        self.temp_current = c
        return c

    def set_max_temp(self, temp):
        self.temp_max = temp

    def set_min_temp(self, temp):
        self.temp_min = temp
        
    
    def get_current_percentage(self):
        temp_current = self.get_current_temp()
        temp_min = self.temp_min
        temp_max = self.temp_max
        
        if(temp_current <= temp_min):
            return 0
    
        elif(temp_current >= temp_max):
            return 100
    
        else:
            return round(((temp_current - temp_min)*100) / (temp_max - temp_min))
        

    # Iterate through all current Fan objects and update current RPM value
    @classmethod
    def update_all_current_temps(cls):
        for obj in cls.class_registry:
            obj.update_current_temp()

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
                return "-1"
            else:
                print("Error reading {0}:  Errno {1}".format(f, e.errno))
                return "-1"

        # General exception catch.  Attempt to continue even if file is not readable.
        except Exception as e:
            print(str(e))
            print("Error reading {0}".format(f))
            print("#### Attempting to continue...\n\n")
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
            else:
                print("Error reading {0}:  Errno {1}".format(f, e.errno))

        # Catch other exceptions and try to continue
        except Exception as e:
            print(str(e))
            print("Error writing {0}".format(f))
            print("#### Attempting to continue...\n\n")
