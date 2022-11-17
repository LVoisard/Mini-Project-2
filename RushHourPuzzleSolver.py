
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
                
                state.cost = heuristic.calculate(current_state)
                state.previous_state = current_state
                state.move = moves

                if str(state) not in open_states_lookup:
                    open_states.put(state)
                    open_states_lookup.add(str(state))
                

        return None, len(visited_states)

