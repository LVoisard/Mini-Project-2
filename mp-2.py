import numpy as np
import copy
import sys
import time
import cProfile
from ParkingLot import ParkingLot
from RushHourPuzzleLoader import RushHourPuzzleLoader
import RushHourPuzzleSolver
import Heuristics

puzzles = RushHourPuzzleLoader.load_puzzles()

solvers = [RushHourPuzzleSolver.UCSRushHourSolver(), RushHourPuzzleSolver.GBFSRushHourSolver(), RushHourPuzzleSolver.ASTARRushHourSolver()]
heuristics = [Heuristics.BlockingVehiclesHeuristic(), Heuristics.BlockedPositionsHeuristic(), Heuristics.BlockingVehiclesHeuristic(3), Heuristics.OpenPositionsHeuristic()]
for heuristic in heuristics:
    for s, solver in enumerate(solvers):
        print(heuristic.__class__.__name__)
        for i, parkingLot in enumerate(puzzles):
            print("\nPuzzle ", i + 1)    
            #parkingLot.print_board()
            startTime = time.perf_counter()
            if s == 0:
                solution, number_of_states = solver.solve(parkingLot, heuristic=None)
            else:
                solution, number_of_states = solver.solve(parkingLot, heuristic)
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

                #for i, move in enumerate(move_order):
                #    print(''.join([str(e) for e in move.move]))

                print('Moves: ', len(move_order))
            print('States Explored: ', number_of_states)
            print(f"In {endTime - startTime:0.4f} seconds")
            
