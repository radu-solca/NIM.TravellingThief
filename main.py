import copy
import os
import random
from typing import List

import pandas as pd
from problem import TTPInstance
from genotype import Chromosome, KnapsackChromosome, SalesmanChromosome
from phenotype import Solution

number_of_generations = 30
number_of_individuals_in_population = 100
evaluation_parallel_population_sample = 10
tournament_size = 3
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

    run_stats = pd.DataFrame(columns=['Generation', 'Salesman_Avg_Fitness', 'Knapsack_Avg_Fitness', 'Best_Solution_Fitness', 'Best_So_Far_Solution_Fitness'])

    salesman_population = [SalesmanChromosome.get_random(len(ttp_instance.cities)) for _ in range(number_of_individuals_in_population)]
    knapsack_population = [KnapsackChromosome.get_random(len(ttp_instance.items)) for _ in range(number_of_individuals_in_population)]

    evaluate_populations(salesman_population, knapsack_population, ttp_instance)

    best_so_far_solution_fitness = 0

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

        print(f"Generation {generation + 1}:")
        best_salesman = max(salesman_offspring, key=lambda x: x.fitness)
        best_knapsack = max(knapsack_offspring, key=lambda x: x.fitness)
        best_solution = Solution(best_salesman, best_knapsack, ttp_instance)
        best_solution_fitness = best_solution.get_fitness()

        if(best_solution_fitness > best_so_far_solution_fitness):
            best_so_far_solution_fitness = best_solution_fitness

        run_stats = pd.concat([run_stats, pd.DataFrame([{
            'Generation': generation + 1,
            'Salesman_Avg_Fitness': sum(individual.fitness for individual in salesman_offspring) / len(salesman_offspring),
            'Knapsack_Avg_Fitness': sum(individual.fitness for individual in knapsack_offspring) / len(knapsack_offspring),
            'Best_Solution_Fitness': best_solution.get_fitness(),
            'Best_So_Far_Solution_Fitness': best_so_far_solution_fitness
        }])], ignore_index=True)

    return run_stats

def main():

    stats_df = pd.DataFrame(columns=['Instance', 'Run', 'Generation', 'Salesman_Avg_Fitness', 'Knapsack_Avg_Fitness', 'Best_Solution_Fitness', 'Best_So_Far_Solution_Fitness'])

    for filename in os.listdir('instances'):
        if filename.endswith('.ttp'):
            ttp_instance = TTPInstance.load_from_file(os.path.join('instances', filename))
            for run in range(30):
                print(f"Running GA for {filename}, run {run+1}")
                run_stats = run_GA(ttp_instance)
                run_stats['Instance'] = filename
                run_stats['Run'] = run + 1
                stats_df = pd.concat([stats_df, run_stats], ignore_index=True)

    stats_df.to_csv('genetic_algorithm_stats.csv', index=False)
    

if __name__ == "__main__":
    main()
