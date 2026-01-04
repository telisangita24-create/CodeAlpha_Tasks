import random

words = ["python", "coding", "intern", "program", "developer"]
secret_word = random.choice(words)

guessed_letters = []
incorrect_guesses = 0
max_attempts = 6

print(" Welcome to Hangman Game!")
print("_ " * len(secret_word))

while incorrect_guesses < max_attempts:
    guess = input("\nEnter a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter a single valid letter.")
        continue

    if guess in guessed_letters:
        print("You already guessed that letter.")
        continue

    guessed_letters.append(guess)

    if guess in secret_word:
        print(" Correct!")
    else:
        incorrect_guesses += 1
        print(f" Wrong! Attempts left: {max_attempts - incorrect_guesses}")

    current_word = ""
    for letter in secret_word:
        if letter in guessed_letters:
            current_word += letter + " "
        else:
            current_word += "_ "

    print(current_word.strip())

    if "_" not in current_word:
        print("\n Congratulations! You guessed the word:", secret_word)
        break

if incorrect_guesses == max_attempts:
    print("\n Game Over! The correct word was:", secret_word)