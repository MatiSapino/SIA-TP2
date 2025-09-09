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
        n_population_size = config["n_population_size"]
        amount_of_triangle = config["amount_of_triangle"]
        k_selection_size = config["k_selection_size"]
        crossover_probability = config["crossover_probability"]
        implementation = config["implementation"]

        n_population = generate_initial_population(target_image, n_population_size, amount_of_triangle)
        fitness_obj = Fitness(n_population, target_image)

        selector = Selection(n_population, fitness_obj)
        selection_method = config["selection_method"]
        if hasattr(selector, selection_method):
            method = getattr(selector, selection_method)
            k_chosen_parents = method(k_selection_size)
        else:
            raise ValueError(f"Invalid {selection_method} selection method")

        k_children_size = k_selection_size
        crossover_method = config["crossover_method"]
        crossover = Crossover(k_chosen_parents, k_children_size, amount_of_triangle, crossover_probability)
        if hasattr(crossover, crossover_method):
            method = getattr(crossover, crossover_method)
            k_children = method()
        else:
            raise ValueError(f"Invalid {crossover_method} crossover method")

        for individual in k_children:
            individual.update_fitness(fitness_obj.fitness(individual))

        if implementation == "traditional":
            combined_population = n_population + k_children

            combined_fitness_obj = Fitness(combined_population, target_image)
            combined_selector = Selection(combined_population, combined_fitness_obj)
            method = getattr(combined_selector, selection_method)

            new_population = method(n_population_size)

        elif implementation == "young-bias":
            if k_children_size > n_population_size:
                children_fitness_obj = Fitness(k_children, target_image)
                children_selector = Selection(k_children, children_fitness_obj)
                method = getattr(children_selector, selection_method)
                new_population = method(n_population_size)
            else:
                new_population = k_children.copy()
                remaining_population_size = n_population_size - k_children_size
                method = getattr(selector, selection_method)
                remaining_population = method(remaining_population_size)
                new_population.extend(remaining_population)

        else:
            raise ValueError(f"Invalid implementation method: {implementation}")

        n_population = new_population

        generational_breach = sum(1 for individual in n_population if individual in k_children) / n_population_size
        last_generation_individuals = (1 - generational_breach) * n_population_size
        individuals_generated = generational_breach * n_population_size

        print("Selected individuals:\n")
        for individual in k_chosen_parents:
            print(f"Individual: {individual.get_triangles()} \n")

        print("New population after crossover:\n")
        for individual in k_children:
            print(f"Individual: {individual.get_triangles()} \n")

        print("New population:\n")
        for individual in n_population:
            print(f"Individual: {individual.get_triangles()} \n")

        print(f"Generational Breach: {generational_breach:.2f}\n")
        print(f"Last generation individuals: {last_generation_individuals}\n")
        print(f"Individuals generated: {individuals_generated}\n")

        cv2.imwrite("output.png", fitness_obj.render_individual(k_children[0]))