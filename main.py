



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







