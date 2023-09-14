# Finn Boyle, 18034590

# Define game board, place ships, and set up the AI
game_over = False

rows, cols = (10, 10)
player_board = [["~" for i in range(cols)] for j in range(rows)]
ai_board = [["~" for i in range(cols)] for j in range(rows)]

# Ship type, length, placement status and board symbol
ships = {
    "Carrier": {'length': 5, 'is_placed': False, 'symbol': "A"},
    "Battleship": {'length': 4, 'is_placed': False, 'symbol': "B"},
    "Cruiser": {'length': 3, 'is_placed': False, 'symbol': "C"},
    "Submarine": {'length': 3, 'is_placed': False, 'symbol': "S"},
    "Destroyer": {'length': 2, 'is_placed': False, 'symbol': "D"}
}
num_ships_placed = 0

# Text formatting
ANSI_RESET = "\033[0m"
ANSI_BOLD_YELLOW = "\033[1;33m"
ANSI_BOLD_RED = "\033[1;31m"
ANSI_BLUE = "\033[34m"


# Print the boards of both the player and AI, side by side, one row at a time
def print_board():
    i = 0

    print(ANSI_BOLD_RED + "     Player's Board" + " "*15 + "AI's Board     " + ANSI_RESET)
    print(ANSI_BOLD_YELLOW + "  0 1 2 3 4 5 6 7 8 9" + " "*9 + "0 1 2 3 4 5 6 7 8 9" + ANSI_RESET)

    for row in range(rows):
        print(ANSI_BOLD_YELLOW + str(i) + ANSI_RESET, end=' ')

        for col in range(cols):
            print(player_board[row][col], end=' ')

        print(" "*5, end=' ')

        print(ANSI_BOLD_YELLOW + str(i) + ANSI_RESET, end=' ')

        for col in range(cols):
            print(ai_board[row][col], end=' ')

        print()
        i += 1
        # Function end


# Check if the player or AI has won
def win_check():
    pass


# Fire a shot at the other player's board
def fire():
    pass


# Check if a shot hit
def check_if_hit():
    pass


# Start of game, place ships on board
def start_place_ships():
    print("Ships to launch: ")
    for ship_name, attributes in ships.items():
        if not attributes['is_placed']:
            print(ship_name)

    # board_in = input("Input board type: ")
    ship_in = input("Ship to deploy: ")
    row_in = input("Vertical deployment location (0-9): ")
    col_in = input("Horizontal deployment location (0-9): ")
    orientation_in = input("Deployment orientation (horizontal or vertical): ")

    # Place ships on board and print board to user
    place_ships(player_board, ship_in, row_in, col_in, orientation_in)
    print_board()


# Check the number of ships that have been placed
def check_ships_placed():
    return sum(1 for ship in ships.values() if ship['is_placed'])


# convert coordinate inputs to integers
def to_int(row, col):
    try:
        row = int(row)
        col = int(col)
    except ValueError:
        row = -1
        col = -1
    return row, col


# Check if ship coordinates are usable
def process_location(row, col, length, orientation):
    if not isinstance(row, int) or not isinstance(col, int) or not (0 <= row <= 9) or not (0 <= col <= 9):
        print("Coordinate values must be integers from 0-9!")
        return False

    if (orientation == "vertical" and row + length > 9) or (orientation == "horizontal" and col + length > 9):
        print("Input coordinates are out of ship placement bounds.")
        return False

    if orientation == "vertical" or orientation == "horizontal":
        return True
    else:
        print("Unrecognised orientation type, only 'horizontal' or 'vertical' allowed (case sensitive)")
        return False


# Check if valid ship
def process_ship_validity(ship_type):
    if ship_type not in ships:
        print("Invalid ship type detected, please use one from the (case sensitive) list!")
        return False

    return True


# Place ships on your board
def place_ships(board, ship_type, row, col, orientation):

    row, col = to_int(row, col)
    can_place = True

    if process_ship_validity(ship_type):
        ship_length = ships[ship_type]['length']
        if process_location(row, col, ship_length, orientation):
            if ship_type in ships and not ships[ship_type]['is_placed']:
                symbol = ships[ship_type]['symbol']

                if orientation == "horizontal":
                    for i in range(ship_length):
                        if board[row][col + i] != "~":
                            can_place = False
                    for i in range(ship_length):
                        if can_place:
                            board[row][col + i] = ANSI_BLUE + symbol + ANSI_RESET
                elif orientation == "vertical":
                    for i in range(ship_length):
                        if board[row + i][col] != "~":
                            can_place = False
                    for i in range(ship_length):
                        if can_place:
                            board[row + i][col] = ANSI_BLUE + symbol + ANSI_RESET
                else:
                    print("Unrecognised orientation type, only 'horizontal' or 'vertical' allowed (case sensitive).")

                if not can_place:
                    print("A pre-existing ship is blocking this placement location.")
                else:
                    ships[ship_type]['is_placed'] = True
            else:
                print("Ship type unrecognised, or ship is already placed.")


# Game loop
while not game_over:
    print_board()

    while check_ships_placed() < len(ships):
        start_place_ships()

    user_turn = input("Step? ")

    # Check if a hit, update game board

    # AI's turn
    # Implement AI logic to choose coordinates
    # Check if a hit, update game board

    # Check win condition

# Ask if the user wants to play again
