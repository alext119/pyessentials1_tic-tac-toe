# Tic-Tac-Toe

from random import randrange
from time import sleep

TURN_DELAY = 1.2 # Seconds
sleep_factor = TURN_DELAY / 3

PLAYER_SYMBOL = 'O'
CPU_SYMBOL    = 'X'

GREETING_TIE_FULL_BOARD = "No one.. Better luck next time, chums!"
GREETING_TIE_VICTORIES  = "Tie.. Not bad, not bad.."
GREETING_VICTORY_CPU    = "CPU.. Better luck next time!"
GREETING_VICTORY_PLAYER = "Player.. Congrats!"

BOARD_ROW_COL_SIZE = 3 # Some things break if this is made larger
                       # i.e., display_board() and CPU going in middle every time
BOARD_SIZE = BOARD_ROW_COL_SIZE ** 2
board_spaces = []
for i in range(BOARD_SIZE):
    board_spaces.insert(0, i + 1)
game_board = [[board_spaces.pop() for j in range(BOARD_ROW_COL_SIZE)] \
                                  for i in range(BOARD_ROW_COL_SIZE)]
spaces_taken = []

TERMINAL_ROW = '+-------' * BOARD_ROW_COL_SIZE + '+'
EMPTY_ROW    = '|       ' * BOARD_ROW_COL_SIZE + '|'
def display_board(board): # Required function definition
    # The function accepts one parameter containing the board's current status
    # and prints it out to the console.
    for i in range(BOARD_ROW_COL_SIZE):
        print(TERMINAL_ROW)
        print(EMPTY_ROW)
        
        player_row = ''
        for j in range(BOARD_ROW_COL_SIZE):
            player_row += '|   ' + str(board[i][j]) + '   '
        print(player_row + '|')

        print(EMPTY_ROW)
    print(TERMINAL_ROW)

def make_list_of_free_fields(board): # Required function definition
    # The function browses the board and builds a list of all the free squares; 
    # the list consists of tuples, while each tuple is a pair of row and column numbers.
    free_spaces = []
    for i in range(BOARD_ROW_COL_SIZE):
        for j in range(BOARD_ROW_COL_SIZE):
            space = board[i][j]
            if space != CPU_SYMBOL and space != PLAYER_SYMBOL:
                free_spaces.append(space)

    return free_spaces

def update_board(board, move, symbol, free_spaces):
    # Find exact spot on game board to place the player symbol
    found = False
    for i in range(BOARD_ROW_COL_SIZE):
        if found:
            break
        if move not in free_spaces:
            # Move recorded. Stop the board scan.
            break
        for j in range(BOARD_ROW_COL_SIZE):
            if move == board[i][j]:
                found = True
                board[i][j] = symbol
                free_spaces.remove(move)
                spaces_taken.append(move)
                break

def enter_move(board): # Required function definition
    # The function accepts the board's current status, asks the user about their move, 
    # checks the input, and updates the board according to the user's decision.
    free_spaces = make_list_of_free_fields(board)
    move = ''
    invalid = True
    while invalid:
        try:
            print()
            print("What's your move?", end=' ')
            move = int(input())
        except:
            print("Move invalid. Please enter a free number available on the board.")
            continue
        
        if move < 1 or move > BOARD_SIZE:
            print("Move outside game board size.. Please enter a valid move.")
            continue
        elif move not in free_spaces:
            print("That is not a free space.. Please enter a valid move.")
            continue
        # Move validated. It's good.
        invalid = False
    print("Player moves to the", move, "space.")
    update_board(board, move, PLAYER_SYMBOL, free_spaces)

def draw_move(board): # Required function definition
    # The function draws the computer's move and updates the board.
    free_spaces = make_list_of_free_fields(board)

    move = 0
    if len(spaces_taken) == 0:
        # CPU must take the middle space each and every time, seemingly
        move = 5
    else:
        while move not in free_spaces:       # Bad algorithm. Worse as choices decrease.
            move = randrange(BOARD_SIZE + 1) # Better if 'random' function could take a
                                         # list of possible choices as a parameter.
    print()
    print("CPU moves to the", move, "space.")
    update_board(board, move, CPU_SYMBOL, free_spaces)

