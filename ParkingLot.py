import numpy as np
from Vehicle import Vehicle
from Vehicle import Orientation

class ParkingLot(object):
    def __init__(self, origin=None, sizeX=6, sizeY=6):
        if origin:
            self.copy_constructor(origin)
        else:
            self.non_copy_constructor(sizeX, sizeY)

    def non_copy_constructor(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.grid = []
        for row in range(self.sizeY):
            self.grid.append([])
            for column in range(self.sizeX):
                self.grid[row].append(None)
        self.previous_state = None
        self.cost = 0

    def copy_constructor(self, origin):
        vehicles = []
        self.sizeX = origin.sizeX
        self.sizeY = origin.sizeY
        self.grid = []
        for row in range(self.sizeY):
            self.grid.append([])
            for column in range(self.sizeX):
                self.grid[row].append(None)
                v = origin.grid[row][column]
                if v and v not in vehicles:
                    vehicles.append(Vehicle(v.name, column, row, v.size, v.orientation, v.fuel))
        
        for vehicle in vehicles:
            self.add_vehicle(vehicle)
        self.previous_state = None
        self.cost = 0

    def __hash__(self):
        return hash(tuple(self.grid))

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

    def remove_vehicle(self, vehicle: Vehicle):
        for offset in range(0, vehicle.size):
            if vehicle.orientation == Orientation.HORIZONTAL:
                self.grid[vehicle.y][vehicle.x + offset] = None
            else:
                self.grid[vehicle.y + offset][vehicle.x] = None

    def get_ambulance_vehicle(self):
        for y in range(0, self.sizeY):
            for x in range(0, self.sizeX):
                vehicle = self.grid[x][y]
                if vehicle and vehicle.name == 'A':
                    return vehicle
        return None
    
    def __str__(self):
        displayGrid = np.ndarray((6,6), dtype=object)
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                vehicle = self.grid[y][x]
                if vehicle:
                    displayGrid[y][x] = self.grid[y][x].get_name()
                else:
                    displayGrid[y][x] = '.'
        return str(displayGrid)

