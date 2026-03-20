import numpy as np
import answer # generates an answer
import copy
import random
import nltk
nltk.download('words')
from nltk.corpus import words


# TODO
# running tests (post-brian edits)
# mutation doesnt work with guesses bigger than answer? Maybe itws letter type
# change mutation after yellow problem

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
    alpha = {
    1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 
    9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 
    16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 
    23: 'w', 24: 'x', 25: 'y', 26: 'z'}
    for i in range(len(individual)):
        individual[i] = alpha[individual[i]]
    return ''.join(individual) 

def letter_type(guessed_word):
    """
    Returns the color of the letter at the given index in the guessed word compared to the real answer.

    Args:
        guessed_word (list): A single individual representing a word

    Returns:
        str: The color of the letter at the given index
    """
    green_list = []
    yellow_list = []
    grey_list = []
    tmp_grey = []
    global ANSWER
    ans_copy = copy.deepcopy(ANSWER)
    idx = 0

    while len(ans_copy) > 0:
        if guessed_word[idx] == ans_copy[0]:
            green_list.append(idx)
        elif guessed_word[idx] in ans_copy:
            yellow_list.append(idx)
        else:
            # If the char is gray, add to a list that can be checked for longer guess yellows
            tmp_grey.append(idx)
            grey_list.append(idx)
        
        # remove the first character from the copy
        ans_copy.pop(0)
        idx += 1
    
    # add the remaining indices into the gray/yellow list?
    for i in range(idx, len(guessed_word)):
        if guessed_word[i] in tmp_grey:
            yellow_list.append(i)
        else:
            grey_list.append(i)
    
    return [green_list,yellow_list,grey_list]



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

    #Determines what kind of letter it is
    for c_index in range(len(individual)):
        if c_index <= len(ANSWER): # ensures index never hits out of bounds

            #Mutation_rate % of the time we mutate an individual gene
            if random.random() < mutation_rate:

                _, yellow_list, grey_list = letter_type(individual)

                swap_list = yellow_list + grey_list
                print(swap_list) # get list of yellows and greys
                
                swap = random.sample(swap_list,2)

                #swaps the two elements
                individual[swap[0]], individual[swap[1]] = individual[swap[1]], individual[swap[0]] 
                

    return individual



def main():
    """executes a full EA"""
    global ANSWER
    ANSWER = answer.initialize_answer() # returns a list of chars for our problem
    
    # initialize population
    population = initialize_population()

    word_found = False
    #while the stopping criteria has not been met
    while word_found == False:
        #evaluate fitness/parent selection

        #recombine/mutate

        #survivor selection        
        pass

    

main()

