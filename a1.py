"""
Wordle
Assignment 1
Semester 1, 2022
CSSE1001
"""

from string import ascii_lowercase
from typing import Optional

from a1_support import (
    load_words,
    choose_word,
    VOCAB_FILE,
    ANSWERS_FILE,
    CORRECT,
    MISPLACED,
    INCORRECT,
    UNSEEN,
)

# Author Details
__author__ = "Muhammad Khan, 47511921"
__email__ = "m.khan2@uqconnect.edu.au"


# Functions
def has_won(guess: str, answer: str) -> bool:
    """
    Function to test whether a user has won, that is if the guess and answer match exactly.

    Args:
        guess(str): User input, a 6 letter word.
        answer(str): The correct word, chosen at random.

    Returns:
        Boolean True or False to confirm if the user has won.
    """
    if guess == answer:
        return True
    else:
        return False


def has_lost(guess_number: int) -> bool:
    """
    Function to test whether the user has lost, that is 6 guesses have been used up and the user has not won.

    Args:
        guess_number(int): How many guesses have already been used, takes value between 0 and 6.

    Returns:
        Boolean True or False to confirm if the user has lost.
    """
    if guess_number >= 6:
        return True
    else:
        return False


def remove_word(answer_words: tuple[str, ...], word: str) -> tuple[str, ...]:
    """
    Function to remove a specific word from a large tuple of words. Does this by concatenating two tuples, one from the
    start to the word, and the other for the rest.

    Args:
        answer_words(tuple): Tuple containing strings of all words.
        word(str): Word to be removed from the provided tuple.

    Returns:
        new_answer_words(tuple): A new tuple with the word removed.

    Could have turned tuple to list and then deleted element from list but this came to mind first.
    """
    word_index = answer_words.index(word)
    new_answer_words = answer_words[:word_index] + answer_words[word_index + 1:]
    return new_answer_words


def prompt_user(guess_number: int, words: tuple[str, ...]) -> str:
    """
    Function to continuously ask the user for a 6-letter word until a valid word is entered. If there is a problem with
    users entry, it briefly describes what the problem was. Also accepts the valid keys 'q', 'k' and 'h'.

    Args:
        guess_number(int): Guess number to display what guess the user is currently on.
        words(str):  A large tuple, containing all valid words.

    Returns:
        guess(str): The valid guess user has entered.
    """
    guess = input(f"Enter guess {guess_number}: ").lower()
    while guess not in words:
        if guess == "q":
            return 'q'
        elif guess == "h":
            return 'h'
        elif guess == "k":
            return 'k'
        elif len(guess) != 6:
            print("Invalid! Guess must be of length 6")
            guess = input(f"Enter guess {guess_number}: ").lower()
        elif len(guess) == 6:
            print("Invalid! Unknown word")
            guess = input(f"Enter guess {guess_number}: ").lower()
        else:
            print("Invalid! Unknown error")
            guess = input(f"Enter guess {guess_number}: ").lower()
    return guess


def process_guess(guess: str, answer: str) -> str:
    """
    Function to work on user's input, and assign specific letters in input to corresponding boxes, which display if it
    is correct, incorrect or misplaced.

    Args:
        guess(str): User's input, valid 6 letter word.
        answer(str): Answer, random word chosen at beginning of game.

    Returns:
        correct_string(str): A string containing coloured boxes which correspond to correct, misplaced or incorrect, in
                            the respective position of the letter in the word. Double letter words have special rules.
    """
    correct = [0, 1, 2, 3, 4, 5]
    for i in range(0, 6):
        if guess[i] == answer[i]:
            correct[i] = CORRECT
            for q in range(0, 6):  # checks for any other occurrence of the letter to mark as incorrect
                if q != i:
                    if guess[q] == guess[i]:
                        correct[q] = INCORRECT

        else:
            if (guess[i] in answer) and (guess[i] not in guess[:i]):  # only takes first occurrence
                correct[i] = MISPLACED
            else:
                correct[i] = INCORRECT
    correct = ''.join(correct)
    return correct


def update_history(history: tuple[tuple[str, str], ...], guess: str, answer: str) -> tuple[tuple[str, str], ...]:
    """
    Function to update the list of former guesses and box strings.

    Args:
        history(tuple): Tuple containing tuples of previous guesses and respective box strings.
        guess(str): Previous guess (user input).
        answer(str): Correct word to be guessed.

    Returns:
        history: Updated version of arg history, appended to add the last guess and box string.

    """
    history = history + ((guess, process_guess(guess, answer)),)
    return history


