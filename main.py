import copy
import os
import random
from typing import List
from deap import tools
import numpy
from problem import TTPInstance
from genotype import Chromosome, KnapsackChromosome, SalesmanChromosome
from phenotype import Solution
import matplotlib.pyplot as plt


number_of_generations = 30
number_of_individuals_in_population = 20
evaluation_parallel_population_sample = 5
tournament_size = 5
gene_mutation_prob = 0.5
crossover_probability = 0.9

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

def evaluate_populations(salesman_population: List[SalesmanChromosome], knapsack_population:List[KnapsackChromosome], problem_instance:TTPInstance):

    for individual in salesman_population:
        knapsack_sample = random.sample(knapsack_population, evaluation_parallel_population_sample)
        individual.set_fitness(evaluate_salesman(individual, knapsack_sample, problem_instance))

    for individual in knapsack_population:
        salesman_sample = random.sample(salesman_population, evaluation_parallel_population_sample)
        individual.set_fitness(evaluate_knapsack(individual, salesman_sample, problem_instance)),

def select(population: List[Chromosome]) -> List[Chromosome]:
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        best_individual = max(tournament, key=lambda x: x.fitness)
        selected.append(copy.copy(best_individual))
    return selected

def crossover_population(population: List[Chromosome], crossover_probability: float) -> List[Chromosome]:
    offsrping = []
    for child1, child2 in zip(population[::2], population[1::2]):
        if random.random() < crossover_probability:
            child1, child2 = child1.crossover(child2)
        offsrping.extend([child1, child2])
    return offsrping

def mutate_population(population: List[Chromosome], gene_mutation_probability: float) -> List[Chromosome]:
    for chromosome in population:
        chromosome.mutate(gene_mutation_probability)

    return population

def run_GA(ttp_instance: TTPInstance) -> None:

    logbook = tools.Logbook()

    ttp_stats = tools.Statistics(key=lambda ind: ind.get_fitness())
    ttp_stats.register("avg", numpy.mean)
    ttp_stats.register("std", numpy.std)
    ttp_stats.register("min", numpy.min)
    ttp_stats.register("max", numpy.max)

    salesman_population = [SalesmanChromosome.get_random(len(ttp_instance.cities)) for _ in range(number_of_individuals_in_population)]
    knapsack_population = [KnapsackChromosome.get_random(len(ttp_instance.items)) for _ in range(number_of_individuals_in_population)]

    evaluate_populations(salesman_population, knapsack_population, ttp_instance)

    for generation in range(number_of_generations):
        salesman_offspring = select(salesman_population)
        knapsack_offspring = select(knapsack_population)

        salesman_offspring = crossover_population(salesman_offspring, crossover_probability)
        knapsack_offspring = crossover_population(knapsack_offspring, crossover_probability)

        salesman_offspring = mutate_population(salesman_offspring, crossover_probability)
        knapsack_offspring = mutate_population(knapsack_offspring, crossover_probability)

        evaluate_populations(salesman_offspring, knapsack_offspring, ttp_instance)

        salesman_population[:] = salesman_offspring
        knapsack_population[:] = knapsack_offspring

        ttp_solutions = []
        for s in salesman_population:
            for k in knapsack_population:
                ttp_solutions.append(Solution(s,k,ttp_instance))


        ttp_record = ttp_stats.compile(ttp_solutions)

        print(f"Generation {generation + 1}:")
        print(ttp_record)
        logbook.record(gen=generation + 1, **ttp_record)

    return logbook

def main():

    for filename in os.listdir('instances'):
        if filename.endswith('.ttp'):
            ttp_instance = TTPInstance.load_from_file(os.path.join('instances', filename))
            for run in range(30):
                print(f"Running GA for {filename}, run {run+1}")
                run_GA(ttp_instance)

if __name__ == "__main__":
    main()
