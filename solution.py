from typing import List

class SelectedItem:
    def __init__(self, weight: int, profit: int):
        self.weight = weight
        self.profit = profit

class VisitedCity:
    def __init__(self, distance: float, items: List[SelectedItem]):
        self.distance = distance
        self.selected_items = items

class Solution:

    def __init__(self, visited_cities: List[VisitedCity]):
        self.__visited_cities = visited_cities

    def get_fitness(self, min_speed: float, max_speed: float, max_weight: int, R: float) -> float:

        collected_weight = 0
        speed_coef = (max_speed - min_speed) / max_weight

        fitness = 0

        for city in self.__visited_cities:
            for item in city.selected_items:
                collected_weight += item.weight
                fitness += item.profit
            fitness -= city.distance * R / (max_speed - speed_coef * collected_weight)
        return fitness
    

