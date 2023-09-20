# Finn Boyle, 18034590
import random

# variables
game_over = False
num_rows, num_cols = (10, 10)

# Public boards (visible to player)
player_board = [["~" for i in range(num_cols)] for j in range(num_rows)]
ai_board = [["~" for i in range(num_cols)] for j in range(num_rows)]

# Aim boards, player shoots at AI board, and AI shoots at player board
player_to_ai_board = [["~" for i in range(num_cols)] for j in range(num_rows)]
ai_to_player_board = [["~" for i in range(num_cols)] for j in range(num_rows)]

# Game boards without text formatting, for use in processing (inaccessible to player and AI)
player_hidden = [["~" for i in range(num_cols)] for j in range(num_rows)]
ai_hidden = [["~" for i in range(num_cols)] for j in range(num_rows)]

# Ship type, length, placement status and board symbol
player_ships = {
    "Carrier": {'length': 5, 'is_placed': False, 'symbol': "A", 'hits_to_sink': 5, 'is_sunk': False},
    "Battleship": {'length': 4, 'is_placed': False, 'symbol': "B", 'hits_to_sink': 4, 'is_sunk': False},
    "Cruiser": {'length': 3, 'is_placed': False, 'symbol': "C", 'hits_to_sink': 3, 'is_sunk': False},
    "Submarine": {'length': 3, 'is_placed': False, 'symbol': "S", 'hits_to_sink': 3, 'is_sunk': False},
    "Destroyer": {'length': 2, 'is_placed': False, 'symbol': "D", 'hits_to_sink': 2, 'is_sunk': False}
}
ai_ships = {
    "Carrier": {'length': 5, 'is_placed': False, 'symbol': "A", 'hits_to_sink': 5, 'is_sunk': False},
    "Battleship": {'length': 4, 'is_placed': False, 'symbol': "B", 'hits_to_sink': 4, 'is_sunk': False},
    "Cruiser": {'length': 3, 'is_placed': False, 'symbol': "C", 'hits_to_sink': 3, 'is_sunk': False},
    "Submarine": {'length': 3, 'is_placed': False, 'symbol': "S", 'hits_to_sink': 3, 'is_sunk': False},
    "Destroyer": {'length': 2, 'is_placed': False, 'symbol': "D", 'hits_to_sink': 2, 'is_sunk': False}
}


# Text formatting
ANSI_RESET = "\033[0m"
ANSI_BOLD_YELLOW = "\033[1;33m"
ANSI_BOLD_RED = "\033[1;31m"
ANSI_RED = "\033[31m"
ANSI_BLUE = "\033[34m"


# Print the boards of both the player and AI, side by side, one row at a time
def print_board():
    i = 0

    print(ANSI_BOLD_RED + "     Player's Board" + " "*15 + "AI's Board     " + ANSI_RESET)
    print(ANSI_BOLD_YELLOW + "  0 1 2 3 4 5 6 7 8 9" + " "*9 + "0 1 2 3 4 5 6 7 8 9" + ANSI_RESET)

    for row in range(num_rows):
        print(ANSI_BOLD_YELLOW + str(i) + ANSI_RESET, end=' ')

        for col in range(num_cols):
            print(player_board[row][col], end=' ')

        print(" "*5, end=' ')

        print(ANSI_BOLD_YELLOW + str(i) + ANSI_RESET, end=' ')

        for col in range(num_cols):
            print(ai_board[row][col], end=' ')

        print()
        i += 1
        # Function end


# Check if the player or AI has won
def win_check(check):
    if all(ship['is_sunk'] for ship in player_ships.values()):
        print("TEST WIN")
        check = True


# Check firing input coordinates
def check_input(row, col, hidden_board):
    if (0 <= row <= 9) and (0 <= col <= 9):
        return True
    elif hidden_board[row][col] == "M" or hidden_board[row][col] == "H":
        print("Cannot fire shot here!")
        return False
    else:
        print("Firing location out of bounds!")
        return False


# Fire a shot at the other player's board
def fire(game_board, hidden_board):
    confirm = False

    print("Prepare to fire, enter coordinates: ")
    while not confirm:
        row_in = input("Row (0-9): ")
        col_in = input("Column (0-9): ")

        row_in, col_in = to_int(row_in, col_in)

        temp = input("Confirm shot? Y/N")
        # If player confirms shot, and the shot is valid, allow the shot to be fired. This will end the turn
        if temp == "Y" and check_input(row_in, col_in, hidden_board):
            confirm = True
            row_confirmed = row_in
            col_confirmed = col_in
            print("Firing...")

            check_if_hit(row_confirmed, col_confirmed, game_board, hidden_board)
        else:
            print("Location unconfirmed, re-enter coordinate data.")


# Check if a shot hit
def check_if_hit(row, col, game_board, hidden_board):
    if hidden_board[row][col] == "~":
        hidden_board[row][col] = "M"
        game_board[row][col] = "M"
        print("Miss!")
        print_board()
    # Is the shot going to hit a ship?
    elif hidden_board[row][col] in {ship['symbol'] for ship in player_ships.values()}:
        update_ship_status(row, col, hidden_board)
        hidden_board[row][col] = "H"
        game_board[row][col] = ANSI_RED + "H" + ANSI_RESET
        print("Hit!")
        print_board()
    elif hidden_board[row][col] == "M" or hidden_board[row][col] == "H":
        print("Shot already taken in this location, fire again!")
    else:
        print("Could not check if shot hit.")
        print_board()


