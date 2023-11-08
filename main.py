import random
import numpy as np
from problem import TTPInstance
from genotype import create_salesman_chromosome, crossover_salesman_chromosomes, mutate_salesman_chromosome
from genotype import create_knapsack_chromosome, crossover_knapsack_chromosomes, mutate_knapsack_chromosome
from phenotype import Solution

from deap import base, creator, tools, algorithms

NUM_SPECIES = 2 

number_of_generations = 10
number_of_individuals_in_population = 10

def evaluate_salesman(salesman_chromosome, knapsack_chromosomes_sample, problem_instance):
    
    pair_fitnesses = []

    for knapsack_chromosome in knapsack_chromosomes_sample:
        solution = Solution(salesman_chromosome, knapsack_chromosome, problem_instance)
        pair_fitnesses.append(solution.get_fitness())
    
    average_fitness = sum(pair_fitnesses) / len(pair_fitnesses)
    return average_fitness

def main():
    ttp_instance = TTPInstance.load_from_file('instances/a280_n279_bounded-strongly-corr_01.ttp')

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("SalesmanChromosome", np.ndarray, fitness=creator.FitnessMax)
    creator.create("KnapsackChromosome", np.ndarray, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("salesman_chromosome", tools.initIterate, creator.SalesmanChromosome, lambda: create_salesman_chromosome(len(ttp_instance.cities)))
    toolbox.register("salesman_population", tools.initRepeat, list, toolbox.salesman_chromosome)

    toolbox.register("knapsack_chromosome", tools.initIterate, creator.KnapsackChromosome, lambda: create_knapsack_chromosome(len(ttp_instance.items)))
    toolbox.register("knapsack_population", tools.initRepeat, list, toolbox.knapsack_chromosome)

    initial_salesman_population = toolbox.salesman_population(number_of_individuals_in_population)
    initial_knapsack_population = toolbox.knapsack_population(number_of_individuals_in_population)

    print(initial_salesman_population)
    print(initial_knapsack_population)

    test = initial_salesman_population[0]
    print(evaluate_salesman(test, initial_knapsack_population, ttp_instance))

if __name__ == "__main__":
    main()
