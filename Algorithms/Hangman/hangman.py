import random
import string
from hangman_words import words, lives_visual_dict as hangman_dict

def get_valid_word(words): 
    # Randomly choose a word from list. Avoid words with spaces or dashes 
    word = random.choice(words)
    while '-' in word or ' ' in word:
            word = random.choice(words)
    return word.upper()

def hangman():
    word = get_valid_word(words)
    # Set of letters in the word 
    word_letters = set(word)
    alphabets = set(string.ascii_uppercase)
    # Set of letters that the user guessed 
    guessed_letters = set()
    # Initiate user's life value 
    lives = 7 

    # Allow player to guess if he has lives 
    while len(word_letters) > 0 and lives > 0: 
        print(str(hangman_dict[lives]))
        # Help player to keep track of what he has guessed so far 
        print('You have used these letters: ', ' '.join(guessed_letters))

        # Display letters in the word that was guessed correctly 
        word_list = [letter if letter in guessed_letters else '-' for letter in word]
        print('Current word: ', ' '.join(word_list))

        # Prompt user to input guess and display hangman 
        user_letter = input('Guess a letter: ').upper()
        
        # Check if letter has been guessed before 
        if user_letter in alphabets - guessed_letters:
            # Add letter to guessed_letter 
            guessed_letters.add(user_letter) 
            
            # Check if letter is in word. If so, remove letter from words_letters 
            if user_letter in word_letters: 
                word_letters.remove(user_letter)
            else: 
                lives -= 1 
                print('Letter is not in word. You have ' + str(lives) + ' lives remaining.')
        
        # If letter has been guessed before, allow player to try again 
        elif user_letter in guessed_letters: 
            print('You have already guessed that letter. Try another one.')
        
        # If user did not input a letter, allow player to try again 
        else: 
            print('Invalid input, try again. ')

    # If player is able to guess the word or player has no lives remaining 
    if lives == 0: 
        print(str(hangman_dict[lives]))
        print('Sorry, you died. The word was: ' + word)
    else:
        print('You got it! Congratulations!')



# Allow player to restart game when needed 
while True:
    answer = input('Do you want to play again? (Y/N): ')
    if answer.lower() == 'y' or answer.lower == 'yes':
        print('-----------------------------------')
        hangman()
    else:
        break
    