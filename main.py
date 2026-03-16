import random



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



print(uniform_crossover([1, 2, 3, 4], [5, 5, 5, 5, 5, 5]))




