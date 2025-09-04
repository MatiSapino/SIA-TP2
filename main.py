import json
import sys

import cv2

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
            selected = method(config["k_selection_size"])
        else:
            raise ValueError(f"Invalid {selection_method} selection method")

        print("Selected individuals:\n")
        for individual in selected:
            print(f"Individual: {individual.chromosome()} \n")