import random
import os

'''Using ANSI colour codes to give colourful output.
Giving name to each code so we don't have to write code again and again.

Also defining global variable which we will use in the entire code.
Declaring everything at one place will make it easy to change it later.'''

GREEN = '\033[92m' 
YELLOW = '\033[93m'
RED = '\033[91m'
GRAY = '\033[90m' 
RESET = '\033[0m'
WORD_LENGTH = 5
MAX_ATTEMPTS = 6
WORD_LIST_FILE = 'words.txt'

'''Following function will load the word from the text file.
Split all the lines and will make the list.
Then the all the words are stripped(remove extra space) and lowered and are stored in a set to ensure there are no duplicates.

After the words are cleaned they are stored back in text file after sorting them.'''


def load_words():
    if not os.path.exists(WORD_LIST_FILE):
        print(f"Word dictionary not found")
        exit()
    else:
        with open(WORD_LIST_FILE, 'r') as f:
            words = f.read().splitlines()
        
        word_set = set(word.strip().lower() for word in words if len(word.strip()) == WORD_LENGTH)
        return word_set
    
def save_clean_words(word_set):
    with open(WORD_LIST_FILE, 'w') as f:
        for word in sorted(word_set):
            f.write(word + '\n')
    print(f"Cleaned word dictionary saved to {WORD_LIST_FILE}")

'''Function to choose random word from the set of words.'''

def choose_word(word_set):
    return random.choice(list(word_set))

'''Following function will validate the user guess.
If the length of the guess is not equal to the required length it will return false.
If the difficulty is hard and the word is not in the dictionary it will return false.
Then it will return true if all the conditions are satisfied.'''

def validate_guess(guess, word_set, difficulty = 'Hard'):
    if len(guess) != WORD_LENGTH:
        print(f"Guess must be {WORD_LENGTH} letters long.")
        return False
    if difficulty == 'Hard' and guess not in word_set:
        print("Word not in dictionary.")
        return False
    return True
    
'''Function to give feedback to the user.
It will compare the guess with the secret word and will return a list of feedback.
Green for correct letter and position, yellow for correct letter but wrong position, gray for wrong letter.'''

def get_feedback(secret, guess):
    feedback = ['gray'] * WORD_LENGTH
    secret_list = list(secret)
    guess_list = list(guess)

    # Step 1: Mark greens
    for i in range(WORD_LENGTH):
        if guess_list[i] == secret_list[i]:
            feedback[i] = 'green'
            secret_list[i] = None   # Remove matched letter
            guess_list[i] = None    # Mark as processed

    # Step 2: Mark yellows
    for i in range(WORD_LENGTH):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            feedback[i] = 'yellow'
            secret_list[secret_list.index(guess_list[i])] = None  # Remove used letter
    return feedback

'''Function to print feedback to the user.'''

def print_feedback(guess, feedback):
    colored_output = ''
    for i in range(WORD_LENGTH):
        if feedback[i] == 'green':
            colored_output += f"{GREEN}{guess[i]}{RESET}"
        elif feedback[i] == 'yellow':
            colored_output += f"{YELLOW}{guess[i]}{RESET}"
        else:
            colored_output += f"{GRAY}{guess[i]}{RESET}"
    print(colored_output)

'''This is the main game logic(loop) where the actual game will be played.'''

def play_game(word_set):
    print("\nChoose difficulty: (E)asy / (H)ard")
    diff_choice = input(">").lower()
    difficulty = 'easy' if diff_choice == 'e' else 'hard'

    secret_word = choose_word(word_set)
    attempts = 0
    hint_given = False

    while attempts < MAX_ATTEMPTS:
        guess = input(f"\nAttempt {attempts+1}/{MAX_ATTEMPTS}. Enter your {WORD_LENGTH}-letter guess: ").lower().strip()
        if not validate_guess(guess, word_set, difficulty):
            continue
        feedback = get_feedback(secret_word, guess)
        print_feedback(guess, feedback)
        attempts += 1
        if guess == secret_word:
            print(f"{GREEN}Congratulations! You've guessed the word '{secret_word}' correctly!{RESET}")
            break
        else:
            if attempts == 3 and not hint_given:
                hint_letter = random.choice([l for l in secret_word if l not in guess])
                print(f"{YELLOW}Hint: The secret word contains the letter '{hint_letter}'.{RESET}")
                hint_given = True
    else:
        print(f"{RED}Sorry, you've used all attempts. The secret word was '{GREEN}{secret_word}{RESET}'.")

'''Main function to start the game and handle replay logic.
The game will continue till user wants to play.
After each game user will be asked if they want to play again or not.'''

def main():
    word_set = load_words()
    save_clean_words(word_set)
    while True:
        play_game(word_set)
        replay = input("\nDo you want to play again? (Y/N): ").lower()
        if replay != 'y':
            print("Thank you for playing! Goodbye!")
            break

'''This will ensure that the main function is called only when this script is run directly.'''

if __name__ == "__main__":
    main()