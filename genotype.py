import random
from typing import Tuple

class SalesmanChromosome:
    def __init__(self, number_of_cities: int):
        permutation = list(range(1, number_of_cities))
        random.shuffle(permutation)
        self.tour = permutation

    def mutate(self):
        # Choose two random indices in the permutation
        index1 = random.randint(0, len(self.tour) - 1)
        index2 = random.randint(0, len(self.tour) - 1)

        # Swap the elements at these indices
        self.tour[index1], self.tour[index2] = self.tour[index2], self.tour[index1]

    def crossover(self, other: 'SalesmanChromosome'):

        #Get random crossover point
        crossover_point = random.randint(1, len(self.tour) - 1)

        #Remove from each parent the elements in the other parents second slice (automatically shift all elements to the left)
        rmv1 = self.tour[crossover_point:]
        rmv2 = other.tour[crossover_point:]
        child1 =  [x for x in self.tour if x not in rmv2]
        child2 =  [x for x in other.tour if x not in rmv1]

        #Shuffle the removed parts
        random.shuffle(rmv1)
        random.shuffle(rmv2)

        #Combine the original part of a parent (shiftet left) with the chosen elements of the other parent
        child1 = child1 + rmv2
        child2 = child2 + rmv1

        return child1, child2

    
class KnapsackChromosome:
    def __init__(self, number_of_items: int):
        self.items = [random.choice([True, False]) for _ in range(number_of_items-1)]

    def mutate(self):
        # flip a bit

        index = random.randint(0, len(self.items) - 1)
        self.items[index] = not self.items[index]

    def crossover(self, other: 'KnapsackChromosome') -> Tuple['KnapsackChromosome','KnapsackChromosome']:
        # one point crossover

        assert len(self.items) == len(other.items)

        crossover_point = random.randint(1, len(self.items) - 1)

        child1 = KnapsackChromosome(len(self.items))
        child2 = KnapsackChromosome(len(other.items))

        child1.items[:crossover_point] = self.items[:crossover_point]
        child1.items[crossover_point:] = other.items[crossover_point:]
        child2.items[:crossover_point] = other.items[:crossover_point]
        child2.items[crossover_point:] = self.items[crossover_point:]

        return child1, child2