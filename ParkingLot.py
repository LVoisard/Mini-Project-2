import numpy as np
from Vehicle import Vehicle
from Vehicle import Orientation

class ParkingLot(object):

    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.grid = np.ndarray((6,6), Vehicle)

    def add_vehicle(self, vehicle: Vehicle):
        for offset in range(0, vehicle.size):
            if vehicle.orientation == Orientation.HORIZONTAL:
                self.grid[vehicle.x + offset][vehicle.y] = vehicle
            else:
                self.grid[vehicle.x][vehicle.y + offset] = vehicle

    def __str__(self):
        displayGrid = np.ndarray((6,6), dtype=object)
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                vehicle = self.grid[x][y]
                if vehicle:
                    displayGrid[x][y] = self.grid[x][y].get_name()
                else:
                    displayGrid[x][y] = '.'
        return str(displayGrid)

