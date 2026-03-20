import random
import numpy as np



#TODO: HOOK UP WITH BRETTS FITNESS FUNCTION
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

    local_population.sort(key=lambda x: calculate_fitness(x), reverse=True)

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


#TODO: Make sure to test this (and all of these more)
def n_point_crossover(parent1, parent2, n):
    """
    Performs n-point crossover on two integer arrays.
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



def letter_type(guessed_word, idx, real_answer):

    if idx < len(real_answer):
        if guessed_word[idx] == real_answer[idx]:
            return 'green'
        elif guessed_word[idx] in real_answer:
            return 'yellow'
        else:
            return 'gray'
    else:
        raise ValueError("Index out of Bounds")



print(letter_type(['c', 'h', 'e', 'a', 'x'], 7, ['c', 'h', 'e', 'a', 't']))





def mutate(individual, real_answer, mutation_rate=0.2):
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


    print(individual)
    return individual


