import numpy as np
import answer # generates 

# --- CONSTANTS ---
ANSWER = []

# --- FUNCTIONS ---
def evaluate_fitness(guess=[], real_answer=[]):
    """
    Takes in a word from the population, returns a normalized fitness number for the word.

    guess - a list of characters from the solution

    fitness - returns a float scoring how strong the guess is
    """
    # initialize fitness
    fitness = 0

    # for each char in the guess
    for c_index in range(len(guess)):
        if c_index <= len(real_answer): # ensures index never hits out of bounds
            # if the location lines up 1:1 with the answer, add 1 to fitness
            if guess[c_index] == real_answer[c_index]:
                fitness += 1
            # else if the char is in the word but wrong spot, add 0.5 to fitness
            elif guess[c_index] in real_answer: # BE ADVISED - YELLOWS MAY BE TAGGED INCORRECTLY DUE TO DUPLICATES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                fitness += 0.5
            # else add 0 to fitnes
        else:
            continue

    # normalize fitness result and return
    fitness = fitness/len(guess)

    return fitness

def main():
    """executes a full EA"""
    ANSWER = answer.initialize_answer() # returns a list of chars for our problem
    

main()