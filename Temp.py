class Temp:

    class_registry = []

    input_suffix = "_input"
    label_suffix = "_label"
    max_suffix = "_max"

    def __init__(self, name, loc, prefix):

        Temp.class_registry.append(self)

        self.temp_current = 0
        self.temp_max = 0

        ### Fan Strings
        self.name = name
        self.file_location = loc
        self.prefix = prefix

        ### Files
        self.input_file = self.file_location + self.prefix + self.input_suffix
        self.label_file = self.file_location + self.prefix + self.label_suffix
        self.max_file = self.file_location + self.prefix + self.max_suffix

        self.file_list = [self.input_file, self.label_file, self.max_file]

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


    # Iterate through all current Fan objects and update current RPM value
    @classmethod
    def update_current_temps(cls):
        for obj in cls.class_registry:
            obj.temp_current = int(read_single_line_file(obj.input_file))

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
