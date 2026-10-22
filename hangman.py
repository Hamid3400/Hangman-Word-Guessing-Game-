import random

# --- 1. LOAD WORDS FROM FILE ---
def load_words(filename):
    """Reads words from a .txt file, filters them to 5-10 letters."""
    with open(filename, "r", encoding="utf-8") as f:
        all_words = [line.strip().lower() for line in f if line.strip()]
    # Only words 5-10 letters, all a-z
    filtered = [w for w in all_words if w.isalpha() and 5 <= len(w) <= 10]
    return filtered

# --- 2. SETUP ---
word_list = load_words("words.txt")
if not word_list:
    print("❌ Error: No valid words found in words.txt")
    exit()

hangman_art = [
    "🟢 (Attempt 1/6) - You are safe... for now.",
    "🟡 (Attempt 2/6) - The rope is tied.",
    "🟠 (Attempt 3/6) - The head is drawn.",
    "🟠 (Attempt 4/6) - The body is drawn.",
    "🔴 (Attempt 5/6) - One leg is drawn. Careful!",
    "🔴 (Attempt 6/6) - Second leg drawn. Next mistake is death!",
    "💀 GAME OVER - The stick figure is complete."
]

# --- 3. WORD MASK ---
def build_mask(word, guessed):
    return "".join((letter if letter in guessed else "_") + " " for letter in word)

# --- 4. PLAY ONE ROUND ---
def play_round():
    secret_word = random.choice(word_list)
    guessed_letters = set()
    wrong_guesses = 0
    max_attempts = 6

    # Fallback hint
    fallback = f"The word has {len(secret_word)} letters and starts with '{secret_word[0].upper()}'."

    print("\n" + "=" * 40)
    print("🎮 NEW ROUND 🎮")
    print("💡 Hint:", fallback)
    print("=" * 40)

    while wrong_guesses < max_attempts:
        print("\n" + hangman_art[min(wrong_guesses, max_attempts - 1)])
        print("Word:", build_mask(secret_word, guessed_letters))
        print("Guessed letters:", sorted(guessed_letters))
        print("-" * 40)

        if "_" not in build_mask(secret_word, guessed_letters):
            print(f"🎉 CONGRATULATIONS! You guessed '{secret_word}' in {wrong_guesses} wrong guess(es).")
            return

        guess = input("Guess a letter: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("❌ Please enter ONE letter (a-z).")
            continue

        if guess in guessed_letters:
            print("⚠️ You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("✅ Good guess!")
        else:
            print("❌ Wrong guess!")
            wrong_guesses += 1

    # Lost
    print(hangman_art[max_attempts - 1])
    print(f"💀 GAME OVER! The word was: {secret_word}")

# --- 5. MAIN LOOP (play again) ---
print("=" * 40)
print("🎮 WELCOME TO HANGMAN 🎮")
print("Rule: Guess letters one at a time.")
print("Win by revealing the whole word.")
print("Lose after 6 wrong guesses.")
print("=" * 40)

while True:
    play_round()
    again = input("\nPlay again? (y/n): ").strip().lower()
    if again != "y":
        print("Thanks for playing! 👋")
        break