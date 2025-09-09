import json
import sys
import time

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

        selection_method = config["selection_method"]
        k_selection_size = config["k_selection_size"]
        temperature_c = config.get("temperature_c", 0)
        temperature_0 = config.get("temperature_0", 0)
        k_constant = config.get("k_constant", 0)
        t_generation = config.get("t_generation", 0)
        m_selection_size = config.get("m_selection_size", 0)
        threshold = config.get("threshold", 0)
        selection_method_args = {
            "boltzmann": [temperature_c, temperature_0, k_constant, t_generation],
            "deterministic_tournaments": [m_selection_size],
            "probabilistic_tournaments": [threshold]
        }

        crossover_method = config["crossover_method"]
        crossover_probability = config["crossover_probability"]
        p_uniform = config.get("p_uniform", 0.0)
        crossover_method_args = {
            "uniform": [p_uniform]
        }

        implementation = config["implementation"]

        stop_condition = config["stop_condition"]
        stop_condition_max_time_seconds = config.get("stop_condition_max_time_seconds", float('inf'))
        stop_condition_max_generations = config.get("stop_condition_max_generations", float('inf'))
        stop_condition_acceptable_solution = config.get("stop_condition_acceptable_solution", 1.0)

        valid_stop_conditions = ["max_time_seconds", "max_generations", "acceptable_solution"]
        if stop_condition not in valid_stop_conditions:
            raise ValueError(f"Invalid stop condition: {stop_condition}")

        n_population = generate_initial_population(target_image, n_population_size, amount_of_triangle)
        fitness_obj = Fitness(n_population, target_image)

        generation_count = 0
        start_time = time.time()
        best_fitness_so_far = 0
        stop = False

        while not stop:
            selector = Selection(n_population, fitness_obj)
            if hasattr(selector, selection_method):
                method = getattr(selector, selection_method)
                selection_args = selection_method_args.get(selection_method, [])
                k_chosen_parents = method(k_selection_size, *selection_args)
            else:
                raise ValueError(f"Invalid {selection_method} selection method")

            k_children_size = k_selection_size
            crossover = Crossover(k_chosen_parents, k_children_size, amount_of_triangle, crossover_probability)
            if hasattr(crossover, crossover_method):
                method = getattr(crossover, crossover_method)
                crossover_args = crossover_method_args.get(crossover_method, [])
                k_children = method(*crossover_args)
            else:
                raise ValueError(f"Invalid {crossover_method} crossover method")

            if implementation == "traditional":
                combined_population = n_population + k_children

                combined_fitness_obj = Fitness(combined_population, target_image)
                combined_selector = Selection(combined_population, combined_fitness_obj)
                method = getattr(combined_selector, selection_method)

                new_population = method(n_population_size, *selection_args)

            elif implementation == "young-bias":
                if k_children_size > n_population_size:
                    children_fitness_obj = Fitness(k_children, target_image)
                    children_selector = Selection(k_children, children_fitness_obj)
                    method = getattr(children_selector, selection_method)
                    new_population = method(n_population_size, *selection_args)
                else:
                    new_population = k_children.copy()
                    remaining_population_size = n_population_size - k_children_size
                    method = getattr(selector, selection_method)
                    remaining_population = method(remaining_population_size, *selection_args)
                    new_population.extend(remaining_population)

            else:
                raise ValueError(f"Invalid implementation method: {implementation}")

            n_population = new_population
            generation_count += 1

            if stop_condition == "acceptable_solution":
                current_best_individual = max(n_population, key=lambda individual: individual.fitness)
                best_fitness_so_far = current_best_individual.fitness

            if generation_count % 10 == 0:
                print(f"Generation: {generation_count}, Time passed: {time.time() - start_time:.2f}s")

            generational_breach = sum(1 for individual in n_population if individual in k_children) / n_population_size
            print(f"Generational Breach: {generational_breach:.2f}\n")

            if stop_condition == "max_time_seconds" and (time.time() - start_time) >= stop_condition_max_time_seconds:
                stop = True
            elif stop_condition == "max_generations" and generation_count >= stop_condition_max_generations:
                stop = True
            elif stop_condition == "acceptable_solution" and best_fitness_so_far >= stop_condition_acceptable_solution:
                stop = True

        best_individual = sorted(n_population, key=lambda ind: ind.fitness, reverse=True)[0]

        print("\n--- Stop Conditions Reached ---")
        print(f"Executed Generations: {generation_count}")
        print(f"Total Time: {time.time() - start_time:.2f} seconds")
        print(f"Best Fitness: {best_individual.fitness:.4f}")

        cv2.imwrite("output.png", fitness_obj.render_individual(best_individual))