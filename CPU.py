import glob
#from _codecs import lookup
from Temp import Temp

class CPU:
    
    def __init__(self, name, directory, sensor_prefix):
        
        # Set variables
        self.directory = directory
        self.sensor_prefix = sensor_prefix
        
        self.temp_max = 0
        self.temp_min = 0
        
        self.cores = []
        
        # Lookup all files with name similar to "temp*_input"
        lookup_files = "{0}{1}*_input".format(self.directory, self.sensor_prefix)
        files_list = glob.glob(lookup_files)
        
        # Iterate through coretemp list
        for f in files_list:
            
            print("FILE " + f)

            # Strip parts of the string to get name and prefix of the sensor
            corename = f.replace(self.directory, '')
            coreprefix = corename.replace("_input", '')
            
            print("CORENAME " + corename)
            print("COREPREFIX " + coreprefix)

            core = Temp("core{0}".format(files_list.index(f)), self.directory, coreprefix)
            
            self.cores.append(core)
            
            
    def get_temps(self):
        temps = []
        for core in self.cores:
            temp = round(int(core.get_current_temp()) / 1000)
            temps.append(temp)
            
        return temps
    

    def get_highest_temp(self):
        temps = self.get_temps()
        highest = 0
        
        for temp in temps:
            if int(temp) > int(highest):
                highest = temp
                
        return highest
    
    def get_average_temp(self):
        temps = self.get_temps()
        sum = 0
        count = len(temps)
        
        for temp in temps:
            sum += temp
        
        average = sum / count
        
        return round(average)
    
    def set_max(self, temp):
        self.temp_max = temp
        
    def set_min(self, temp):
        self.temp_min = temp
        
    def get_max(self):
        return self.temp_max
    
    def get_min(self):
        return self.temp_min
    
    def get_current_percentage_highest(self):
        temp_current = int(self.get_highest_temp())
        temp_min = int(self.temp_min)
        temp_max = int(self.temp_max)
        
        if(temp_current <= temp_min):
            return 0
    
        elif(temp_current >= temp_max):
            return 100
    
        else:
            return round(((temp_current - temp_min)*100) / (temp_max - temp_min))
        
        
    def get_current_percentage_average(self):
        temp_current = self.get_average_temp()
        temp_min = self.temp_min
        temp_max = self.temp_max
        
        if(temp_current <= temp_min):
            return 0
    
        elif(temp_current >= temp_max):
            return 100
    
        else:
            return round(((temp_current - temp_min)*100) / (temp_max - temp_min))
            
            
    
