import numpy as np
from Vehicle import Vehicle
from Vehicle import Orientation

class ParkingLot(object):

    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.grid = np.ndarray((6,6), Vehicle)
        self.previous_state = None
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

    def remove_vehicle(self, vehicle: Vehicle):
         for offset in range(0, vehicle.size):
            if vehicle.orientation == Orientation.HORIZONTAL:
                self.grid[vehicle.y][vehicle.x + offset] = None
            else:
                self.grid[vehicle.y + offset][vehicle.x] = None

    def get_vehicles(self):
        vehicles = []
        for y in range(0, self.sizeY):
            for x in range(0, self.sizeX):
                vehicle = self.grid[x][y]
                if vehicle:
                    vehicles.append(vehicle)
        return vehicles

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

