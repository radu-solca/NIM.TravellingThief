from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple

class Chromosome(ABC):
    def __init__(self):
        self.fitness = None

    def set_fitness(self, fitness: float) -> None:
        self.fitness = fitness

    def clear_fitness(self) -> None:
        self.fitness = None

    @abstractmethod
    def mutate(self, gene_mutation_probability: float) -> None:
        pass

    @abstractmethod
    def crossover(self, other: 'Chromosome') -> Tuple['Chromosome', 'Chromosome']:
        pass

class SalesmanChromosome(Chromosome):
    def __init__(self, permutation: np.ndarray):
        super().__init__()
        self.permutation = permutation

    @staticmethod
    def get_random(number_of_cities: int) -> 'SalesmanChromosome':
        permutation = np.arange(1, number_of_cities+1)
        np.random.shuffle(permutation)
        return SalesmanChromosome(permutation)

    def mutate(self, gene_mutation_probability: float) -> None:
        for i in range(len(self.permutation)):
            if np.random.random() < gene_mutation_probability:
                swap_index = np.random.randint(len(self.permutation))
                self.permutation[i], self.permutation[swap_index] = self.permutation[swap_index], self.permutation[i]

    def crossover(self: 'SalesmanChromosome', other: 'SalesmanChromosome') -> Tuple['SalesmanChromosome', 'SalesmanChromosome']:
        crossover_point = np.random.randint(1, len(self.permutation))
        rmv1 = set(self.permutation[crossover_point:])
        rmv2 = set(other.permutation[crossover_point:])
        child1 =  [x for x in self.permutation if x not in rmv2]
        child2 =  [x for x in other.permutation if x not in rmv1]
        np.random.shuffle(list(rmv1))
        np.random.shuffle(list(rmv2))
        child1 = np.concatenate((child1, list(rmv2)))
        child2 = np.concatenate((child2, list(rmv1)))
        return SalesmanChromosome(child1), SalesmanChromosome(child2)

class KnapsackChromosome(Chromosome):
    def __init__(self, items: np.ndarray):
        super().__init__()
        self.items = items

    @staticmethod
    def get_random(number_of_items: int) -> 'KnapsackChromosome':
        items = np.random.choice([True, False], size=number_of_items)
        return KnapsackChromosome(items)

    def mutate(self, gene_mutation_probability: float) -> None:
        for i in range(len(self.items)):
            if np.random.random() < gene_mutation_probability:
                self.items[i] = not self.items[i]

    def crossover(self: 'KnapsackChromosome', other: 'KnapsackChromosome') -> Tuple['KnapsackChromosome', 'KnapsackChromosome']:
        assert len(self.items) == len(other.items)
        crossover_point = np.random.randint(1, len(self.items))
        child1 = np.copy(self.items)
        child2 = np.copy(other.items)
        child1[:crossover_point] = self.items[:crossover_point]
        child1[crossover_point:] = other.items[crossover_point:]
        child2[:crossover_point] = other.items[:crossover_point]
        child2[crossover_point:] = self.items[crossover_point:]
        return KnapsackChromosome(child1), KnapsackChromosome(child2)
