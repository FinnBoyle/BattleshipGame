# Finn Boyle, 18034590

# Define game board, place ships, and set up the AI
game_over = False

rows, cols = (10, 10)
player_board = [["~" for i in range(cols)] for j in range(rows)]
ai_board = [["~" for i in range(cols)] for j in range(rows)]

ships = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2
}

# Text formatting
ANSI_RESET = "\033[0m"
ANSI_BOLD_YELLOW = "\033[1;33m"
ANSI_BOLD_RED = "\033[1;31m"
ANSI_BLUE = "\033[34m"


# Print the boards of both the player and AI, side by side, one row at a time
def print_board():
    i = 0

    print(ANSI_BOLD_RED + "     Player's Board" + " "*15 + "AI's Board     " + ANSI_RESET)
    print(ANSI_BOLD_YELLOW + "  A B C D E F G H I J" + " "*9 + "A B C D E F G H I J" + ANSI_RESET)

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


# Fire a shot at the other player's board
def fire():
    pass


# Check if a shot hit
def check_if_hit():
    pass


# Place ships on your board
def place_ships(board, ship_type, row, col, orientation):
    ship_length = ships[ship_type]

    if ship_type == "Carrier":
        if orientation == "horizontal":
            for i in range(ship_length):
                board[row][col + i] = ANSI_BLUE + "A" + ANSI_RESET
        elif orientation == "vertical":
            for i in range(ship_length):
                board[row + i][col] = ANSI_BLUE + "A" + ANSI_RESET
        else:
            # Handle incorrect orientation input
            pass
    elif ship_type == "Battleship":
        if orientation == "horizontal":
            for i in range(ship_length):
                board[row][col + i] = ANSI_BLUE + "B" + ANSI_RESET
        elif orientation == "vertical":
            for i in range(ship_length):
                board[row + i][col] = ANSI_BLUE + "B" + ANSI_RESET
        else:
            # Handle incorrect orientation input
            pass
    elif ship_type == "Cruiser":
        if orientation == "horizontal":
            for i in range(ship_length):
                board[row][col + i] = ANSI_BLUE + "C" + ANSI_RESET
        elif orientation == "vertical":
            for i in range(ship_length):
                board[row + i][col] = ANSI_BLUE + "C" + ANSI_RESET
        else:
            # Handle incorrect orientation input
            pass
    elif ship_type == "Submarine":
        if orientation == "horizontal":
            for i in range(ship_length):
                board[row][col + i] = ANSI_BLUE + "S" + ANSI_RESET
        elif orientation == "vertical":
            for i in range(ship_length):
                board[row + i][col] = ANSI_BLUE + "S" + ANSI_RESET
        else:
            # Handle incorrect orientation input
            pass
    elif ship_type == "Destroyer":
        if orientation == "horizontal":
            for i in range(ship_length):
                board[row][col + i] = ANSI_BLUE + "D" + ANSI_RESET
        elif orientation == "vertical":
            for i in range(ship_length):
                board[row + i][col] = ANSI_BLUE + "S" + ANSI_RESET
        else:
            # Handle incorrect orientation input
            pass
    else:
        # Handle incorrect ship type input
        pass


# Game loop
while not game_over:
    print_board()
    board_in = input("Input board type: ")
    ship_in = input("input ship type: ")
    row_in = input("row: ")
    col_in = input("col: ")
    orientation_in = input("orientation: ")
    place_ships(player_board, ship_in, int(row_in), int(col_in), orientation_in)
    user_turn = input("Player enter coordinates to fire: ")

    # Check if a hit, update game board

    # AI's turn
    # Implement AI logic to choose coordinates
    # Check if a hit, update game board

    # Check win condition

# Ask if the user wants to play again
