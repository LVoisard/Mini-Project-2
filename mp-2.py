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
    with cProfile.Profile() as pr:
        print("\nPuzzle ", i + 1)
        print(parkingLot)
        solver = RushHourPuzzleSolver()
        
        startTime = time.perf_counter()
        solution, number_of_states = solver.solve(parkingLot)
        endTime = time.perf_counter()
    
    pr.print_stats('cumulative')
    if not solution:
        print('no solution found')
        continue

    move_order = [solution]
    while solution.previous_state and solution.previous_state.previous_state:
        move_order.append(solution.previous_state)
        solution = solution.previous_state
    
    move_order.reverse()

    for i, move in enumerate(move_order):
        print('\n move ', i + 1, '\n', move)

    print('Moves: ', len(move_order))
    print('States Explored: ', number_of_states)
    print(f"Solved in {endTime - startTime:0.4f} seconds")
    