def print_history(history: tuple[tuple[str, str], ...]) -> None:
    """
    Function to print the history from previous function in a user-friendly way.

    Args:
        history(tuple): Tuple containing tuples of previous guesses and respective box strings.

    Returns:
        Print text to show the history.

    """
    guess_number = 1
    print(15 * "-")
    for (i) in history:
        print("Guess " + str(guess_number) + ":  " + (" ".join(i[0])))
        print(9 * " " + i[1])
        print(15 * "-")
        guess_number += 1
    print()


def print_keyboard(history: tuple[tuple[str, str], ...]) -> None:
    """
    Function that prints the keyboard in a user-friendly way with the information currently known about each letter.

    Args:
        history(tuple): Tuple containing tuples of previous guesses and respective box strings.

    Returns:
        Print text to show each letter and the information currently known about it.

    """
    correct_letters = []
    misplaced_letters = []
    incorrect_letters = []
    keyboard = {i: UNSEEN for i in ascii_lowercase}

    print('\nKeyboard information\n------------')
    for i in history:
        count = 0
        while count < 7:
            if ((i[1])[count]) == CORRECT:
                correct_letters.append((i[0])[count])
            elif ((i[1])[count]) == MISPLACED:
                misplaced_letters.append((i[0])[count])
            elif ((i[1])[count]) == INCORRECT:
                incorrect_letters.append((i[0])[count])
            count += 1
            if count == 6:
                break

    for i in keyboard:
        if str(i) in correct_letters:
            (keyboard[i]) = CORRECT
        elif str(i) in misplaced_letters:
            (keyboard[i]) = MISPLACED
        elif str(i) in incorrect_letters:
            (keyboard[i]) = INCORRECT
    keys = list(keyboard.keys())
    values = list(keyboard.values())
    count = 0

    while count < 27:
        print(f'{keys[count]}: {values[count]}\t{keys[count + 1]}: {values[count + 1]}')
        count += 2
        if count == 26:
            print()
            break


def print_stats(stats: tuple[int, ...]) -> None:
    """
    Function to show the number of wins and losses and guess used in previous games.

    Args:
        stats(tuple): Tuple containing the number of games won with number of guesses and number of losses.

    Returns:
        Print text to show the stats in user-friendly way.

    """
    print("\nGames won in:")
    for i in range(1, 7):
        print(i, 'moves:', stats[i - 1])
    print("Games lost:", stats[6])


def main():
    """
    Main function to run all code. Implements all other function to make the game seamless.

    No args, as all args are defined for different functions.

    No return, just implements the game until user quits.
    """
    all_words = load_words(VOCAB_FILE)
    answer_words = load_words(ANSWERS_FILE)
    stats = (0, 0, 0, 0, 0, 0, 0, 0)

    while True:
        answer = choose_word(answer_words)
        guess_number = 1
        history = ()

        while guess_number < 7:
            guess = (prompt_user(guess_number, all_words)).lower()

            if guess == 'q':
                return None

            elif guess == 'k':
                print_keyboard(history)

            elif guess == 'h':
                print('Ah, you need help? Kill yourself nigger.')

            else:
                history = update_history(history, guess, answer)
                print_history(history)

                if has_won(guess, answer) is True:
                    print(f'Correct! You won in {guess_number} guesses!')
                    stats_list = list(stats)
                    stats_list[guess_number - 1] += 1
                    stats = tuple(stats_list)
                    print_stats(stats)
                    play_again = input('Would you like to play again (y/n)? ')
                    while True:
                        if play_again == 'y' or play_again == 'Y':
                            answer_words = remove_word(answer_words, answer)
                            break
                        elif play_again == 'n' or play_again == 'N':
                            return None
                        else:
                            print("Sorry, please enter y or n.")
                            play_again = input('Would you like to play again (y/n)? ')
                    break

                if has_lost(guess_number) is True:
                    print(f'You lose! The answer was: {answer}')
                    stats_list = list(stats)
                    stats_list[6] += 1
                    stats = tuple(stats_list)
                    print_stats(stats)
                    play_again = input('Would you like to play again (y/n)? ')
                    while True:
                        if play_again == 'y' or play_again == 'Y':
                            answer_words = (answer_words, answer)
                            break
                        elif play_again == 'n' or play_again == 'N':
                            return None
                        else:
                            print("Sorry, please enter y or n.")
                            play_again = input('Would you like to play again (y/n)? ')
                    break

                guess_number += 1


if __name__ == "__main__":
    main()
