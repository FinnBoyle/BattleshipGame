# Finn Boyle, 18034590
import random

# variables
game_over = False
num_rows, num_cols = (10, 10)
player_placed = False
ai_placed = False

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
RESET = "\033[0m"
B_RED = "\033[1;31m"
B_GREEN = "\033[1;32m"
B_YELLOW = "\033[1;33m"
B_MAGENTA = "\033[1;35m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"


# Print the boards of both the player and AI, side by side, one row at a time
def print_board():
    i = 0

    print(B_MAGENTA + "     Player's Board" + " " * 15 + "AI's Board     " + RESET)
    print(MAGENTA + "  0 1 2 3 4 5 6 7 8 9" + " " * 9 + "0 1 2 3 4 5 6 7 8 9" + RESET)

    for row in range(num_rows):
        print(MAGENTA + str(i) + RESET, end=' ')

        for col in range(num_cols):
            print(player_board[row][col], end=' ')

        print(" "*5, end=' ')

        print(MAGENTA + str(i) + RESET, end=' ')

        for col in range(num_cols):
            print(ai_board[row][col], end=' ')

        print()
        i += 1
        # Function end


# If all player ships have been sunk, AI wins. If all AI ships sunk, player wins
def win_check():
    if all(ship['is_sunk'] for ship in player_ships.values()):
        print(B_GREEN + " " * 8 + "PLAYER LOSES!" + RESET)
        return True
    elif all(ship['is_sunk'] for ship in ai_ships.values()):
        print(B_RED + " "*8 + "PLAYER WINS!" + RESET)
        return True
    else:
        return False


# Check firing input coordinates
def check_input(row, col, hidden_board):
    if (0 <= row <= 9) and (0 <= col <= 9):
        return True
    elif hidden_board[row][col] == "M" or hidden_board[row][col] == "H":
        print(B_RED + " " * 8 + "Cannot fire shot here!" + RESET)
        return False
    else:
        print(B_RED + " " * 8 + "Firing location out of bounds!" + RESET)
        return False


# Fire a shot at the other player's board
def fire(game_board, hidden_board):
    confirm = False

    print(B_YELLOW + "Prepare to fire, enter coordinates: " + RESET)
    while not confirm:
        row_in = input(B_YELLOW + "Row (0-9): " + RESET)
        col_in = input(B_YELLOW + "Column (0-9): " + RESET)

        row_in, col_in = to_int(row_in, col_in)

        temp = input(B_YELLOW + "Confirm shot? Y/N " + RESET)
        # If player confirms shot, and the shot is valid, allow the shot to be fired. This will end the turn
        if temp == "Y" and check_input(row_in, col_in, hidden_board):
            confirm = True
            row_confirmed = row_in
            col_confirmed = col_in
            print(B_YELLOW + "Firing..." + RESET)

            check_if_hit(row_confirmed, col_confirmed, game_board, hidden_board)
        else:
            print(B_RED + "Location unconfirmed, re-enter coordinate data." + RESET)


# Check if a shot hit
def check_if_hit(row, col, game_board, hidden_board):
    if hidden_board[row][col] == "~":
        hidden_board[row][col] = "M"
        game_board[row][col] = "M"
        print(B_RED + " "*8 + "---Miss!---" + RESET)
        print_board()
    # Is the shot going to hit a ship?
    elif hidden_board[row][col] in {ship['symbol'] for ship in player_ships.values()}:
        update_ship_status(row, col, hidden_board)
        hidden_board[row][col] = "H"
        game_board[row][col] = RED + "H" + RESET
        print(B_GREEN + " "*8 + "---Hit!---" + RESET)
        print_board()
    elif hidden_board[row][col] == "M" or hidden_board[row][col] == "H":
        print(B_RED + " "*8 + "---Shot already taken in this location, fire again!---" + RESET)
    else:
        print(B_RED + " "*8 + "---Could not check if shot hit.---" + RESET)
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
        print(B_RED + " "*8 + "---Ship hit not in dictionary.---" + RESET)


def check_sunk(symbol):
    for name, attributes in player_ships.items():
        if attributes['symbol'] == symbol and attributes['hits_to_sink'] == 0:
            attributes['is_sunk'] = True


