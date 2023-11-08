import numpy as np
from typing import List

from problem import City, Item, TTPInstance

class Solution:

    def __init__(self, salesman_chromosome: np.ndarray, knapsack_chromosome: np.ndarray, problem_instance: TTPInstance):

        self.items_picked_per_city: List[Item] = [[] for _ in range(len(problem_instance.cities))]

        for item_index, item in problem_instance.items.items():
            if knapsack_chromosome[item.index-1]:
                self.items_picked_per_city[item.city_index-1].append(item)

        self.city_tour: List[City] = [problem_instance.cities[i] for i in salesman_chromosome]

        self.problem_instance = problem_instance


    def get_fitness(self) -> float:

        fitness = 0

        collected_weight = 0
        speed_coef = (self.problem_instance.speed_max - self.problem_instance.speed_min) / self.problem_instance.capacity

        #start in the first city
        previous_city = self.city_tour[0]

        for current_city in self.city_tour:
            
            for item in self.items_picked_per_city[current_city.index-1]:
                collected_weight += item.weight
                fitness += item.profit
                
            fitness -= current_city.get_distance_to(previous_city) * self.problem_instance.rent_ratio / (self.problem_instance.speed_max - speed_coef * collected_weight)
            previous_city = current_city

        return fitness
    

