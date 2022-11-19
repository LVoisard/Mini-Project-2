import numpy as np
import copy
import sys
import time
import cProfile
import os
from ParkingLot import ParkingLot
from RushHourPuzzleLoader import RushHourPuzzleLoader
import RushHourPuzzleSolver
import Heuristics

puzzles = RushHourPuzzleLoader.load_puzzles()

solvers = [
    # UCS
    RushHourPuzzleSolver.UCSRushHourSolver(),
    # GBFS
    RushHourPuzzleSolver.GBFSRushHourSolver(Heuristics.BlockingVehiclesHeuristic()), 
    RushHourPuzzleSolver.GBFSRushHourSolver(Heuristics.BlockedPositionsHeuristic()),
    RushHourPuzzleSolver.GBFSRushHourSolver(Heuristics.BlockingVehiclesHeuristic(3)),
    RushHourPuzzleSolver.GBFSRushHourSolver(Heuristics.OpenPositionsHeuristic()),
    #A STAR
    RushHourPuzzleSolver.ASTARRushHourSolver(Heuristics.BlockingVehiclesHeuristic()),
    RushHourPuzzleSolver.ASTARRushHourSolver(Heuristics.BlockedPositionsHeuristic()),
    RushHourPuzzleSolver.ASTARRushHourSolver(Heuristics.BlockingVehiclesHeuristic(3)),
    RushHourPuzzleSolver.ASTARRushHourSolver(Heuristics.OpenPositionsHeuristic())]
    
def write_solution_to_file(file_name, initial_puzzle, move_order, search_states, runtime):
    directory = 'Output'
    if not os.path.exists(directory):
        os.mkdir(directory)
    file = open(file_name, 'w')


    additional_info = ''    
    car_fuel_available = []
    for vehicle in initial_puzzle.vehicles:
        if vehicle.fuel != 100:
            additional_info += vehicle.name + str(vehicle.fuel) + ' '
        car_fuel_available.append(vehicle.name +':'+ str(vehicle.fuel))

    file.write('--------------------------------------------------------------------------------\n')
    file.write('\n')
    file.write('Initial board configuration: {board} {additional_info}\n'.format(board=initial_puzzle,additional_info=additional_info))
    file.write('\n')
    if additional_info != '':
        file.write('! ' + additional_info + '\n')    
    file.write(parkingLot.get_board_display())
    file.write('\n')
    file.write('Car fuel available: ')
    file.write(' , '.join(car_fuel_available))
    file.write('\n')
    file.write('\n')

    if not move_order:
        file.write('Sorry, could not solve the puzzle as specified.\n')
        file.write('Error: no solution found\n')
    
    file.write(f'Runtime: {runtime:0.5f}\n')

    if move_order:
        file.write(f'Solution path: {"; ".join([f"{state.move[0].name} {state.move[1]} {state.move[2]}" for state in move_order])} \n')
        file.write(f'Search path length: {str(len(search_states))} \n')
        file.write(f'Solution path length: {str(len(move_order))} \n')

        file.write('\n')
        moved_vehicles = {}
        for state in move_order:
            moved_vehicles[state.move[0].name] = f'{state.move[0].name}{str(state.move[0].fuel)}'
            file.write(f'{state.move[0].name} {state.move[1]} {str(state.move[2])} \t {str(state.move[0].fuel)} {str(state)} \t {" ".join([moved_vehicles[v] for v in moved_vehicles])}\n')
        
        file.write('\n')
        file.write('! ' + ' '.join(moved_vehicles.values()) + '\n')
        file.write(move_order[-1].get_board_display() + '\n')
    file.write('--------------------------------------------------------------------------------\n')

def write_to_search_file(file_name, search_paths):
    directory = 'Output'
    if not os.path.exists(directory):
        os.mkdir(directory)
    file = open(file_name, 'w')

    for path in search_paths:
        path_vehicle_details = ''
        current_path = path
        while current_path.previous_state:
           path_vehicle_details += current_path.move[0].name + str(current_path.move[0].fuel) +' '
           current_path = current_path.previous_state

        file.write(f'{path.fCost} {path.gCost} {path.hCost} {str(path)} {path_vehicle_details} \n')

    
def get_file_name(algo_class_name, puzzle_number, heuristic_number, is_sol):
    file_type = 'sol' if is_sol else 'search'
    directory = 'Output'
    file_name = ''
    if 'UCS' in algo_class_name:
        file_name = '{directory}\\{algo}-{file_type}-{puzzle_number}.txt'.format(directory=directory, algo='ucs', file_type=file_type, puzzle_number=puzzle_number)
    elif 'GBFS' in algo_class_name:
        file_name = '{directory}\\{algo}-h{heuristic_number}-{file_type}-{puzzle_number}.txt'.format(directory=directory, algo='gbfs', file_type=file_type, heuristic_number=heuristic_number, puzzle_number=puzzle_number)
    elif 'ASTAR' in algo_class_name:
        file_name = '{directory}\\{algo}-h{heuristic_number}-{file_type}-{puzzle_number}.txt'.format(directory=directory, algo='a-star', file_type=file_type, heuristic_number=heuristic_number, puzzle_number=puzzle_number)
    else: 
        raise 'no algo matches the one given'
    return file_name

heuristic_count = 1
for s, solver in enumerate(solvers):

    if solvers[s-1].__class__.__name__ == solvers[s].__class__.__name__:
        heuristic_count+=1
    else:
        heuristic_count = 1
    for i, parkingLot in enumerate(puzzles):

        print("Solving Puzzle ", i + 1, '\n')
        #parkingLot.print_board()

        #with cProfile.Profile() as pr:
        startTime = time.perf_counter()
        solution, searched_states = solver.solve(parkingLot)
        endTime = time.perf_counter()
        #pr.print_stats('cumulative')

        move_order = None
        solution_file = get_file_name(solver.__class__.__name__, i + 1, heuristic_count, True)
        search_file = get_file_name(solver.__class__.__name__, i + 1, heuristic_count, False)
        if not solution:
            print('no solution found')
        else:
            move_order = [solution]
            while solution.previous_state and solution.previous_state.previous_state:
                move_order.append(solution.previous_state)
                solution = solution.previous_state
            
            move_order.reverse()

        write_solution_to_file(solution_file, parkingLot, move_order, searched_states, endTime - startTime)
        write_to_search_file(search_file, searched_states)

