import numpy as np
import pandas as pd
import copy
import sys
import time
import cProfile
import os
from ParkingLot import ParkingLot
from RushHourPuzzleLoader import RushHourPuzzleLoader
import RushHourPuzzleSolver
import Heuristics

puzzles = RushHourPuzzleLoader.load_puzzles(False)

solvers = [
    # UCS
    RushHourPuzzleSolver.UCSRushHourSolver(),
    # GBFS
    RushHourPuzzleSolver.GBFSRushHourSolver(Heuristics.BlockingVehiclesHeuristic()), 
    RushHourPuzzleSolver.GBFSRushHourSolver(Heuristics.BlockedPositionsHeuristic()),
    RushHourPuzzleSolver.GBFSRushHourSolver(Heuristics.BlockingVehiclesHeuristic(3)),
    RushHourPuzzleSolver.GBFSRushHourSolver(Heuristics.CustomHeuristic()),
    #A STAR
    RushHourPuzzleSolver.ASTARRushHourSolver(Heuristics.BlockingVehiclesHeuristic()),
    RushHourPuzzleSolver.ASTARRushHourSolver(Heuristics.BlockedPositionsHeuristic()),
    RushHourPuzzleSolver.ASTARRushHourSolver(Heuristics.BlockingVehiclesHeuristic(3)),
    RushHourPuzzleSolver.ASTARRushHourSolver(Heuristics.CustomHeuristic())]
    
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
    file.write(parkingLot.get_board_display())
    file.write('\n')
    file.write('Car fuel available: ')
    file.write(', '.join(car_fuel_available))
    file.write('\n')
    file.write('\n')

    if not move_order:
        file.write('Sorry, could not solve the puzzle as specified.\n')
        file.write('Error: no solution found\n')
    
    file.write(f'Runtime: {runtime:0.5f} seconds \n')

    if move_order:
        file.write(f'Search path length: {str(len(search_states))} states \n')
        file.write(f'Solution path length: {str(len(move_order))} moves \n')
        file.write(f'Solution path: {"; ".join([f"{state.move[0].name} {state.move[1]} {state.move[2]}" for state in move_order])} \n')

        file.write('\n')
        for state in move_order:
            file.write(f'{state.move[0].name} {state.move[1]} {str(state.move[2])} \t {str(state.move[0].fuel)} {str(state)}\n')
        
        file.write('\n')
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
    elif 'A/A*' in algo_class_name:
        file_name = '{directory}\\{algo}-h{heuristic_number}-{file_type}-{puzzle_number}.txt'.format(directory=directory, algo='a-star', file_type=file_type, heuristic_number=heuristic_number, puzzle_number=puzzle_number)
    else: 
        raise 'no algo matches the one given'
    return file_name

data = []

heuristic_count = 1


for i, parkingLot in enumerate(puzzles):
    for s, solver in enumerate(solvers):

        if solvers[s-1].__class__.__name__ == solvers[s].__class__.__name__:
            heuristic_count+=1
        else:
            heuristic_count = 1

        algo_name = ''
        if 'UCS' in solver.__class__.__name__:
            algo_name = 'UCS'
        elif 'GBFS' in solver.__class__.__name__:
            algo_name = 'GBFS'
        elif 'ASTAR' in solver.__class__.__name__:
            algo_name = 'A/A*'

        print("Solving Puzzle ", i + 1, '\n')
        #parkingLot.print_board()

        #with cProfile.Profile() as pr:
        startTime = time.perf_counter()
        solution, searched_states = solver.solve(parkingLot)
        endTime = time.perf_counter()
        execution_time = endTime - startTime

        #pr.print_stats('cumulative')

        move_order = None
        solution_file = get_file_name(algo_name, i + 1, heuristic_count, True)
        search_file = get_file_name(algo_name, i + 1, heuristic_count, False)
        if not solution:
            print('no solution found')
        else:
            print('solved \n')

            move_order = [solution]
            while solution.previous_state and solution.previous_state.previous_state:
                move_order.append(solution.previous_state)
                solution = solution.previous_state
            
            move_order.reverse()

        write_solution_to_file(solution_file, parkingLot, move_order, searched_states, execution_time)
        write_to_search_file(search_file, searched_states)
        data.append([i + 1, algo_name, f'h{heuristic_count}' if algo_name != 'UCS' else 'NA', len(move_order) if move_order else np.nan, len(searched_states), execution_time])
columns=['Puzzle Number', 'Algorithm', 'Heuristic', 'Length of the Solution', 'Length of the Search Path', 'Execution Time (in seconds)']
dataFrame = pd.DataFrame(data=data, columns=columns)
writer = pd.ExcelWriter("Rush Hour Analysis.xlsx", engine='xlsxwriter')
dataFrame.to_excel(writer, sheet_name='Sheet1', index=False)

avg_columns = ['Algorithm', 'Heuristic','Average Length of the Solution', 'Average Length of the Search Path', 'Average Execution Time (in seconds)']

df = pd.concat([
dataFrame.loc[dataFrame['Algorithm'] == 'UCS'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0).to_frame().T,
dataFrame.loc[dataFrame['Algorithm'] == 'GBFS'].loc[dataFrame['Heuristic'] == 'h1'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0, numeric_only=True, skipna=True).to_frame().T,
dataFrame.loc[dataFrame['Algorithm'] == 'GBFS'].loc[dataFrame['Heuristic'] == 'h2'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0, numeric_only=True, skipna=True).to_frame().T,
dataFrame.loc[dataFrame['Algorithm'] == 'GBFS'].loc[dataFrame['Heuristic'] == 'h3'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0,numeric_only=True, skipna=True).to_frame().T,
dataFrame.loc[dataFrame['Algorithm'] == 'GBFS'].loc[dataFrame['Heuristic'] == 'h4'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0,numeric_only=True, skipna=True).to_frame().T,
dataFrame.loc[dataFrame['Algorithm'] == 'A/A*'].loc[dataFrame['Heuristic'] == 'h1'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0,numeric_only=True, skipna=True).to_frame().T,
dataFrame.loc[dataFrame['Algorithm'] == 'A/A*'].loc[dataFrame['Heuristic'] == 'h2'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0,numeric_only=True, skipna=True).to_frame().T,
dataFrame.loc[dataFrame['Algorithm'] == 'A/A*'].loc[dataFrame['Heuristic'] == 'h3'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0,numeric_only=True, skipna=True).to_frame().T,
dataFrame.loc[dataFrame['Algorithm'] == 'A/A*'].loc[dataFrame['Heuristic'] == 'h4'][['Length of the Solution','Length of the Search Path','Execution Time (in seconds)']].mean(axis=0,numeric_only=True, skipna=True).to_frame().T
])

df['Algorithm'] = ['UCS', 'GBFS','GBFS','GBFS','GBFS', 'A/A*', 'A/A*', 'A/A*', 'A/A*']
df['Heuristic'] = ['NA', 'h1','h2','h3','h4','h1','h2','h3','h4',]
df.to_excel(writer, sheet_name='Averages', index=False)

workbook = writer.book
workheet1 = writer.sheets['Sheet1']
workheet2 = writer.sheets['Averages']

time_format = workbook.add_format({'num_format': '#,###0.000'})

workheet1.set_column(0, 0, 15, None)
workheet1.set_column(3, 3, 20, None)
workheet1.set_column(4, 4, 23, None)
workheet1.set_column(5, 5, 25, None)

workheet1.set_column(0, 0, 20, None)
workheet1.set_column(1, 1, 23, None)
workheet1.set_column(2, 2, 25, None)

writer.save()

