import glob
#from _codecs import lookup
from Temp import Temp

class CPU:
    
    def __init__(self, name, dir, sensor_prefix):
        
        # Set variables
        self.dir = dir
        self.sensor_prefix = sensor_prefix
        
        self.temp_max = 0
        self.temp_min = 0
        
        self.cores = []
        
        # Lookup all files with name similar to "temp*_input"
        lookup_files = "{0}{1}*_input".format(self.dir, self.sensor_prefix)
        glob.glob(lookup_files)
        
        # Iterate through coretemp list
        for file in lookup_files:
            
            # Strip parts of the string to get name and prefix of the sensor
            corename = file.replace(self.dir, '')
            coreprefix = corename.replace("_input", '')
            
            core = Temp("core{0}".format(lookup_files.index(file)), self.dir, coreprefix)
            
            self.cores.append(core)
            
            
    def get_temps(self):
        temps = []
        for core in self.cores:
            temp = (core.get_current_temp() / 1000)
            temps.append(temp)
            
        return temps
    

    def get_highest_temp(self):
        temps = self.get_temps()
        highest = 0
        
        for temp in temps:
            if temp > highest:
                highest = temp
                
        return highest
    
    def get_average_temp(self):
        temps = self.get_temps()
        sum = 0
        count = len(temps)
        
        for temp in temps:
            sum += temp
        
        average = sum / count
        
        return average
    
    def set_max(self, temp):
        self.temp_max = temp
        
    def set_min(self, temp):
        self.temp_min = temp
        
    def get_max(self):
        return self.temp_max
    
    def get_min(self):
        return self.temp_min
    
    def get_current_percentage_highest(self):
        temp_current = self.get_highest_temp()
        temp_min = self.temp_min
        temp_max = self.temp_max
        
        if(temp_current <= temp_min):
            return 0
    
        elif(temp_current >= temp_max):
            return 100
    
        else:
            return (((temp_current - temp_min)*100) / (temp_max - temp_min))
        
        
    def get_current_percentage_average(self):
        temp_current = self.get_average_temp()
        temp_min = self.temp_min
        temp_max = self.temp_max
        
        if(temp_current <= temp_min):
            return 0
    
        elif(temp_current >= temp_max):
            return 100
    
        else:
            return (((temp_current - temp_min)*100) / (temp_max - temp_min))
            
            
    