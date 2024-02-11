from art import logo, vs
import random
from game_data import data
# from replit import clear # This is specific to Replit. If you're not using Replit, you might need an alternative method to clear the console.

def clear_screen():
    # This is a simple cross-platform way to clear the console, but it might not work in some environments.
    print("\033[H\033[J")

def get_follower_count(person):
    return person['follower_count']

def game():
    print(logo)
    score = 0

    while True:
        person_a = random.choice(data)
        person_b = random.choice(data)
        while person_a == person_b:
            person_b = random.choice(data)

        print(f"Compare A: {person_a['name']}, a {person_a['description']}, from {person_a['country']}.")
        print(vs)
        print(f"Against B: {person_b['name']}, a {person_b['description']}, from {person_b['country']}.")

        guess = input("Who has more followers? Type 'A' or 'B': ").lower()

        if guess == 'a':
            if get_follower_count(person_a) > get_follower_count(person_b):
                score += 1
                print(f"Correct! Your current score is {score}.")
                # clear()
                clear_screen()
            else:
                print(f"Wrong! Your final score is {score}.")
                break
        elif guess == 'b':
            if get_follower_count(person_b) > get_follower_count(person_a):
                score += 1
                print(f"Correct! Your current score is {score}.")
                # clear()
                clear_screen()
            else:
                print(f"Wrong! Your final score is {score}.")
                break
        else:
            print("Invalid input. Please type 'A' or 'B'.")

game()
