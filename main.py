import random
import numpy as np
from problem import TTPInstance
from genotype import create_salesman_chromosome, crossover_salesman_chromosomes, mutate_salesman_chromosome
from genotype import create_knapsack_chromosome, crossover_knapsack_chromosomes, mutate_knapsack_chromosome
from phenotype import Solution

from deap import base, creator, tools, algorithms

number_of_generations = 10
number_of_individuals_in_population = 100
evaluation_parallel_population_sample = 10
gene_mutation_prob = 0.01
crossover_probability = 0.01

def evaluate_salesman(salesman_chromosome, knapsack_chromosomes_sample, problem_instance):
    
    pair_fitnesses = []

    for knapsack_chromosome in knapsack_chromosomes_sample:
        solution = Solution(salesman_chromosome, knapsack_chromosome, problem_instance)
        pair_fitnesses.append(solution.get_fitness())
    
    average_fitness = sum(pair_fitnesses) / len(pair_fitnesses)
    return average_fitness

def evaluate_knapsack(knapsack_chromosome, salesman_chromosomes_sample, problem_instance):
    
    pair_fitnesses = []

    for salesman_chromosome in salesman_chromosomes_sample:
        solution = Solution(salesman_chromosome, knapsack_chromosome, problem_instance)
        pair_fitnesses.append(solution.get_fitness())
    
    average_fitness = sum(pair_fitnesses) / len(pair_fitnesses)
    return average_fitness

import random

def evaluate_populations(salesman_population, knapsack_population, problem_instance):

    for individual in salesman_population:
        # Select a random sample from the knapsack population
        knapsack_sample = random.sample(knapsack_population, evaluation_parallel_population_sample)
        # Evaluate the salesman individual with the knapsack sample
        individual.fitness.values = evaluate_salesman(individual, knapsack_sample, problem_instance),

    for individual in knapsack_population:
        # Select a random sample from the salesman population
        salesman_sample = random.sample(salesman_population, evaluation_parallel_population_sample)
        # Evaluate the knapsack individual with the salesman sample
        individual.fitness.values = evaluate_knapsack(individual, salesman_sample, problem_instance),

def main():
    ttp_instance = TTPInstance.load_from_file('instances/a280_n279_bounded-strongly-corr_01.ttp')

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("SalesmanChromosome", np.ndarray, fitness=creator.FitnessMax)
    creator.create("KnapsackChromosome", np.ndarray, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    toolbox.register("salesman_chromosome", tools.initIterate, creator.SalesmanChromosome, lambda: create_salesman_chromosome(len(ttp_instance.cities)))
    toolbox.register("salesman_population", tools.initRepeat, list, toolbox.salesman_chromosome)

    toolbox.register("evaluate_salesman", evaluate_salesman, problem_instance=ttp_instance)
    toolbox.register("crossover_salesman_chromosomes", crossover_salesman_chromosomes)
    toolbox.register("mutate_salesman_chromosome", mutate_salesman_chromosome, gene_mutation_prob=gene_mutation_prob)
    toolbox.register("select_salesmen", tools.selTournament, tournsize = 3)

    toolbox.register("knapsack_chromosome", tools.initIterate, creator.KnapsackChromosome, lambda: create_knapsack_chromosome(len(ttp_instance.items)))
    toolbox.register("knapsack_population", tools.initRepeat, list, toolbox.knapsack_chromosome)

    toolbox.register("evaluate_knapsack", evaluate_knapsack, problem_instance=ttp_instance)
    toolbox.register("crossover_knapsack_chromosomes", crossover_knapsack_chromosomes)
    toolbox.register("mutate_knapsack_chromosome", mutate_knapsack_chromosome, gene_mutation_prob=gene_mutation_prob)
    toolbox.register("select_knapsacks", tools.selTournament, tournsize = 3)

    salesman_population = toolbox.salesman_population(number_of_individuals_in_population)
    knapsack_population = toolbox.knapsack_population(number_of_individuals_in_population)

    evaluate_populations(salesman_population, knapsack_population, ttp_instance)

    for g in range(number_of_generations):
        # Select the next generation individuals
        offspring_salesmen = toolbox.select_salesmen(salesman_population, len(salesman_population))
        offspring_salesmen = list(map(toolbox.clone, offspring_salesmen))

        offspring_knapsacks = toolbox.select_salesmen(knapsack_population, len(knapsack_population))
        offspring_knapsacks = list(map(toolbox.clone, offspring_knapsacks))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring_salesmen[::2], offspring_salesmen[1::2]):
            if random.random() < crossover_probability:
                child1, child2 = toolbox.crossover_salesman_chromosomes(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for child1, child2 in zip(offspring_knapsacks[::2], offspring_knapsacks[1::2]):
            if random.random() < crossover_probability:
                child1, child2 = toolbox.crossover_knapsack_chromosomes(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring_salesmen:
            toolbox.mutate_salesman_chromosome(mutant)
            del mutant.fitness.values

        for mutant in offspring_knapsacks:
            toolbox.mutate_knapsack_chromosome(mutant)
            del mutant.fitness.values

        # The population is entirely replaced by the offspring
        salesman_population[:] = offspring_salesmen
        knapsack_population[:] = offspring_knapsacks

if __name__ == "__main__":
    main()
