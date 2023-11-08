import math
from typing import List

class Item:
    def __init__(self, index: int, profit: float, weight: float, city_index: int):
        self.index = index
        self.profit = profit
        self.weight = weight
        self.city_index = city_index

class City:
    def __init__(self, index: int, x: float, y: float):
        self.index = index
        self.x = x
        self.y = y

    def get_distance_to(self, other: 'City'):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class TTPInstance:
    def __init__(
        self, 
        problem_name: str, 
        knapsack_type: str, 
        capacity: float, 
        speed_min: float,
        speed_max: float,
        rent_ratio: float,
        edge_weight_type: str,
        cities: List[City],
        items: List[Item]
    ):
        self.problem_name = problem_name 
        self.knapsack_type = knapsack_type 
        self.capacity = capacity 
        self.speed_min = speed_min
        self.speed_max = speed_max
        self.rent_ratio = rent_ratio
        self.edge_weight_type = edge_weight_type
        self.cities = cities
        self.items = items

    @staticmethod
    def load_from_file(filepath: str) -> 'TTPInstance':
        with open(filepath, 'r') as file:

            #Read Problem Data
            problem_name = file.readline().split(":")[1].strip()
            knapsack_type = file.readline().split(":")[1].strip()
            cities_count = int(file.readline().split(":")[1].strip())
            items_count = int(file.readline().split(":")[1].strip())
            capacity = float(file.readline().split(":")[1].strip())
            speed_min = float(file.readline().split(":")[1].strip())
            speed_max = float(file.readline().split(":")[1].strip())
            rent_ratio = float(file.readline().split(":")[1].strip())
            edge_weight_type = file.readline().split(":")[1].strip()

            #Read Cities
            file.readline()
            cities = {}
            for _ in range(cities_count):
                city_index, city_x, city_y = file.readline().split()
                city_index, city_x, city_y = int(city_index), float(city_x), float(city_y)
                city = City(city_index, city_x, city_y)
                cities[city_index] = city

            #Read Items
            file.readline()
            items = {}
            for _ in range(items_count):
                item_index, item_profit, item_weight, item_assigned_node = file.readline().split()
                item_index, item_profit, item_weight, item_assigned_node = int(item_index), float(item_profit), float(item_weight), int(item_assigned_node)
                item = Item(item_index, item_profit, item_weight, item_assigned_node)
                items[item_index] = item

            return TTPInstance(
                problem_name, 
                knapsack_type, 
                capacity, 
                speed_min,
                speed_max,
                rent_ratio,
                edge_weight_type,
                cities,
                items
            )