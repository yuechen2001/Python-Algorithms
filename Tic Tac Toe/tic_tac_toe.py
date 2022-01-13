#Tic Tac Toe game in python
from operator import truediv
from tokenize import Triple

# Initialise board 
board = [' ' for x in range(10)]

# Insert player's choice onto the board 
def insertLetter (letter, pos):
   board[pos] = letter 

# Check if space on the board is occupied 
def spaceIsFree (pos):
    return board[pos] == ' '

# Print the board onto terminal   
def printBoard (board):
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')

# Check every line whether the line contains only Xs or Os
def isWinner (board, letter):
    return ((board[7] == letter and board[8] == letter and board[9] == letter) or (board[4] == letter and board[5] == letter and board[6] == letter) or (board[1] == letter and board[2] == letter and board[3] == letter) or (board[7] == letter and board[4] == letter and board[1] == letter) or (board[8] == letter and board[5] == letter and board[2] == letter) or (board[9] == letter and board[6] == letter and board[3] == letter) or (board[7] == letter and board[5] == letter and board[3] == letter) or (board[9] == letter and board[5] == letter and board[1] == letter)) 

def playerMove () :
    turn = True 
    while turn: 
        move = input('Please select a position from 1-9 as your next move: ')

        # Check for valid input by player 
        try: 
            # Check if player entered an integer. If not an integer, ValueError will be raised 
            move = int(move)
            
            # Check if int is within range  
            if move > 0 and move < 10: 
                # Check if space is occupied
                if spaceIsFree(move): 
                    turn = False
                    insertLetter('X', move)
                else: 
                    print("That spot is already occupied, please try again.") 
            else: 
                print("Sorry, the number that you have entered is out of range.")
        except:
            print("Please enter a valid integer value.") 

def compMove () :
# Considerations for AI moves: 
# 1. Check for winning move 
# 2. Check if player can win the next time. If so, move to block player 
# 3. If 1 and 2 are false, occupy either corner, center or edge spaces (in that order)

    # Check for empty spaces on the board (except for when n = 0)
    possible_moves = [n for n, letter in enumerate(board) if letter == ' ' and n != 0]
    move = 0

    # In a copy of the board, first check if AI can win with this move. If so, return this move
    # Next, check if player can win on his next move. If so, block the player by playing into this space 
    for letter in ['O', 'X']:
        for i in possible_moves:
            boardCopy = board[:]
            boardCopy[i] = letter 
            if isWinner(boardCopy, letter): 
                move = i 
                return move 

    # Check for open corners 
    openCorners = []
    for i in possible_moves:
        if i in [1, 3, 7, 9]:
            openCorners.append(i)
    # If there are open corners, return random corner 
    if len(openCorners) > 0:
        move = selectRandom(openCorners)
        return move 

    # Check if centre is open. Return centre as move if so
    if 5 in possible_moves:
        move = 5 
        return move 

    # Check for open edges 
    openEdges = []
    for i in possible_moves:
        if i in [1, 3, 7, 9]:
            openEdges.append(i)
    # If there are open edges, return random edge
    if len(openEdges) > 0:
        move = selectRandom(openEdges)
        return move 
    
    # If no possible space found, return move as 0 
    return move 

def selectRandom(moves) :
   import random 
   length = len(moves)
   i = random.randrange(0, length)
   return moves[i] 

def isBoardFull (board) :
    if board.count(' ') > 1:
        return False
    else: 
        return True 

def main ():
    # Initialise welcome message 
    print("Welcome to Tic-Tac-Toe!")
    printBoard(board)

    while not isBoardFull(board):
        # Check if AI won. If not, allow player to make move 
        if not isWinner(board, 'O'):
            playerMove()
            printBoard(board)
        else:
            print("You lost, try again!")
            break 

        # Check if player won. If not, allow AI to make move 
        if not isWinner(board, 'X'):
            move = compMove()

            # If AI is unable to come up with a move, announce tie game 
            if move == 0: 
                print("Tie Game.")
            else: 
                insertLetter('O', move)
                print("Computer has made its move, your turn!")
                printBoard(board)
        else:
            print("Good job, you win!")
            break 

    if isBoardFull(board):
        print("Tie Game.")
   
# Allow player to restart game
while True:
    answer = input('Do you want to play again? (Y/N)')
    if answer.lower() == 'y' or answer.lower == 'yes':
        board = [' ' for x in range(10)]
        print('-----------------------------------')
        main()
    else:
        break