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

class OpenPositionsHeuristic(object):

    def calculate(self, parkingLot):
        openPositionsCount = 0
        ambulance = parkingLot.get_ambulance_vehicle()
        if not ambulance:
            return 0
        for x in range(0, parkingLot.sizeX):
            vehicle = parkingLot.grid[ambulance.y][x]
            if not vehicle:
                openPositionsCount += 1
        return parkingLot.sizeX - openPositionsCount



            