# Start of game, place ships on board
def start_place_ships(public_board, hidden_board, is_ai):
    if not is_ai:
        print(B_YELLOW + "Ships to launch: " + RESET)
        for ship_name, attributes in player_ships.items():
            if not attributes['is_placed']:
                print(ship_name)

        ship_in = input(B_YELLOW + "Ship to deploy: " + RESET)
        row_in = input(B_YELLOW + "Deployment row (0-9): " + RESET)
        col_in = input(B_YELLOW + "Deployment column (0-9): " + RESET)
        orientation_in = input(B_YELLOW + "Deployment orientation (horizontal or vertical): " + RESET)

        # Place ships on board and print board to user
        place_ships(public_board, hidden_board, ship_in, row_in, col_in, orientation_in, False)
    elif is_ai:
        unplaced = [ship_name for ship_name, attributes in ai_ships.items() if not attributes['is_placed']]

        if unplaced:
            random_ship = random.choice(unplaced)
            rand_row = random.randint(0, 9)
            rand_col = random.randint(0, 9)
            rand_orient = random.choice(["vertical", "horizontal"])

            place_ships(public_board, hidden_board, random_ship, rand_row, rand_col, rand_orient, True)

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
        print(RED + " "*8 + "---Coordinate values must be integers from 0-9!---" + RESET)
        return False

    if (orientation == "vertical" and row + length > num_rows)\
            or (orientation == "horizontal" and col + length > num_cols):
        print(RED + " "*8 + "---Input coordinates are out of ship placement bounds.---" + RESET)
        return False

    if orientation == "vertical" or orientation == "horizontal":
        return True
    else:
        print(RED + " "*8 + "---Unrecognised orientation type, "
                            "only 'horizontal' or 'vertical' allowed (case sensitive)---" + RESET)
        return False


# Check if valid ship
def process_ship_validity(ship_type, is_ai):
    if is_ai:
        if ship_type not in ai_ships:
            return False
    elif not is_ai:
        if ship_type not in player_ships:
            print(RED + " "*8 + "Invalid ship type detected, please use one from the (case sensitive) list!" + RESET)
            return False

    return True


# Place ships on your board
def place_ships(game_board, hidden_board, ship_type, row, col, orientation, is_ai):

    row, col = to_int(row, col)
    can_place = True

    # Is the input one in the list?
    if process_ship_validity(ship_type, is_ai):
        if is_ai:
            which_ships = ai_ships
            ship_length = which_ships[ship_type]['length']
        else:
            which_ships = player_ships
            ship_length = which_ships[ship_type]['length']

        # Is the input location and orientation legal
        if process_location(row, col, ship_length, orientation):
            # Is the ship already placed
            if ship_type in which_ships and not which_ships[ship_type]['is_placed']:
                symbol = which_ships[ship_type]['symbol']
                # Orientation then placement, checking for overlapped placements
                if orientation == "horizontal":
                    for i in range(ship_length):
                        if hidden_board[row][col + i] != "~":
                            can_place = False
                    for i in range(ship_length):
                        if can_place:
                            game_board[row][col + i] = BLUE + symbol + RESET
                            hidden_board[row][col + i] = symbol
                elif orientation == "vertical":
                    for i in range(ship_length):
                        if hidden_board[row + i][col] != "~":
                            can_place = False
                    for i in range(ship_length):
                        if can_place:
                            game_board[row + i][col] = BLUE + symbol + RESET
                            hidden_board[row + i][col] = symbol
                else:
                    if not is_ai:
                        print(RED +
                              " "*8 + "---Unrecognised orientation type, "
                                      "only 'horizontal' or 'vertical' allowed (case sensitive).---"
                              + RESET)
                # If the to-be-placed ship will overlap with another, deny placement, else allow
                if not can_place:
                    if not is_ai:
                        print(RED + " "*8 + "---A pre-existing ship is blocking this placement location.---" + RESET)
                else:
                    which_ships[ship_type]['is_placed'] = True
            else:
                if not is_ai:
                    print(RED + " "*8 + "---Ship type unrecognised, or ship is already placed.---" + RESET)
        else:
            if not is_ai:
                print(RED + " "*8 + "---Could not verify ship placement coordinate data"
                                    " (row, column, orientation).---" + RESET)
    else:
        if not is_ai:
            print(RED + " "*8 + "---Could not verify ship type.---" + RESET)


# Game loop
while not game_over:
    print_board()

    # Allow player to place ships
    if check_ships_placed(False) < len(player_ships):
        start_place_ships(player_board, player_hidden, False)
    elif check_ships_placed(False) == len(player_ships) and not player_placed:
        player_placed = True
        print(B_GREEN + " "*8 + "---Player ships placed!---" + RESET)

    # Randomly place AI ships
    if check_ships_placed(True) < len(ai_ships):
        start_place_ships(ai_board, ai_hidden, True)
    elif check_ships_placed(True) == len(ai_ships) and not ai_placed:
        ai_placed = True
        print(B_GREEN + " "*8 + "---AI ships placed!---" + RESET)

    if not win_check():
        user_turn = input("Step? ")
        fire(ai_board, ai_hidden)
    else:
        game_over = win_check()
    # Check if a hit, update game board

    # AI's turn
    # Implement AI logic to choose coordinates
    # Check if a hit, update game board

    # Check win condition

# Ask if the user wants to play again
