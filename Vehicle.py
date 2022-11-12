from enum import Enum
class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

class Vehicle(object):
    name: str
    x: int
    y: int
    size: int
    orientation: Orientation
    fuel: int
    infiniteFuel: bool

    def __init__(self,name, x, y, size, orientation, fuel, infiniteFuel):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation
        self.fuel = fuel
        self.infiniteFuel = infiniteFuel
    
    def set_fuel(self, fuel, infiniteFuel):
        self.fuel = fuel
        self.infiniteFuel = infiniteFuel

    def __str__(self):
        return 'Name: ' + self.name + str(' Position: ('+str(self.x) + ', ' + str(self.y)+')') + ' Size: ' + str(self.size) +' Orientation: ' + self.orientation.name +' Fuel: ' + (str(self.fuel) if not self.infiniteFuel else 'Infinite')

    def slide(self, distance, direction):
        return
    
    def get_name(self):
        return self.name