def victory_for(board, sign): # Required function definition
    # The function analyzes the board's status in order to check if
    # the player using PLAYER_SYMBOL or CPU_SYMBOL has won the game
    
    # List containing the victory type(s), if any, which will get returned
    # If the list is empty, we know there were no victories achieved
    victories_achieved = []

    # Horizontal scan
    victories_achieved.append('horizontal') if board_scan_horizontal(board, sign) \
                                            else None

    # Vertical scan
    victories_achieved.append('vertical') if board_scan_vertical(board, sign) \
                                          else None

    # Diagonal (L -> R) scan
    victories_achieved.append('diagonal_lr') if board_scan_leftright_diagonal(board, sign) \
                                             else None

    # Diagonal (R -> L) scan
    victories_achieved.append('diagonal_rl') if board_scan_rightleft_diagonal(board, sign) \
                                             else None

    return victories_achieved

def board_scan_horizontal(board, sign):
    # If we get to the end of the row and
    # all spaces matched the relevant symbol, return True.
    # This is checked by comparing the iteration
    # count versus the row size (they should match).

    for i in range(BOARD_ROW_COL_SIZE):
        for j in range(BOARD_ROW_COL_SIZE):
            if board[i][j] != sign:
                break # No luck, check next row
            if j == BOARD_ROW_COL_SIZE - 1:
                return True # We have a winner

    return False # No winner so far...

def board_scan_vertical(board, sign):
    # If we get to the end of the column and
    # all spaces matched the relevant symbol, return True.
    # This is checked by comparing the iteration
    # count versus the column size (they should match).

    for i in range(BOARD_ROW_COL_SIZE):
        for j in range(BOARD_ROW_COL_SIZE):
            if board[j][i] != sign:
                break # No luck, check next column
            if j == BOARD_ROW_COL_SIZE - 1:
                return True # We have a winner

    return False # No winner so far...

def board_scan_leftright_diagonal(board, sign):
    # Diagonal (starting top-left, going to bottom-right)
    i = 0
    for j in range(BOARD_ROW_COL_SIZE):
        if board[i][j] != sign:
            break
        if j == BOARD_ROW_COL_SIZE - 1:
            return True # We have a winner
        i += 1

    return False # No winner so far...

def board_scan_rightleft_diagonal(board, sign):
    # Diagonal (starting top-right, going to bottom-left)
    i = BOARD_ROW_COL_SIZE - 1
    for j in range(BOARD_ROW_COL_SIZE):
        if board[j][i] != sign:
            break
        if j == BOARD_ROW_COL_SIZE - 1:
            return True # We have a winner
        i -= 1

    return False # No winner so far...

def start_game():
    print("TIC-TAC-TOE, let's go!")
    print("The board has", BOARD_ROW_COL_SIZE, "rows and columns..", end=' ')
    print("with", BOARD_SIZE, "spaces total.")
    display_board(game_board)
    print()
    print("CPU goes first.")

def end_game(victor):
    print("Game over!")
    print("The winner is", end='')
    for i in range(3):
        sleep(0.5)
        print(".", end='')
    print(" ", victor)
    for i in range(3):
        sleep(0.3)
        print(".")
    print("~ final board layout ~")
    display_board(game_board)

def game_loop():
    full_board = False
    cpu_victory = False
    cpu_victories = [] # Could make end greetings more interesting at some point
    player_victory = False
    player_victories = [] # Could make end greetings more interesting at some point

    while not full_board  and not cpu_victory and not player_victory:
        # Check for a full board (& recheck after CPU moves)
        if len(spaces_taken) == BOARD_SIZE: full_board = True
        if full_board: victor = GREETING_TIE_FULL_BOARD

        # CPU move first; AI will always have the upper hand... Muahahahaha....
        if not full_board:
            # Delay CPU turn to give illusion of thought
            for i in range(3):
                print('.')
                sleep(sleep_factor)
            draw_move(game_board)
            display_board(game_board)
            # Check for CPU victory
            cpu_victories = victory_for(game_board, CPU_SYMBOL)
            cpu_victory = True if len(cpu_victories) > 0 else False

            # One more full board check (repeated code from above)
            if len(spaces_taken) == BOARD_SIZE: full_board = True
            if full_board: victor = GREETING_TIE_FULL_BOARD

        # Player can go if the CPU didn't just win and there's still room to go
        if not cpu_victory and not full_board:
            enter_move(game_board) # Player decides their move
            display_board(game_board)
            # Check for Player victory
            player_victories = victory_for(game_board, PLAYER_SYMBOL)
            player_victory = True if len(player_victories) > 0 else False

    if cpu_victory or player_victory:
        if cpu_victory and player_victory:
            victor = GREETING_TIE_VICTORIES
        elif cpu_victory:
            victor = GREETING_VICTORY_CPU
        elif player_victory:
            victor = GREETING_VICTORY_PLAYER

    return victor

def main():
    start_game()

    victor = game_loop()

    end_game(victor)

main()
