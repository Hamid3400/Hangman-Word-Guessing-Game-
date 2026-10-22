# 1. Import the random module
import random

# 2. Create a list of words
# A list is just a collection of items inside square brackets []
word_list = ["python", "computer", "internship", "developer", "keyboard", "hangman", "software"]

# 3. Make the computer pick one random word from the list
secret_word = random.choice(word_list)

# 4. Print it just to test that it works! 
# (We will hide this from the player later)
print("The secret word is:", secret_word)