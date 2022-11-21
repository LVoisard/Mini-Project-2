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

#ex:
#AA.B.. = 4 - 2 = 2
#AA.CC. =  4 - 2 = 2
#AABCDE = 4 - 0 = 4
#AA.B.C = 4 - 2 = 2
#AABC.. = 4 - 1 = 3
class PositionsHeuristic(object):

    def calculate(self, parkingLot):
        open_segments = 0
        ambulance = parkingLot.get_ambulance_vehicle()
        if not ambulance:
            return 0
        x = ambulance.x + ambulance.size

        lastItem = ambulance
        while x < parkingLot.sizeX:
            vehicle = parkingLot.grid[ambulance.y][x]

            if lastItem and not vehicle:
                open_segments += 1

            lastItem = vehicle
            x += 1
        
        if open_segments > 0:
            return open_segments
        else:
            return (parkingLot.sizeX - (ambulance.x + ambulance.size))


            

