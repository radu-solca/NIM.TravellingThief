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


number_of_generations = 100
number_of_individuals_in_population = 30
evaluation_parallel_population_sample = number_of_individuals_in_population
gene_mutation_probability = 0.1 
good_crossover_probability = 0.5
crossover_top = 80 
min_copy = int((number_of_individuals_in_population) * ( 5 / 100))  
max_copy = int((number_of_individuals_in_population) * ( 10 / 100))  

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

def evaluate_populations(salesman_population: List[SalesmanChromosome], knapsack_population:List[KnapsackChromosome], problem_instance:TTPInstance):

    for individual in salesman_population:
        knapsack_sample = random.sample(knapsack_population, evaluation_parallel_population_sample)
        individual.set_fitness(evaluate_salesman(individual, knapsack_sample, problem_instance))

    for individual in knapsack_population:
        salesman_sample = random.sample(salesman_population, evaluation_parallel_population_sample)
        individual.set_fitness(evaluate_knapsack(individual, salesman_sample, problem_instance)),



def select(population: List[Chromosome]) -> List[Chromosome]:
    return sorted(population, key=lambda x: x.fitness, reverse=True)



def crossover_population(population: List[Chromosome],good_crossover_probability: float, crossover_top: float) -> List[Chromosome]:
    copy_ind = random.randint(min_copy, max_copy)
    offsrping = population[:copy_ind]
    cross_top = int(len(population) * ( crossover_top / 100))
    while(len(offsrping)<len(population)):
        i = random.random()
        cross_1 = random.randint(0, len(population) - 1)
        if i < good_crossover_probability:
            cross_2 = random.randint(0, cross_top - 1)
        else:
            cross_2 = random.randint(0, len(population) - 1)
        while(cross_1 == cross_2):
            if i < good_crossover_probability:
                cross_2 = random.randint(0, cross_top - 1)
            else:
                cross_2 = random.randint(0, len(population) - 1)

        child1, child2 = population[cross_1].crossover(population[cross_2])
        offsrping.extend([child1, child2])

    if(len(offsrping) == len(population)):
        return offsrping
    else:
        return offsrping[:len(population)]

def mutate_population(population: List[Chromosome], gene_mutation_probability: float) -> List[Chromosome]:
    for chromosome in population:
        chromosome.mutate(gene_mutation_probability)

    return population

def run_GA(ttp_instance: TTPInstance, run: float) -> None:

    logbook = tools.Logbook()

    ttp_stats = tools.Statistics(key=lambda ind: ind.get_fitness())
    ttp_stats.register("avg", lambda x: int(numpy.mean(x)))
    ttp_stats.register("std", lambda x: int(numpy.std(x)))
    ttp_stats.register("min", lambda x: int(numpy.min(x)))
    ttp_stats.register("max", lambda x: int(numpy.max(x)))

    salesman_population = [SalesmanChromosome.get_random(len(ttp_instance.cities)) for _ in range(number_of_individuals_in_population)]
    knapsack_population = [KnapsackChromosome.get_random(len(ttp_instance.items)) for _ in range(number_of_individuals_in_population)]

    evaluate_populations(salesman_population, knapsack_population, ttp_instance)

    for generation in range(number_of_generations):
        salesman_offspring = select(salesman_population)
        knapsack_offspring = select(knapsack_population)

        salesman_offspring = crossover_population(salesman_offspring, good_crossover_probability, crossover_top)
        knapsack_offspring = crossover_population(knapsack_offspring, good_crossover_probability, crossover_top)

        salesman_offspring = mutate_population(salesman_offspring, gene_mutation_probability)
        knapsack_offspring = mutate_population(knapsack_offspring, gene_mutation_probability)

        evaluate_populations(salesman_offspring, knapsack_offspring, ttp_instance)

        salesman_population[:] = salesman_offspring
        knapsack_population[:] = knapsack_offspring

        ttp_solutions = []
        for s in salesman_population:
            for k in knapsack_population:
                ttp_solutions.append(Solution(s,k,ttp_instance))


        ttp_record = ttp_stats.compile(ttp_solutions)

        print(f"Generation {generation + 1}, run {run+1}:")
        print(ttp_record)
        logbook.record(gen=generation + 1, **ttp_record)

    return logbook

def main():

    for filename in os.listdir('instances'):
        if filename.endswith('.ttp'):
            ttp_instance = TTPInstance.load_from_file(os.path.join('instances', filename))
            for run in range(30):
                print(f"Running GA for {filename}, run {run+1}")
                run_GA(ttp_instance, run)

if __name__ == "__main__":
    main()
