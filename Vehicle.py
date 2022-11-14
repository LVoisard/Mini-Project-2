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

    def __init__(self,name, x, y, size, orientation, fuel):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation
        self.fuel = fuel

    def __hash__(self):
        hash(self.name)
    
    def set_fuel(self, fuel):
        self.fuel = fuel

    def __str__(self):
        return 'Name: ' + self.name + str(' Position: ('+str(self.x) + ', ' + str(self.y)+')') + ' Size: ' + str(self.size) +' Orientation: ' + self.orientation.name +' Fuel: ' + str(self.fuel)

    def __eq__(self, other: object):
        if not other:
            return False
        return self.name == other.name

    def move(self, distance, direction):
        if self.orientation == Orientation.HORIZONTAL:
            self.x += distance * direction.value
        else:
            self.y -= distance * direction.value
        self.fuel -= distance
    
    def get_name(self):
        return self.name