def update_ship_status(row, col, hidden_board):
    symbol = hidden_board[row][col]
    # Check if symbol exists in the ship dictionary
    if symbol in {ship['symbol'] for ship in player_ships.values()}:
        # Find the ship with the matching symbol and decrement its 'hits_to_sink' value
        for ship in player_ships.values():
            if ship['symbol'] == symbol:
                ship['hits_to_sink'] -= 1
                check_sunk(symbol)
                break
    else:
        print("Ship hit not in dictionary.")


def check_sunk(symbol):
    for name, attributes in player_ships.items():
        if attributes['symbol'] == symbol and attributes['hits_to_sink'] == 0:
            attributes['is_sunk'] = True


# Start of game, place ships on board
def start_place_ships(public_board, hidden_board, is_ai):
    if not is_ai:
        print("Ships to launch: ")
        for ship_name, attributes in player_ships.items():
            if not attributes['is_placed']:
                print(ship_name)

        # board_in = input("Input board type: ")
        ship_in = input("Ship to deploy: ")
        row_in = input("Deployment row (0-9): ")
        col_in = input("Deployment column (0-9): ")
        orientation_in = input("Deployment orientation (horizontal or vertical): ")

        # Place ships on board and print board to user
        place_ships(public_board, hidden_board, ship_in, row_in, col_in, orientation_in)
    elif is_ai:
        unplaced = [ship_name for ship_name, attributes in ai_ships.items() if not attributes['is_placed']]

        if unplaced:
            random_ship = random.choice(unplaced)
            rand_row = random.randint(0, 9)
            rand_col = random.randint(0, 9)
            rand_orient = random.choice(["vertical", "horizontal"])

            place_ships(public_board, hidden_board, random_ship, rand_row, rand_col, rand_orient)

    print_board()


# Check the number of ships that have been placed
def check_ships_placed(is_ai):
    if is_ai:
        return sum(1 for ship in ai_ships.values() if ship['is_placed'])
    elif not is_ai:
        return sum(1 for ship in player_ships.values() if ship['is_placed'])


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

    if (orientation == "vertical" and row + length > num_rows) or (orientation == "horizontal" and col + length > num_cols):
        print("Input coordinates are out of ship placement bounds.")
        return False

    if orientation == "vertical" or orientation == "horizontal":
        return True
    else:
        print("Unrecognised orientation type, only 'horizontal' or 'vertical' allowed (case sensitive)")
        return False


# Check if valid ship
def process_ship_validity(ship_type):
    if ship_type not in player_ships:
        print("Invalid ship type detected, please use one from the (case sensitive) list!")
        return False

    return True


# Place ships on your board
def place_ships(game_board, hidden_board, ship_type, row, col, orientation):

    row, col = to_int(row, col)
    can_place = True

    if process_ship_validity(ship_type):
        ship_length = player_ships[ship_type]['length']
        if process_location(row, col, ship_length, orientation):
            if ship_type in player_ships and not player_ships[ship_type]['is_placed']:
                symbol = player_ships[ship_type]['symbol']
                if orientation == "horizontal":
                    for i in range(ship_length):
                        if hidden_board[row][col + i] != "~":
                            can_place = False
                    for i in range(ship_length):
                        if can_place:
                            game_board[row][col + i] = ANSI_BLUE + symbol + ANSI_RESET
                            hidden_board[row][col + i] = symbol
                elif orientation == "vertical":
                    for i in range(ship_length):
                        if hidden_board[row + i][col] != "~":
                            can_place = False
                    for i in range(ship_length):
                        if can_place:
                            game_board[row + i][col] = ANSI_BLUE + symbol + ANSI_RESET
                            hidden_board[row + i][col] = symbol
                else:
                    print("Unrecognised orientation type, only 'horizontal' or 'vertical' allowed (case sensitive).")

                if not can_place:
                    print("A pre-existing ship is blocking this placement location.")
                else:
                    player_ships[ship_type]['is_placed'] = True
            else:
                print("Ship type unrecognised, or ship is already placed.")
        else:
            print("Could not verify ship placement coordinate data (row, column, orientation).")
    else:
        print("Could not verify ship type.")


# Game loop
while not game_over:
    print_board()

    # Allow player to place ships
    while check_ships_placed(False) < len(player_ships):
        start_place_ships(player_board, player_hidden, False)

    # Randomly place AI ships
    # while check_ships_placed(True) < len(ai_ships):
        # start_place_ships(ai_board, ai_hidden, True)

    while not win_check(game_over):
        user_turn = input("Step? ")
        fire(player_board, player_hidden)

    win_check(game_over)
    # Check if a hit, update game board

    # AI's turn
    # Implement AI logic to choose coordinates
    # Check if a hit, update game board

    # Check win condition

# Ask if the user wants to play again
