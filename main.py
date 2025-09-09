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
        amount_of_triangle = config["amount_of_triangle"]
        k_selection_size = config["k_selection_size"]
        crossover_probability = config["crossover_probability"]

        population = generate_initial_population(target_image, population_size, amount_of_triangle)
        fitness_obj = Fitness(population, target_image)

        selector = Selection(population, fitness_obj)
        selection_method = config["selection_method"]
        if hasattr(selector, selection_method):
            method = getattr(selector, selection_method)
            chosen_parents = method(k_selection_size)
        else:
            raise ValueError(f"Invalid {selection_method} selection method")

        children_size = k_selection_size
        crossover_method = config["crossover_method"]
        crossover = Crossover(chosen_parents, children_size, amount_of_triangle, crossover_probability)
        if hasattr(crossover, crossover_method):
            method = getattr(crossover, crossover_method)
            children = method()
        else:
            raise ValueError(f"Invalid {crossover_method} crossover method")

        print("Selected individuals:\n")
        for individual in chosen_parents:
            print(f"Individual: {individual.get_triangles()} \n")

        print("New population after crossover:\n")
        for individual in children:
            print(f"Individual: {individual.get_triangles()} \n")

        cv2.imwrite("output.png", fitness_obj.render_individual(children[0]))