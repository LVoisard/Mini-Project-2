import numpy as np
from Vehicle import Vehicle
from Vehicle import Orientation
from ParkingLot import ParkingLot

class RushHourPuzzleLoader(object):
    @staticmethod
    def load_puzzles():
        
        GRIDSIZE = 6

        puzzlesFile = open("sample-input.txt")
        puzzleConfigurations = []
        parkingLots = []

        for line in puzzlesFile:
            if not line.startswith("#") and not line.startswith('\n'):
                puzzleConfigurations.append(line)

        for puzzle in puzzleConfigurations:
            puzzleConfig = puzzle.split()
            gridConfig = list(puzzleConfig[0])
            grid = np.reshape(gridConfig[:GRIDSIZE**2], (-1, GRIDSIZE))
            vehicles = []
            for y in range(0,GRIDSIZE):
                for x in range(0, GRIDSIZE):
                    if not grid[x][y] == '.':
                        if any(v.name == grid[x][y] for v in vehicles):
                            continue
                        elif x+1 < GRIDSIZE and grid[x][y] == grid[x+1][y]:
                            size = 1
                            while x+size < GRIDSIZE and grid[x][y] == grid[x+size][y]:
                                size += 1

                            vehicles.append(Vehicle(
                                name = grid[x,y], 
                                x=x, 
                                y=y,
                                size=size,
                                orientation=Orientation.HORIZONTAL,
                                fuel=100,
                                infiniteFuel=True))
                        elif y+1 < GRIDSIZE and grid[x][y] == grid[x][y+1]:
                            size = 1
                            while y+size < GRIDSIZE and grid[x][y] == grid[x][y+size]:
                                size += 1

                            vehicles.append(Vehicle(
                                name = grid[x,y], 
                                x=x, 
                                y=y,
                                size=size,
                                orientation=Orientation.VERTICAL,
                                fuel=100,
                                infiniteFuel=True))


            parkingLot = ParkingLot(GRIDSIZE, GRIDSIZE)
            
            for vehicle in vehicles:
                for vehicleFuelConfig in puzzleConfig[1::]:
                    if(vehicleFuelConfig.startswith(vehicle.name)):
                        vehicle.set_fuel(vehicleFuelConfig[1:len(vehicleFuelConfig)], False)
                parkingLot.add_vehicle(vehicle)
            
            parkingLots.append(parkingLot)
        
        return parkingLots