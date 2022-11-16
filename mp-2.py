import numpy as np
import copy
import sys
import time
import cProfile
from ParkingLot import ParkingLot
from RushHourPuzzleLoader import RushHourPuzzleLoader
from RushHourPuzzleSolver import RushHourPuzzleSolver                

puzzles = RushHourPuzzleLoader.load_puzzles()

for i, parkingLot in enumerate(puzzles):
    print("\nPuzzle ", i + 1)
    parkingLot.print_board()
    solver = RushHourPuzzleSolver()
    startTime = time.perf_counter()
    solution, number_of_states = solver.solve(parkingLot)
    endTime = time.perf_counter()
    if not solution:
        print('no solution found')
        print(parkingLot)
    else:
        move_order = [solution]
        while solution.previous_state and solution.previous_state.previous_state:
            move_order.append(solution.previous_state)
            solution = solution.previous_state
        
        move_order.reverse()

        for i, move in enumerate(move_order):
            print(''.join([str(e) for e in move.move]))

        print('Moves: ', len(move_order))
    print('States Explored: ', number_of_states)
    print(f"In {endTime - startTime:0.4f} seconds")
    
