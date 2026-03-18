import numpy as np
import answer # generates an answer
import copy

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
    for c_index, char in enumerate(guess):
        if c_index < len(real_answer): # ensures index never hits out of bounds
            # if the location lines up 1:1 with the answer, add 1 to fitness
            if char == real_answer[c_index]:
                fitness += 1
            # else if the char is in the word but wrong spot, add 0.5 to fitness
            elif char in real_answer: # BE ADVISED - YELLOWS MAY BE TAGGED INCORRECTLY DUE TO DUPLICATES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                fitness += 0.5
            # else add 0 to fitnes
        else:
            if char in real_answer:
                fitness += 0.5

    # normalize fitness result and return
    fitness = fitness/len(guess)

    return fitness

def tourney_selection(k=5, pop=[], answer=[]):
    """
    pick individuals as parents for the next generation. 
    For tournament, pick a small random subset (tournament) and the best one wins the right to reproduce

    k - size of each tournament
    pop - the full population we are selecting from
    answer - verifies fitness

    parent_list - a list of solutions that have clearence to be parents.
    """
    # initialize list of solutions with clearence to be parents
    parent_list = []
    pop_size = len(pop)
    target_size = pop_size // 2
    
    # while the list of parents isn't large enough, we continue tournaments
    while len(parent_list) < target_size:
        # a single loop will run ONE tournament
        # pick a subset from pop of size k
        p_indices = np.random.choice(len(pop), size=k, replace=False)
        t_participants = [pop[i] for i in p_indices]


        # add the one with the highest fitness to the parent list
        best_sol = None
        best_fit = -1

        for p in t_participants:
            new_fit = evaluate_fitness(p, answer)

            if new_fit > best_fit: # replace best recorded fitness
                best_sol = p
                best_fit = new_fit

        parent_list.append(best_sol)

    return parent_list

def main():
    """executes a full EA"""
    ANSWER = answer.initialize_answer() # returns a list of chars for our problem
    

main()