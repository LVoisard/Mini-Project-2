import numpy as np
import copy
from Vehicle import Vehicle
from Vehicle import Orientation
from Vehicle import Direction

class ParkingLot(object):
    def __init__(self, origin=None):
        if origin:
            self.copy_constructor(origin)
        else:
            self.non_copy_constructor()

    def non_copy_constructor(self):
        self.sizeX = 6
        self.sizeY = 6
        self.grid = np.ndarray((6,6), Vehicle)        
        self.previous_state = None
        self.vehicles = []
        self.move = []
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0

    def copy_constructor(self, origin):
        self.sizeX = origin.sizeX
        self.sizeY = origin.sizeY
        self.grid = np.ndarray((6,6), Vehicle)
        self.vehicles = []
        for v in origin.vehicles:
            self.add_vehicle(Vehicle(v.name, v.x, v.y, v.size, v.orientation, v.fuel))
        self.previous_state = None
        self.move = origin.move
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0

    def __eq__(self, other: object):
        if not other:
            return False
        
        for y in range(0, self.sizeY):
            for x in range(0, self.sizeX):
                if not self.grid[y][x] == other.grid[y][x]:
                    return False
        return True

    def __lt__(self, other):
        return self.fCost < other.fCost

    def __gt__(self, other):
        return self.fCost > other.fCost

    def add_vehicle(self, vehicle: Vehicle):
        for offset in range(0, vehicle.size):
            if vehicle.orientation == Orientation.HORIZONTAL:
                self.grid[vehicle.y][vehicle.x + offset] = vehicle
            else:
                self.grid[vehicle.y + offset][vehicle.x] = vehicle
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle: Vehicle):
        for offset in range(0, vehicle.size):
            if vehicle.orientation == Orientation.HORIZONTAL:
                self.grid[vehicle.y][vehicle.x + offset] = None
            else:
                self.grid[vehicle.y + offset][vehicle.x] = None
        self.vehicles.remove(vehicle)

    def get_ambulance_vehicle(self):
        for vehicle in self.vehicles:
            if vehicle.name == 'A':
                return vehicle
        return None
    
    def get_board_display(self):
        displayGrid = ''
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                vehicle = self.grid[x][y]
                if vehicle:
                    displayGrid += self.grid[x][y].get_name()
                else:
                    displayGrid += '.'
            displayGrid += '\n'
        return str(displayGrid)

    def is_vehicle_at_exit(self, vehicle):
        if vehicle.orientation == Orientation.HORIZONTAL:
            if vehicle.x == 6 - vehicle.size and vehicle.y == 2:
                return True
        return False

    def can_move_vehicle(self, vehicle, direction):
        """Returns the maximum distance for a vehicle in a specified direction"""
        if vehicle.fuel == 0:
            return 0
        
        if vehicle.orientation == Orientation.HORIZONTAL and direction == Direction.FORWARD:
            distance = 0
            while (vehicle.x + vehicle.size) + distance < self.sizeX:
                v = self.grid[vehicle.y][vehicle.x + distance + vehicle.size]
                if not v:
                    distance += 1
                else:
                    return distance
            return vehicle.fuel if vehicle.fuel < distance else distance

        elif vehicle.orientation == Orientation.HORIZONTAL and direction == Direction.BACKWARD:
            distance = 0
            while vehicle.x - distance - 1 >= 0:
                v = self.grid[vehicle.y][vehicle.x - distance - 1]
                if not v:
                    distance += 1
                else:
                    return distance
            return vehicle.fuel if vehicle.fuel < distance else distance

        elif vehicle.orientation == Orientation.VERTICAL and direction == Direction.FORWARD:
            distance = 0
            while vehicle.y - distance - 1 >= 0:
                v = self.grid[vehicle.y - distance - 1][vehicle.x]
                if not v:
                    distance += 1
                else:
                    return distance
            return vehicle.fuel if vehicle.fuel < distance else distance

        elif vehicle.orientation == Orientation.VERTICAL and direction == Direction.BACKWARD:
            distance = 0
            while (vehicle.y + vehicle.size) + distance < self.sizeY:
                v = self.grid[vehicle.y + distance + vehicle.size][vehicle.x]
                if not v:
                    distance += 1
                else:
                    return distance
            return vehicle.fuel if vehicle.fuel < distance else distance
        
        return 0

    def get_states(self):
        states = []
        for vehicle in self.vehicles:
            for direction in Direction:
                max_distance_move = self.can_move_vehicle(vehicle, direction)

                if max_distance_move == 0:
                    continue

                for distance in range(1, max_distance_move + 1):
                    new_state = ParkingLot(origin=self)
                    new_vehicle = new_state.grid[vehicle.y][vehicle.x]
                    new_state.remove_vehicle(new_vehicle)
                    new_vehicle.move(distance, direction)
                    if new_vehicle.name == 'A' or not new_state.is_vehicle_at_exit(new_vehicle):
                        new_state.add_vehicle(new_vehicle)
                    dir = ''
                    if direction == Direction.FORWARD and new_vehicle.orientation == Orientation.HORIZONTAL:
                        dir = 'R'
                    elif direction == Direction.BACKWARD and new_vehicle.orientation == Orientation.HORIZONTAL:
                        dir = 'L'
                    elif direction == Direction.FORWARD and new_vehicle.orientation == Orientation.VERTICAL:
                        dir = 'U'
                    else:
                        dir = 'D'

                    states.append([new_state, [new_vehicle, dir, distance]])
        return states


    def is_golden_state(self):
        ambulance = self.get_ambulance_vehicle()
        if ambulance:
            return self.is_vehicle_at_exit(ambulance)
        return False

    def __str__(self):
        return ''.join([element.name if element is not None else '.' for element in self.grid.flatten()])

