# 455-k-wordle
**
Evolutionary Algorithm Design: Word Optimization**

This project implements an Evolutionary Algorithm (EA) designed to "evolve" a target word through stochastic optimization, mimicking the process of natural selection.
1. Representation

    Genotype: An integer array of length L, where each element ∈{1,…,26}, representing a randomized sequence of alphabetical indices.

    Phenotype: The decoded string (word guess) mapped from the genotypic integer array.

2. Fitness Evaluation

The fitness function measures the fitness of a single individual by the number of letters that are correct and also in the correct location. Fitness for corect letters that aren't in the right location
should also be encorporated.

3. Variation Operators

We employ a mix of mutation and recombination to maintain genetic diversity while converging on a solution.

Mutation

    Creep Mutation: Small incremental changes to the integer values to explore neighboring letters.

    Random Resetting: Replacing a value with a completely random index (1-26) to prevent local optima.

    Swap Mutation: If a "yellow" letter (correct letter, wrong spot) is identified, we may swap its position within the array.

Recombination (Crossover)

These are our two options that we can test and see which one works better.

    Uniform Crossover: Our primary operator, where each gene is chosen from either parent with equal probability.

    N-Point Crossover: An alternative method to be tested for maintaining contiguous "building blocks" of letters.

4. Selection & Population Management

    Parent Selection: Tournament Selection. This ensures high selection pressure by forcing individuals to compete in small groups, guaranteeing that the strongest candidates are consistently chosen for reproduction.

    Survivor Selection: Generational. The entire population is replaced by the offspring in each iteration to encourage rapid exploration of the search space. (comma notation)

5. Parameter Choices

Parameters such as population size, mutation rate, and tournament size are currently dynamic.

    These parameters will be tuned as the algorithm is developed depending on which one produces the best result
