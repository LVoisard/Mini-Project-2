
import copy
from queue import PriorityQueue
from Vehicle import Orientation
from Vehicle import Direction
from ParkingLot import ParkingLot


class UCSRushHourSolver(object):

    def solve(self, parkingLot, heuristic=None):
        visited_states = set()
        open_states = PriorityQueue()
        open_states_lookup = set()
        open_states.put(parkingLot)
        open_states_lookup.add(str(parkingLot))

        while not open_states.empty() > 0:
            current_state = open_states.get()
            open_states_lookup.remove(str(current_state))

            if current_state.is_golden_state():
                return current_state, len(visited_states)

            visited_states.add(str(current_state))

            next_states = current_state.get_states()
            for state, moves in next_states:
                if str(state) in visited_states:
                    continue
                
                state.cost = current_state.cost + 1
                state.previous_state = current_state
                state.move = moves

                if str(state) not in open_states_lookup:
                    open_states.put(state)
                    open_states_lookup.add(str(state))
                
        return None, len(visited_states)


class GBFSRushHourSolver(object):
    def solve(self, parkingLot, heuristic):
        visited_states = set()  # Closed list
        open_states = PriorityQueue()  # Open list, sorted according to f(n)
        open_states_lookup = set()  # Unordered iterable set, to verify if current_state is in the open list
        open_states.put(parkingLot)
        open_states_lookup.add(str(parkingLot))

        while not open_states.empty() > 0:  # As long as the open list isn't empty
            current_state = open_states.get()  # Get the state with the lowest f(n)
            open_states_lookup.remove(str(current_state))  # Remove the state with the lowest f(n) from the open list lookup

            if current_state.is_golden_state():  # Check if the current state is the goal
                return current_state, len(visited_states)

            visited_states.add(str(current_state))  # Add the current state to the closed list

            next_states = current_state.get_states()  # Retrieve the state's successors
            for state, moves in next_states:  # For every successor state and its possible moves
                if str(state) in visited_states:  # If the state has already been visited
                    continue
                
                state.cost = heuristic.calculate(current_state)  # Calculate f(n)
                state.previous_state = current_state  # Set the parent to the current_state
                state.move = moves  # Set the possible moves

                if str(state) not in open_states_lookup:  # Add the successor state to the open list
                    open_states.put(state)
                    open_states_lookup.add(str(state))

        return None, len(visited_states)


class ASTARRushHourSolver(object):
    def solve(self, parkingLot, heuristic):
        visited_states = set()  # Closed list
        open_states = PriorityQueue()  # Open list, sorted according to f(n)
        open_states_lookup = set()  # Unordered iterable set, to verify if current_state is in the open list
        open_states.put(parkingLot)
        open_states_lookup.add(str(parkingLot))

        while not open_states.empty() > 0:  # As long as the open list isn't empty
            current_state = open_states.get()  # Get the state with the lowest f(n)
            open_states_lookup.remove(str(current_state))  # Remove the state with the lowest f(n) from the open list lookup

            if current_state.is_golden_state():  # Check if the current state is the goal
                return current_state, len(visited_states)

            visited_states.add(str(current_state))  # Add the current state to the closed list

            next_states = current_state.get_states()  # Retrieve the state's successors
            for state, moves in next_states:  # For every successor state and its possible moves
                if str(state) in visited_states:  # If the state has already been visited
                    continue

                state.cost = heuristic.calculate(current_state) + current_state.cost  # Calculate f(n)
                state.previous_state = current_state  # Set the parent to the current_state
                state.move = moves  # Set the possible moves

                if str(state) not in open_states_lookup:  # Add the successor state to the open list
                    open_states.put(state)
                    open_states_lookup.add(str(state))

        return None, len(visited_states)

