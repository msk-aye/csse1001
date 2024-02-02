def process_guess(guess: str, answer: str) -> str:
    correct_list = [0, 1, 2, 3, 4, 5]
    for i in range(0, 6):
        if guess[i] == answer[i]:
            correct_list[i] = 'Correct'
        else:
            for c in range(i,6):
                if guess[c] in answer:
                    correct_list[c] = 'misplaced'
                else:
                    correct_list[c] = 'wrong'

    return correct_list

def process_guess(guess: str, answer: str) -> str:
    correct_list = [0, 1, 2, 3, 4, 5]
    for i in range(0, 6):
        if guess[i] == answer[i]:
            correct_list[i] = 'Correct'
        else:
            for c in range(i,6):
                if (guess[c] in answer) and (guess[c] not in guess[:c]):
                    correct_list[c] = 'misplaced'
                else:
                    correct_list[c] = 'wrong'

    return correct_list
