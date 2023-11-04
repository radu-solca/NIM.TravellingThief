import random

class City:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.items = []  # Initialize an empty list for items

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

class Item:
    def __init__(self, profit, weight, assigned_node):
        self.profit = profit
        self.weight = weight
        self.assigned_node = assigned_node

    def get_profit(self):
        return self.profit

    def get_weight(self):
        return self.weight

    def get_assigned_node(self):
        return self.assigned_node

def road_one_point_crossover(parent1, parent2):

  #Get random crossover point
  crossover_point = random.randint(1, len(parent1) - 1)

  #Remove from each parent the elements in the other parents second slice (automatically shift all elements to the left)
  rmv1 = parent1[crossover_point:]
  rmv2 = parent2[crossover_point:]
  offspring1 =  [x for x in parent1 if x not in rmv2]
  offspring2 =  [x for x in parent2 if x not in rmv1]

  #Shuffle the removed parts
  random.shuffle(rmv1)
  random.shuffle(rmv2)

  #Combine the original part of a parent (shiftet left) with the chosen elements of the other parent
  offspring1 = offspring1 + rmv2
  offspring2 = offspring2 + rmv1

  return offspring1, offspring2


def take_one_point_crossover(parent1, parent2):
  # Get a random point
  crossover_point = random.randint(1, len(parent1) - 1)
  # Crossover
  offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
  offspring2 = parent2[:crossover_point] + parent1[crossover_point:]

  return offspring1, offspring2


def inversion_mutation(arr):
  # Get two random points in our array
  start, end = sorted(random.sample(range(len(arr)), 2))
    
  # Make sure the segement is at least 2 bits long
  while end - start < 2:
    start, end = sorted(random.sample(range(len(arr)), 2))

    # Invert the portion of the array between the two points
  arr[start:end + 1] = arr[start:end + 1][::-1]

  return arr


def shift_mutation(arr):
  # Get the size of the shifted segment
  segment_size = random.randint(2, len(arr))
    
  # Get a random number of shifts
  shift_amount = random.randint(1, segment_size - 1)
    
  # Left or Right
  shift_direction = random.choice([-1, 1])
    
  # Get the segment
  start = random.randint(0, len(arr) - segment_size)
  segment_to_shift = arr[start:start + segment_size]
    
  # Shift
  if shift_direction == -1:
    shifted_segment = segment_to_shift[shift_amount:] + segment_to_shift[:shift_amount]
  else:
    shifted_segment = segment_to_shift[-shift_amount:] + segment_to_shift[:-shift_amount]
    
  arr[start:start + segment_size] = shifted_segment
    
  return arr

def flip_bit_mutation(arr):

    # Random Index
    flip = random.randint(0, len(arr) - 1)

    # Flip
    arr[flip] = 1 - arr[flip]

    return arr


def randomize_list(n):
    solution = list(range(1, n+1))

    random.shuffle(solution)

    return solution

def data_reader(file_path):

  global cities
  global items
  global cities_count
  global items_count

  with open(file_path, 'r') as file:

    #Read Problem Data
    problem_name = file.readline().split(":")[1].strip()
    print(problem_name)
    knapsack_type = file.readline().split(":")[1].strip()
    print(knapsack_type)
    cities_count = int(file.readline().split(":")[1].strip())
    print(cities_count)
    items_count = int(file.readline().split(":")[1].strip())
    print(items_count)
    capacity = float(file.readline().split(":")[1].strip())
    print(capacity)
    speed_min = float(file.readline().split(":")[1].strip())
    print(speed_min)
    speed_max = float(file.readline().split(":")[1].strip())
    print(speed_max)
    rent_ratio = float(file.readline().split(":")[1].strip())
    print(rent_ratio)
    edge_weight_type = file.readline().split(":")[1].strip()
    print(edge_weight_type)

    #Read Cities
    aux = file.readline()
    for aux in range(cities_count):
      city_index, city_x, city_y = file.readline().split()
      city = City(city_x, city_y)
      cities[city_index] = city
    print(len(cities))

    #Read Items
    aux = file.readline()
    for aux in range(items_count):
      item_index, item_profit, item_weight, item_assigned_node = file.readline().split()
      item = Item(item_profit, item_weight, item_assigned_node)
      items[item_index] = item
      cities[item_assigned_node].add_item(item_index)
    print(len(items))



cities = {}
items = {}
cities_count = 0
items_count = 0
generation_size = 6
solutions = list()

data_reader('/content/a280_n1395_bounded-strongly-corr_01.ttp')

#Initial solution 
for i in range(generation_size):
  result = randomize_list(6) #cities_size
  solutions.append(result)

print(solutions[0])
print(solutions[1]) 
print()
print(road_one_point_crossover(solutions[0], solutions[1]))
print()
print(inversion_mutation(solutions[0]))
print()
print(shift_mutation(solutions[0]))
