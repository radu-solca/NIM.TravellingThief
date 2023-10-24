from solution import Solution, VisitedCity, SelectedItem

def main():

    city1 = VisitedCity(15, [SelectedItem(100,120), SelectedItem(100, 110)])
    city2 = VisitedCity(45, [SelectedItem(1,100), SelectedItem(10, 15)])
    city3 = VisitedCity(2, [SelectedItem(100,80), SelectedItem(100, 80)])

    someRandomSolution = Solution([city1, city2, city3])

    print(someRandomSolution.get_fitness(10, 100, 1000, 40))
    pass


if (__name__ == "__main__"):
    main()