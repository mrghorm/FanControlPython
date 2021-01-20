class Area:

    class_registry = []

    def __init__(self):

        sensors = []
        fans = []


    @classmethod
    def read_sensors(cls):
        for obj in class_registry:
            for item in obj.sensors:
                item.temp_current
