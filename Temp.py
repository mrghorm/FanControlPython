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
        return round(int(read_single_line_file(self.input_file)) / 1000)

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
        line = file_open.readline()
        line = line.rstrip()

        return line

# TRUNCATE & Write File
def overwrite_file(f, message):

    with open(f, 'w') as file_open:
        file_open.truncate()
        file_open.write(message)
