import sys
sys.path.append('..')

from problem import TTPInstance
from genotype import KnapsackChromosome, SalesmanChromosome
from phenotype import Solution

def main():
    # Load TTP instance from file
    ttp_instance = TTPInstance.load_from_file('../instances/a280_n279_bounded-strongly-corr_01.ttp')

    print(f'Problem Name: {ttp_instance.problem_name}')
    print(f'Knapsack Type: {ttp_instance.knapsack_type}')
    print(f'Capacity: {ttp_instance.capacity}')
    print(f'Min Speed: {ttp_instance.speed_min}')
    print(f'Max Speed: {ttp_instance.speed_max}')
    print(f'Rent Ratio: {ttp_instance.rent_ratio}')
    print(f'Edge Weight Type: {ttp_instance.edge_weight_type}')
    print(f'Cities: {[city for city in ttp_instance.cities]}')
    print(f'Items: {[item for item in ttp_instance.items]}')

    # Create a hardcoded solution
    # Replace these with your actual solution
    salesman_chromosome = SalesmanChromosome([i for i in range(1, len(ttp_instance.cities)+1)])
    knapsack_chromosome = KnapsackChromosome([True for _ in range(len(ttp_instance.items))])

    # Compute fitness for the solution
    solution = Solution(salesman_chromosome, knapsack_chromosome, ttp_instance)
    fitness = solution.get_fitness()

    print(f'Fitness: {fitness}')

if __name__ == '__main__':
    main()
