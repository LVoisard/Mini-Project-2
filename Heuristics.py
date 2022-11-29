from Vehicle import Orientation

class DepthHeuristic(object):

    def calculate(self, parkingLot):
        return 1

class BlockingVehiclesHeuristic(object):

    def __init__(self, multiplier=1):
        self.multiplier = multiplier

    def calculate(self, parkingLot):
        vehicles = []
        ambulance = parkingLot.get_ambulance_vehicle()
        if not ambulance:
            return 0
        for x in range(ambulance.x + ambulance.size - 1, parkingLot.sizeX):
            vehicle = parkingLot.grid[ambulance.y][x]
            if vehicle and vehicle not in vehicles:
                vehicles.append(vehicle)
        return len(vehicles) * self.multiplier

class BlockedPositionsHeuristic(object):

    def calculate(self, parkingLot):
        positionCount = 0
        ambulance = parkingLot.get_ambulance_vehicle()
        if not ambulance:
            return 0
        for x in range(ambulance.x + ambulance.size - 1, parkingLot.sizeX):
            vehicle = parkingLot.grid[ambulance.y][x]
            if vehicle:
                positionCount += 1
        return positionCount

# number of open segments, if segements is 0, return positions between ambulance and exit

class CustomHeuristic(object):

    def calculate(self, parkingLot):
        ambulance = parkingLot.get_ambulance_vehicle()
        if not ambulance:
            return 0
        blocking_vehicles = []
        direct_blocking = 0
        for x in range(ambulance.x + ambulance.size, parkingLot.sizeX):
            vehicle = parkingLot.grid[ambulance.y][x]
            if vehicle and vehicle not in blocking_vehicles:
                blocking_vehicles.append(vehicle)
                direct_blocking += 1
        
        blocking_cost = 0
        indirect_blocking_vehicles = []
        for vehicle in blocking_vehicles:
            if vehicle.orientation == Orientation.VERTICAL:
                blocking_up = 0
                blocking_down = 0
                if vehicle.size < 3:
                    for y in range(0, vehicle.y):
                        blocking_v = parkingLot.grid[y][vehicle.x]
                        if blocking_v and blocking_v not in indirect_blocking_vehicles:
                            indirect_blocking_vehicles.append(blocking_v)
                            blocking_up += 1
                else:
                    blocking_up += 100
                for y in range(vehicle.y + vehicle.size, min(vehicle.y + vehicle.size + vehicle.size - 1, parkingLot.sizeY)):
                    blocking_v = parkingLot.grid[y][vehicle.x]
                    if blocking_v and blocking_v not in indirect_blocking_vehicles:
                        indirect_blocking_vehicles.append(blocking_v)
                        blocking_down += 1
                blocking_cost += min(blocking_up, blocking_down)
        return direct_blocking + blocking_cost


        


            

