import random

print("-----HANGMAN GAME-----")
print("    --- RULES ---")
print("1) Display random words with missing letters on your screen")
print("2) You choose a letter")
print("3) Letters must be in lower case")

greet = input("Enter your name: ")
def hangman():
    print(f"\nWelcome to Hangman:{greet}")
    words = ["python", "java", "go", "css", "ruby", "html"]
    chose = random.choice(words)
    underline = ['_'] * len(chose)
    tries = 3   # maximum wrong tries
    print(f"Hidden word has {len(chose)} letters")
    print(' '.join(underline))
    print(f"You have {tries} tries\n")
    while '_' in underline and tries > 0:
        guess = input("Enter a letter: ").lower()
        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabet letter")
            continue
        # Check guess
        if guess in chose:
            for i, letter in enumerate(chose):
                if letter == guess and underline[i] == '_':
                    underline[i] = guess
                    break
            print("Good guess!")
        else:
            tries -= 1
            print(f"Wrong guess! Tries left: {tries}")
        print(' '.join(underline))
        print()
    if '_' not in underline:
        print(f"Congratulations! You guessed the word: {chose}")
    else:
        print(f"Game Over! The word was: {chose}")
hangman()
