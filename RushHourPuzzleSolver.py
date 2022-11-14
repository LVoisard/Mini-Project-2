
import copy
from queue import PriorityQueue
from Vehicle import Orientation
from Vehicle import Direction
from ParkingLot import ParkingLot

class RushHourPuzzleSolver(object):

    def can_move_vehicle(self, vehicle, direction, parkingLot):
        """Returns the maximum distance for a vehicle in a specified direction"""
        if vehicle.fuel == 0:
            return 0
        
        if vehicle.orientation == Orientation.HORIZONTAL and direction == Direction.FORWARD:
            distance = 0
            while (vehicle.x + vehicle.size) + distance < parkingLot.sizeX:
                v = parkingLot.grid[vehicle.y][vehicle.x + distance + vehicle.size]
                if not v:
                    distance += 1
                else:
                    return distance
            return vehicle.fuel if vehicle.fuel < distance else distance

        elif vehicle.orientation == Orientation.HORIZONTAL and direction == Direction.BACKWARD:
            distance = 0
            while vehicle.x - distance - 1 >= 0:
                v = parkingLot.grid[vehicle.y][vehicle.x - distance - 1]
                if not v:
                    distance += 1
                else:
                    return distance
            return vehicle.fuel if vehicle.fuel < distance else distance

        elif vehicle.orientation == Orientation.VERTICAL and direction == Direction.FORWARD:
            distance = 0
            while vehicle.y - distance - 1 >= 0:
                v = parkingLot.grid[vehicle.y - distance - 1][vehicle.x]
                if not v:
                    distance += 1
                else:
                    return distance
            return vehicle.fuel if vehicle.fuel < distance else distance

        elif vehicle.orientation == Orientation.VERTICAL and direction == Direction.BACKWARD:
            distance = 0
            while (vehicle.y + vehicle.size) + distance < parkingLot.sizeY:
                v = parkingLot.grid[vehicle.y + distance + vehicle.size][vehicle.x]
                if not v:
                    distance += 1
                else:
                    return distance
            return vehicle.fuel if vehicle.fuel < distance else distance
        
        return 0

    def get_states(self, parkingLot):
        states = []
        vehicles_moved = []
        for y in range(0, parkingLot.sizeY):
            for x in range(0, parkingLot.sizeX):

                vehicle = parkingLot.grid[x][y]
                if not vehicle or any(v == vehicle for v in vehicles_moved):
                    continue

                for direction in Direction:
                    max_distance_move = self.can_move_vehicle(vehicle, direction, parkingLot)

                    if max_distance_move == 0:
                        continue

                    for distance in range(1, max_distance_move + 1):
                        new_state = ParkingLot(origin=parkingLot)
                        new_vehicle = new_state.grid[x][y]
                        new_state.remove_vehicle(new_vehicle)
                        new_vehicle.move(distance, direction)
                        new_state.add_vehicle(new_vehicle)
                        states.append(new_state)
                        vehicles_moved.append(new_vehicle)
        return states

    def is_golden_state(self, parkingLot):
        ambulance = parkingLot.get_ambulance_vehicle()
        if ambulance.x == 4 and ambulance.y == 2:
            return True
        return False


    def solve(self, parkingLot):
        visited_states = set()
        open_states = PriorityQueue()
        open_states_lookup = set()
        open_states.put(parkingLot)
        open_states_lookup.add(str(parkingLot))

        while not open_states.empty() > 0:
            current_state = open_states.get()

            if self.is_golden_state(current_state):
                return current_state, len(visited_states)

            visited_states.add(str(current_state))
            open_states_lookup.remove(str(current_state))

            following_states = self.get_states(current_state)

            for state in following_states:
                if str(state) in visited_states:
                    continue
                
                state.cost = 1 + current_state.cost
                state.previous_state = current_state

                if str(state) not in open_states_lookup:
                    open_states.put(state)
                    open_states_lookup.add(str(state))
                

        return None, len(visited_states)

