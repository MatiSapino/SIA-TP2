import json
import sys

import cv2

from src.crossover.crossover import Crossover
from src.fitness.fitness import Fitness
from src.population.population import generate_initial_population
from src.selection.selection import Selection

if __name__ == '__main__':
    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        target_image = cv2.imread(config["target_image"])
        population_size = config["population_size"]

        population = generate_initial_population(target_image, population_size)
        fitness_obj = Fitness(population, target_image)

        selector = Selection(population, fitness_obj)
        selection_method = config["selection_method"]
        if hasattr(selector, selection_method):
            method = getattr(selector, selection_method)
            selected_population = method(config["k_selection_size"])
        else:
            raise ValueError(f"Invalid {selection_method} selection method")

        new_population_size = population_size
        crossover_method = config["crossover_method"]
        crossover = Crossover(selected_population, new_population_size)
        if hasattr(crossover, crossover_method):
            method = getattr(crossover, crossover_method)
            new_population = method()
        else:
            raise ValueError(f"Invalid {crossover_method} crossover method")

        print("Selected individuals:\n")
        for individual in selected_population:
            print(f"Individual: {individual.chromosome()} \n")

        print("New population after crossover:\n")
        for individual in new_population:
            print(f"Individual: {individual.chromosome()} \n")