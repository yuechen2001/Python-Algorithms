import random

moveset = ['scissors', 'paper', 'stone']
player_score = 0 
computer_score = 0

# AI to choose a random move 
def compMove(): 
    move = random.choice(moveset)
    return move 

# Player to input a move
def playerMove(): 
    turn = True 

    # Prompt player to enter his choice and check for valid input 
    while turn:
        move = input('Please select your next move: ').lower()
        if move != 'scissors' and move != 'paper' and move != 'stone':
            print('Invalid input. Please try again!')
        else:
            turn = False
            return move 
    
# Check who won the round
def isWinner(player, computer):
    if player == 'scissors' and computer == 'stone':
        return 'computer'
    if player == 'paper' and computer == 'scissors':
        return 'computer'
    if player == 'stone' and computer == 'paper':
        return 'computer'
    if player == 'scissors' and computer == 'paper':
        return 'player'
    if player == 'paper' and computer == 'stone':
        return 'player'
    if player == 'stone' and computer == 'scissors':
        return 'player'    
    else: 
        return None 

# Returns player score against computer score 
def displayScore(player, computer):
    score = str('{}-{}'.format(player, computer))
    return score

# Check if game is still ongoing
def isGameOver(): 
    if player_score == 3 or computer_score == 3:
        return True 
    else:
        return False

def main():
    # Welcome player to the game and initialise score
    global player_score, computer_score
    name = input('Please enter your name: ').capitalize()
    print('Welcome ' + name + '!')

    while not isGameOver():
        player_choice = playerMove()
        computer_choice = compMove()
        round_winner = isWinner(player_choice, computer_choice)

        # Award points according to who won the round 
        if round_winner == 'computer': 
            computer_score += 1 
            print('Computer wins! The score now is: ' + displayScore(player_score, computer_score))
        elif round_winner == 'player':
            player_score += 1
            print('Player wins! The score now is: ' + displayScore(player_score, computer_score))
        else: 
            print('Tie! The score now is: ' + displayScore(player_score, computer_score))
    
    # When game ends, announce the winner 
    if computer_score == 3: 
        print('Sorry, you lost! Try again next time!')
    else: 
        print('You have won! Congratulations!')

# Allow player to restart the game 
while True:
    answer = input('Do you want to play the game? (Y/N): ')
    if answer.lower() == 'y' or answer.lower() == 'yes':
        print('-----------------------------------')
        
        # Reset score
        player_score = 0 
        computer_score = 0
        main()
    else:
        break 