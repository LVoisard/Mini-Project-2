import numpy as np
from Vehicle import Vehicle
from Vehicle import Orientation
from ParkingLot import ParkingLot

class RushHourPuzzleLoader(object):
    @staticmethod
    def load_puzzles(load_from_samples):        
        GRIDSIZE = 6

        puzzlesFile = open("sample-input.txt") if load_from_samples else open("Input Puzzles\\hand-written-puzzles.txt")
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
            for y, row in enumerate(grid):
                for x, letter in enumerate(row):                    
                    if not letter == '.':
                        if any(v.name == letter for v in vehicles):
                            continue
                        elif y+1 < GRIDSIZE and letter == grid[y+1][x]:
                            size = 1
                            while y+size < GRIDSIZE and letter == grid[y+size][x]:
                                size += 1
                            
                            vehicles.append(Vehicle(
                                name = letter, 
                                x=x, 
                                y=y,
                                size=size,
                                orientation=Orientation.VERTICAL,
                                fuel=100,))
                        elif x+1 < GRIDSIZE and letter == grid[y][x+1]:
                            size = 1
                            while x+size < GRIDSIZE and letter == grid[y][x+size]:
                                size += 1

                            vehicles.append(Vehicle(
                                name = letter, 
                                x=x, 
                                y=y,
                                size=size,
                                orientation=Orientation.HORIZONTAL,
                                fuel=100,))


            parkingLot = ParkingLot()
            
            for vehicle in vehicles:
                for vehicleFuelConfig in puzzleConfig[1::]:
                    if(vehicleFuelConfig.startswith(vehicle.name)):
                        vehicle.set_fuel(int(vehicleFuelConfig[1:len(vehicleFuelConfig)]))
                parkingLot.add_vehicle(vehicle)
                if parkingLot.is_vehicle_at_exit(vehicle):
                    parkingLot.remove_vehicle(vehicle)
            
            parkingLots.append(parkingLot)
        
        return parkingLots

    @staticmethod
    def save_puzzles(directory, puzzles):
        file = open(f'{directory}puzzles.txt', 'w')
        for i, puzzle in enumerate(puzzles):
            file.write(f'{str(puzzle)}\n')