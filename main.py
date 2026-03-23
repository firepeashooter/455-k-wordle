import numpy as np
import answer # generates an answer
import random
import string
import copy
import nltk
nltk.download('words')
from nltk.corpus import words

# --- CONSTANTS ---
ANSWER = []

# --- FUNCTIONS ---
def evaluate_fitness(guess=[]):
    """
    Takes in a word from the population, returns a normalized fitness number for the word.
    
    Args:
        guess - a list of characters from the solution

    Returns:
        fitness - returns a float scoring how strong the guess is
    """
    # initialize fitness
    fitness = 0
    global ANSWER

    # for each char in the guess
    green, yellow, _ = letter_type(guess)

    # calculate the fitness of each letter
    fitness = len(green) + len(yellow)*0.5

    # normalize fitness result and return
    fitness = fitness/len(guess)

    return fitness

def tourney_selection(k=5, pop=[]):
    """
    pick individuals as parents for the next generation. 
    For tournament, pick a small random subset (tournament) and the best one wins the right to reproduce

    Args:
        k - size of each tournament
        pop - the full population we are selecting from

    Returns:
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
            new_fit = evaluate_fitness(p)

            if new_fit > best_fit: # replace best recorded fitness
                best_sol = p
                best_fit = new_fit

        parent_list.append(best_sol)

    return parent_list



def generational_selection(population, offspring, k):
    """
    Performs Generational Survivor Selection with elitism, by replacing the population  
    with the best k individuals and filling the rest with the offspring

    Args:
        population (list): A list of Candidate objects.
        offspring (list): A list of offspring generated this generation

    Returns:
        new_population (list): The individual with the highest fitness score.
    """

    #Pick the top k individuals to move onto the next state

    #Sort the population by fitness
    local_population = population.copy()

    local_population.sort(key=lambda x: evaluate_fitness(x), reverse=True)

    elites = local_population[:k]

    new_population = elites + offspring

    return new_population




def uniform_crossover(parent1, parent2):
    """
    Performs uniform crossover on two parents to create two offspring

    Args:
        parent1 (list): A single individual representing a word
        parent2 (list): A single individual representing a word

    Returns:
        offspring (list): A list of two individuals that represent the offspring
    """

    offspring1 = []
    offspring2 = []


    #TODO: How do we decide the length of the offspring? Are they both the same?
    #      Do we want them to match the parent length?

    #Right now the length of the offspring = the length of the smallest parent

    offspring_size = min(len(parent1), len(parent2))

    for i in range(offspring_size):

        #With probability 0.5 take from parent 1 or parent 2, other child gets the other one
        if random.random() < 0.5:
            offspring1.append(parent1[i])
            offspring2.append(parent2[i])
        else:
            offspring1.append(parent2[i])
            offspring2.append(parent1[i])

    return [offspring1, offspring2]



def n_point_crossover(parent1, parent2, n):
    """
    Performs n-point crossover on two integer arrays.

    Args:
        parent1 (list): A single individual representing a word
        parent2 (list): A single individual representing a word
        n (int): The number of crossover points

    Returns:
        offspring (list): A list of two individuals that represent the offspring
    """

    min_len = min(len(parent1), len(parent2))
    #If the shorter parent is too small for n points,we cap n to avoid an error.
    n = min(n, min_len - 1)
    
    #Pick and sort n random split points
    points = sorted(random.sample(range(1, min_len), n))
    #Add the start and end indices to make looping easier just like that example in class
    points = [0] + points + [min_len]
    
    offspring1 = []
    offspring2 = []
    
    #Alternate segments
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i+1]
        
        #Every other segment, we swap which parent goes to which child
        if i % 2 == 0:
            offspring1.extend(parent1[start:end])
            offspring2.extend(parent2[start:end])
        else:
            offspring1.extend(parent2[start:end])
            offspring2.extend(parent1[start:end])
            
    #Make it so that the child 1 is as long as child 2 and vice versa
    if len(parent1) > len(parent2):
        offspring1.extend(parent1[min_len:])
    elif len(parent2) > len(parent1):
        offspring2.extend(parent2[min_len:])
        
    return [offspring1, offspring2]

def create_individual():
    """
    Creates a random individual for the population

    Returns:
        individual - A list of characters representing a guess
    """
    global ANSWER
    word_length = len(ANSWER)
    full_word_list = words.words('en') 

    final_list = []
    for w in full_word_list:
        if len(w) == word_length:
            final_list.append(w)

    random_word = final_list[np.random.randint(0,len(final_list)-1)].lower()

    return [char for char in random_word]
  

def initialize_population(pop_size=100):
    """
    Initializes a population of random guesses

    Args:
        pop_size - The number of individuals in the population

    Returns:
        population - A list of individuals representing the population
    """
    population = []
    for i in range(pop_size):
        new_individual = create_individual()
        population.append(new_individual)
    
    return population

def to_phenotype(individual):
    """
    Converts a list of characters into a string 

    Args:
        individual - a list of characters representing a guess

    Returns:
        phenotype - a string representing the guess
        
    """
    #alpha = {
    #0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 
    #8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 
    #15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 
    #22: 'w', 23: 'x', 24: 'y', 25: 'z'}
    #for i in range(len(individual)):
        #individual[i] = alpha[i]
    return "".join(individual)

def letter_type(guessed_word):
    """
    Returns the color of the letter at the given index in the guessed word compared to the real answer.

    Args:
        guessed_word (list): A single individual representing a word

    Returns:
        green_list: A list of indices in a guess where greens are located
        yellow_list: A list of indices where there are yellow letters
        grey_list: A list where all grey letters are located
    """

    global ANSWER
    green_list = []
    yellow_list = []
    grey_list = []
    
    # to handle duplicate letters correctly.
    remaining_ans = list(ANSWER)
    
    # round 1: Find all Greens (Exact Matches)
    # do this first so a Green letter doesn't get 'stolen' by a Yellow check
    for i in range(min(len(guessed_word), len(ANSWER))):
        if guessed_word[i] == ANSWER[i]:
            green_list.append(i)
            # Mark this character as 'used' so it can't be a yellow for another letter
            # We use None to keep the indices aligned
            remaining_ans[i] = None 

    # round 2: Find Yellows and Greys
    for i in range(len(guessed_word)):
        if i in green_list:
            continue
            
        char = guessed_word[i]
        if char in remaining_ans:
            yellow_list.append(i)
            # Remove ONLY one instance of that character from the pool
            remaining_ans.remove(char)
        else:
            grey_list.append(i)
            
    return green_list, yellow_list, grey_list



def mutate(individual, mutation_rate=0.2):
    """
    Performs mutation on an individual by mutating each gene with a mutation_rate% chance. 
    If the letter is a Green Letter we don't mutate, if Yelllow we swap mutate, if the letter
    is gray we random reset

    Args:
        individual (list): A single individual representing a word
        mutation_rate (float): A float between 0 and 1 determning chance of a gene being
        mutated

    Returns:
        individual (list): the new mutated individual
    """
    global ANSWER

    # We use indices to avoid the "duplicate letter" confusion
    green_indices, yellow_indices, grey_indices = letter_type(individual)

    # iterate and apply mutations
    for c_index in range(len(individual)):
        if random.random() < mutation_rate:
            
            # Skip greens
            if c_index in green_indices:
                continue

            # random reset on grey
            elif c_index in grey_indices:
                individual[c_index] = random.choice(string.ascii_lowercase)

            # bit swap yellows with non-greens
            elif c_index in yellow_indices:
                # swap with any other Yellow or Gray index
                possible_swap_targets = yellow_indices + grey_indices
                # Remove current index so we don't "swap" with ourselves
                if c_index in possible_swap_targets:
                    possible_swap_targets.remove(c_index)
                
                if possible_swap_targets:
                    swap_with = random.choice(possible_swap_targets)
                    individual[c_index], individual[swap_with] = individual[swap_with], individual[c_index]

    return individual



def main():
    """executes a full EA"""
    global ANSWER
    #random word
    ANSWER = answer.initialize_answer() # returns a list of chars for our problem
    
    
    #hyperparameters
    POP_SIZE = 25
    MAX_GEN = 100
    MUTATION_RATE = 0.1
    TOURNEY_SIZE = 4
    ELITISM_FACTOR = 3
    TEST_WORD_LIST = [['r','a','t','e'],['m','u','t','a','t','e','s'],['p','o','p','u','l','a','t','i','o','n']]
    N_POINT_FACTOR = 3

    #UNCOMMENT IF TESTING (change index for word)
    #ANSWER = TEST_WORD_LIST[0]

    # initialize population
    population = initialize_population(pop_size=POP_SIZE)

    
    #while the stopping criteria has not been met
    for gen in range(MAX_GEN):
        #evaluate fitness/parent selection
        population.sort(key=lambda ind: evaluate_fitness(ind), reverse=True)

        best_individual = population[0]
        best_score = evaluate_fitness(best_individual)

        print("Winning individual in generation " + str(gen) + ": " + to_phenotype(best_individual) + " with a score of " + str(best_score))

        #if we have reached the answer then break the loop
        if best_individual == ANSWER:
            print("---- ANSWER FOUND! ----")
            print(to_phenotype(ANSWER) + " was reached in " + str(gen) + " generations")
            break


        # parent selection
        parents = tourney_selection(k=TOURNEY_SIZE, pop=population)\
        
        offspring = [] #initialize the next gen

        while len(offspring) < POP_SIZE: #fill it up until all offspring are created
            parent1,parent2 = random.sample(parents,2)
            
            #try one or the other
            offspring1, offspring2 = uniform_crossover(parent1, parent2) #uniform crossover
            #offspring1, offspring2 = n_point_crossover(parent1, parent2, n=N_POINT_FACTOR)

            offspring.append(offspring1)
            offspring.append(offspring2)

        # we have all of the parents/children, now we survivor select
        new_population = generational_selection(population,offspring,ELITISM_FACTOR)

        # then we mutate (chance incorporated)
        for p in new_population:
            p = mutate(p, MUTATION_RATE)
        # iterate generations
        population = new_population

    


    

main()

