import numpy as np
import copy
from Vehicle import Vehicle
from Vehicle import Orientation

class ParkingLot(object):
    def __init__(self, origin=None):
        if origin:
            self.copy_constructor(origin)
        else:
            self.non_copy_constructor()

    def non_copy_constructor(self):
        self.sizeX = 6
        self.sizeY = 6
        self.grid = np.ndarray((6,6), Vehicle)        
        self.previous_state = None
        self.vehicles = []
        self.move = []
        self.cost = 0

    def copy_constructor(self, origin):
        self.sizeX = origin.sizeX
        self.sizeY = origin.sizeY
        self.grid = np.ndarray((6,6), Vehicle)
        self.vehicles = []
        for v in origin.vehicles:
            self.add_vehicle(Vehicle(v.name, v.x, v.y, v.size, v.orientation, v.fuel))
        self.previous_state = None
        self.move = []
        self.cost = 0

    def __eq__(self, other: object):
        if not other:
            return False
        
        for y in range(0, self.sizeY):
            for x in range(0, self.sizeX):
                if not self.grid[y][x] == other.grid[y][x]:
                    return False
        return True

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def add_vehicle(self, vehicle: Vehicle):
        for offset in range(0, vehicle.size):
            if vehicle.orientation == Orientation.HORIZONTAL:
                self.grid[vehicle.y][vehicle.x + offset] = vehicle
            else:
                self.grid[vehicle.y + offset][vehicle.x] = vehicle
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle: Vehicle):
        for offset in range(0, vehicle.size):
            if vehicle.orientation == Orientation.HORIZONTAL:
                self.grid[vehicle.y][vehicle.x + offset] = None
            else:
                self.grid[vehicle.y + offset][vehicle.x] = None
        self.vehicles.remove(vehicle)

    def get_ambulance_vehicle(self):
        for y in range(0, self.sizeY):
            for x in range(0, self.sizeX):
                vehicle = self.grid[x][y]
                if vehicle and vehicle.name == 'A':
                    return vehicle
        return None
    
    def print_board(self):
        displayGrid = np.ndarray((6,6), dtype=object)
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                vehicle = self.grid[y][x]
                if vehicle:
                    displayGrid[y][x] = self.grid[y][x].get_name()
                else:
                    displayGrid[y][x] = '.'
        print(displayGrid)

    def is_vehicle_at_exit(self, vehicle):
        if vehicle.orientation == Orientation.HORIZONTAL:
            if vehicle.x == 6 - vehicle.size and vehicle.y == 2:
                return True
        return False

    def __str__(self):
        return ''.join([element.name if element is not None else '.' for element in self.grid.flatten()])

