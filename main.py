import numpy as np
import answer # generates an answer
import copy
import random


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


#TEMPORARY?????
def letter_type(guessed_word, idx, real_answer):
    """
    Returns the color of the letter at the given index in the guessed word compared to the real answer.

    Args:
        guessed_word (list): A single individual representing a word
        idx (int): The index of the letter to check
        real_answer (list): The correct answer to compare against

    Returns:
        str: The color of the letter at the given index
    """

    if idx < len(real_answer):
        if guessed_word[idx] == real_answer[idx]:
            return 'green'
        elif guessed_word[idx] in real_answer:
            return 'yellow'
        else:
            return 'gray'
    else:
        raise ValueError("Index out of Bounds")








def mutate(individual, real_answer, mutation_rate=0.2):
    """
    Performs mutation on an individual by mutating each gene with a mutation_rate% chance. 
    If the letter is a Green Letter we don't mutate, if Yelllow we swap mutate, if the letter
    is gray we random reset

    Args:
        individual (list): A single individual representing a word
        real_answer (list): The correct answer to compare against
        mutation_rate (float): A float between 0 and 1 determning chance of a gene being
        mutated

    Returns:
        individual (list): the new mutated individual
    """


    #Determines what kind of letter it is
    for c_index in range(len(individual)):
        if c_index <= len(real_answer): # ensures index never hits out of bounds

            #Mutation_rate % of the time we mutate an individual gene
            if random.random() < mutation_rate:

                letter_color = letter_type(individual, c_index, real_answer)

                print(letter_color)

                #Skip Green Letters
                if letter_color == 'green':
                    print("Green Letter, Nothing")
                    continue

                #Swap mutation the yellows
                #TODO: Make this actually not swap with green letters
                elif letter_color == 'yellow': 

                    print("Yellow Letter, Swap Mutation, but not with other greens")

                    random_idx = random.randrange(len(individual))

                    # Swap this element with a random one in the arr
                    individual[c_index], individual[random_idx] = individual[random_idx], individual[c_index]
                

                #Do random resetting
                else:
                    print("Gray Letter, Random Reset Mutation")
                    new_letter = np.random.randint(1,26)

                    individual[c_index] = new_letter

    return individual



def main():
    """executes a full EA"""
    ANSWER = answer.initialize_answer() # returns a list of chars for our problem
    

main()

