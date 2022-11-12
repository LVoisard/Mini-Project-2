import numpy as np
from ParkingLot import ParkingLot
from RushHourPuzzleLoader import RushHourPuzzleLoader

parkingLots = RushHourPuzzleLoader.load_puzzles()

for i, parkingLot in enumerate(parkingLots):
    print("\nPuzzle ", i+1)
    print(parkingLot)
    
