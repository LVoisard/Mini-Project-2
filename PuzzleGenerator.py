import random

car_names = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]


def generate_puzzle():
    grid = ["." for i in range(36)]
    # First, we position the ambulance on the third row
    ambulance_pos = random.randrange(12, 16)
    grid[ambulance_pos] = "A"
    grid[ambulance_pos + 1] = "A"

    # We remove the ambulance from the list of available spots.
    available_spots = [i for i in range(36)]
    del available_spots[ambulance_pos:ambulance_pos + 2]

    num_cars_horizontal = random.randrange(2, 5)
    num_cars_vertical = random.randrange(2, 5)

    available_spots = place_horizontal_cars(num_cars_horizontal, grid, available_spots)
    available_spots = place_vertical_cars(num_cars_vertical, grid, available_spots)

    # Printing the grid into the console
    row = ""
    for i in range(36):
        row += grid[i]
        if (i+1) % 6 == 0:
            print(row)
            row = ""


def place_horizontal_cars(num_cars_horizontal, grid, available_spots):
    for i in range(num_cars_horizontal):
        isPlaced = False
        while not isPlaced:
            # A random position is taken from the list of available positions
            position = available_spots[random.randrange(0, len(available_spots))]

            # Ideal scenario: 2 spaces available next to each other
            if (position + 1) in available_spots and (position + 1) % 6 != 0:
                available_spots = place_car_right(grid, position, available_spots)
                isPlaced = True
                continue

            # If the position is at the far right of the grid
            # OR if the position is not at the far right, but the right spot is taken
            if (position + 1) % 6 == 0 or (position + 1) not in available_spots:
                # We check the left spot.
                # If the left spot is free
                if (position - 1) in available_spots:
                    available_spots = place_car_left(grid, position, available_spots)
                    isPlaced = True
                    continue

            # Neither the left or right spot is free
            # Remove 'position' from the available spots as a car can't fit there
            del available_spots[position]

    return available_spots


def place_vertical_cars(num_cars_vertical, grid, available_spots):
    for i in range(num_cars_vertical):
        isPlaced = False
        while not isPlaced:
            # A random position is taken from the list of available positions
            position = available_spots[random.randrange(0, len(available_spots))]

            # Ideal scenario: 2 spaces available on top of each other
            if (position + 6) in available_spots:
                available_spots = place_car_down(grid, position, available_spots)
                isPlaced = True
                continue

            # If the position down is out of the grid or is taken
            if (position + 6) > 35 or (position + 6) not in available_spots:
                # We check the position up.
                # If the position up is available
                if (position - 6) in available_spots:
                    available_spots = place_car_up(grid, position, available_spots)
                    isPlaced = True
                    continue

            # Neither the up nor down spot is free
            # Remove 'position' from the available spots as a car can't fit there
            del available_spots[position]

    return available_spots


def place_car_up(grid, position, available_spots):
    # Add the car to it
    grid[position] = car_names[0]
    grid[position - 6] = car_names[0]

    # Remove them from the available spots
    to_remove = [position - 6, position]
    available_spots = [ele for ele in available_spots if ele not in to_remove]

    # Update the car_names list
    car_names.pop(0)
    return available_spots


def place_car_down(grid, position, available_spots):
    # Add the car to it
    grid[position] = car_names[0]
    grid[position + 6] = car_names[0]

    # Remove them from the available spots
    to_remove = [position, position + 6]
    available_spots = [ele for ele in available_spots if ele not in to_remove]

    # Update the car_names list
    car_names.pop(0)
    return available_spots


def place_car_left(grid, position, available_spots):
    # Add the car to it
    grid[position] = car_names[0]
    grid[position - 1] = car_names[0]

    # Remove them from the available spots
    to_remove = [position-1, position]
    available_spots = [ele for ele in available_spots if ele not in to_remove]

    # Update the car_names list
    car_names.pop(0)
    return available_spots


def place_car_right(grid, position, available_spots):
    # Add the car to it
    grid[position] = car_names[0]
    grid[position + 1] = car_names[0]

    # Remove them from the available spots
    to_remove = [position, position+1]
    available_spots = [ele for ele in available_spots if ele not in to_remove]

    # Update the car_names list
    car_names.pop(0)
    return available_spots


if __name__ == '__main__':
    generate_puzzle()
