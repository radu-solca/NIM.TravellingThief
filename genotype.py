import numpy as np
from typing import Tuple

def create_salesman_chromosome(number_of_cities: int) -> np.ndarray:
    permutation = np.arange(1, number_of_cities+1)
    np.random.shuffle(permutation)
    return permutation

def mutate_salesman_chromosome(tour: np.ndarray) -> None:
    index1, index2 = np.random.randint(0, len(tour), size=2)
    tour[index1], tour[index2] = tour[index2], tour[index1]

def crossover_salesman_chromosomes(tour1: np.ndarray, tour2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    crossover_point = np.random.randint(1, len(tour1))
    rmv1 = set(tour1[crossover_point:])
    rmv2 = set(tour2[crossover_point:])
    child1 =  [x for x in tour1 if x not in rmv2]
    child2 =  [x for x in tour2 if x not in rmv1]
    np.random.shuffle(list(rmv1))
    np.random.shuffle(list(rmv2))
    child1 = np.concatenate((child1, list(rmv2)))
    child2 = np.concatenate((child2, list(rmv1)))
    return child1, child2

def create_knapsack_chromosome(number_of_items: int) -> np.ndarray:
    return np.random.choice([True, False], size=number_of_items)

def mutate_knapsack_chromosome(items: np.ndarray) -> None:
    index = np.random.randint(0, len(items))
    items[index] = not items[index]

def crossover_knapsack_chromosomes(items1: np.ndarray, items2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    assert len(items1) == len(items2)
    crossover_point = np.random.randint(1, len(items1))
    child1 = np.copy(items1)
    child2 = np.copy(items2)
    child1[:crossover_point] = items1[:crossover_point]
    child1[crossover_point:] = items2[crossover_point:]
    child2[:crossover_point] = items2[:crossover_point]
    child2[crossover_point:] = items1[crossover_point:]
    return child1, child2
