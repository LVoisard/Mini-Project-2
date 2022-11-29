
import copy
from queue import PriorityQueue
from Vehicle import Orientation
from Vehicle import Direction
from ParkingLot import ParkingLot

# Everytime you visit a state, it is the first time
# no need to look in the opened list
class UCSRushHourSolver(object):

    def solve(self, parkingLot):
        visited_states = []
        visited_states_lookup = set() # O(1)
        open_states = PriorityQueue() # Open list, sorted according to f(n)
        open_states_lookup = set() # O(1) # Unordered iterable set, to verify if current_state is in the open list
        open_states.put(parkingLot)
        open_states_lookup.add(str(parkingLot))

        while not open_states.empty(): # As long as the open list isn't empty
            current_state = open_states.get()  # Get the state with the lowest f(n)
            open_states_lookup.remove(str(current_state)) # Remove the state with the lowest f(n) from the open list lookup

            visited_states_lookup.add(str(current_state))  # Add the current state to the closed list
            visited_states.append(current_state)

            if current_state.is_golden_state(): # Check if the current state is the goal
                return current_state, visited_states

            next_states = current_state.get_states() # Retrieve the state's successors
            for state, moves in next_states: # For every successor state and its possible moves
                if str(state) in visited_states_lookup: # If the state has already been visited
                    continue
                
                state.gCost = current_state.gCost + 1
                state.fCost = state.gCost + state.hCost # Calculate f(n)
                state.previous_state = current_state # Set the parent to the current_state
                state.move = moves

                if str(state) not in open_states_lookup: # Add the successor state to the open list
                    open_states.put(state)
                    open_states_lookup.add(str(state))
                
        return None, visited_states

# doesnt remeber the depth of the nodes (number of previous moves)
class GBFSRushHourSolver(object):

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solve(self, parkingLot):
        visited_states = []
        visited_states_lookup = set()  # Closed list
        open_states = PriorityQueue()  # Open list, sorted according to f(n)
        open_states_lookup = set()  # Unordered iterable set, to verify if current_state is in the open list
        open_states.put(parkingLot)
        open_states_lookup.add(str(parkingLot))

        while not open_states.empty():  # As long as the open list isn't empty
            current_state = open_states.get()  # Get the state with the lowest f(n)
            open_states_lookup.remove(str(current_state))  # Remove the state with the lowest f(n) from the open list lookup

            visited_states_lookup.add(str(current_state))  # Add the current state to the closed list
            visited_states.append(current_state)
            
            if current_state.is_golden_state():  # Check if the current state is the goal
                return current_state, visited_states

            next_states = current_state.get_states()  # Retrieve the state's successors
            for state, moves in next_states:  # For every successor state and its possible moves
                if str(state) in visited_states_lookup:  # If the state has already been visited
                    continue
                
                state.gCost = current_state.gCost # always 0
                state.hCost = self.heuristic.calculate(current_state)
                state.fCost = state.gCost + state.hCost # Calculate f(n)
                state.previous_state = current_state  # Set the parent to the current_state
                state.move = moves  # Set the possible moves

                if str(state) not in open_states_lookup:  # Add the successor state to the open list
                    open_states.put(state)
                    open_states_lookup.add(str(state))

        return None, visited_states


class ASTARRushHourSolver(object):
    
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solve(self, parkingLot):
        visited_states = []
        visited_states_lookup = set()  # Closed list
        open_states = PriorityQueue()  # Open list, sorted according to f(n)
        open_states_lookup = {}  # Unordered iterable set, to verify if current_state is in the open list and the number of times it is
        open_states.put(parkingLot)
        open_states_lookup[str(parkingLot)] = 1 # add this because we cant remove from open_state queue

        g_costs = {} # this avoids removing all the element and adding them back when looking for an element
        g_costs[str(parkingLot)] = 0

        while not open_states.empty():  # As long as the open list isn't empty
            current_state = open_states.get()  # Get the state with the lowest f(n)
            open_states_lookup[str(current_state)] -= 1 # Remove the state with the lowest f(n) from the open list lookup  

            visited_states_lookup.add(str(current_state))  # Add the current state to the closed list
            visited_states.append(current_state)
            if current_state.is_golden_state():  # Check if the current state is the goal
                return current_state, visited_states

            next_states = current_state.get_states()  # Retrieve the state's successors
            for state, moves in next_states:  # For every successor state and its possible moves

                state.gCost = current_state.gCost + 1
                state.hCost = self.heuristic.calculate(current_state)
                state.fCost = state.gCost + state.hCost # Calculate f(n)
                state.previous_state = current_state  # Set the parent to the current_state
                state.move = moves  # Set the possible moves
                
                if str(state) in visited_states_lookup:  # If the state has already been visited
                    continue

                if str(state) not in open_states_lookup or open_states_lookup[str(state)] == 0: # if the state is not in the open list
                    # Add the successor state to the open list 
                    open_states.put(state)
                    open_states_lookup[str(state)] = 1
                    g_costs[str(state)] = state.gCost
                else:  # if there is a shorter path to the successor, add it to the queue
                    if g_costs[str(state)] > state.gCost:
                        open_states.put(state)
                        open_states_lookup[str(state)] += 1
        
        return None, visited_states

