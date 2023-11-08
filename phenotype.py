from typing import List

from problem import City, Item, TTPInstance
from genotype import KnapsackChromosome, SalesmanChromosome

class Solution:

    def __init__(self, salesman_chromosome: SalesmanChromosome, knapsack_chromosome: KnapsackChromosome, problem_instance: TTPInstance):

        self.items_picked_per_city: List[Item] = [[] for _ in range(len(problem_instance.cities))]

        for item in problem_instance.items:
            if knapsack_chromosome.items[item.city_index]:
                self.items_picked_per_city[item.city_index].append(item)

        self.city_tour: List[City] = [problem_instance.cities[i] for i in salesman_chromosome.tour]

        self.problem_instance = problem_instance


    def get_fitness(self,  R: float) -> float:

        fitness = 0

        collected_weight = 0
        speed_coef = (self.problem_instance.speed_max - self.problem_instance.speed_min) / self.problem_instance.capacity

        #start in the first city
        previous_city = self.city_tour[0]

        for city_index in range(len(self.city_tour)):
            current_city = self.city_tour[city_index]
            
            for item in self.items_picked_per_city[city_index]:
                collected_weight += item.weight
                fitness += item.profit
                
            fitness -= current_city.get_distance_to(previous_city) * self.problem_instance.rent_ratio / (self.problem_instance.speed_max - speed_coef * collected_weight)
            previous_city = current_city

        return fitness
    

