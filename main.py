import argparse
import csv
import json
import time
import cv2
import os

from src.crossover.crossover import Crossover
from src.fitness.fitness import Fitness
from src.population.population import generate_initial_population
from src.selection.selection import Selection
from src.mutation.mutation import Mutation

def create_svg_from_individual(individual, filename="output.svg"):
    img_width = target_image.shape[1]
    img_height = target_image.shape[0]
    svg_content = f'<svg width="{img_width}" height="{img_height}" xmlns="http://www.w3.org/2000/svg">\n'
    genotypes = individual.get_triangles()

    for index, genotype in enumerate(genotypes):
        r, g, b, a = genotype.gen_color
        rgb_color = f'rgb({r}, {g}, {b})'
        alpha_opacity = a / 255.0
        p1, p2, p3 = genotype.gen_triangle
        svg_content += f'  <polygon points="{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}" fill="{rgb_color}" fill-opacity="{alpha_opacity:.2f}" />\n'

    svg_content += '</svg>'

    with open(filename, 'w') as f:
        f.write(svg_content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Genetic Algorithm for image recreation.')
    parser.add_argument('--target-image', type=str, default="./src/data/flag.png", help='Path to the target image.')
    parser.add_argument('--amount-of-triangles', type=int, default=200, help='Number of triangles.')
    parser.add_argument('--config-file', type=str, default="./configs/config.json",
                        help='Path to the configuration JSON file.')
    parser.add_argument('--target-csv', type=str, default="./fitnessEvolution.csv", help='Path to the fitness evolution data CSV file.')
    parser.add_argument('--render-division', type=int, default=10, help='How often do you generate output images.')
    parser.add_argument('--print-progress', type=str, default="", help='Print progress data. Default = false')
    parser.add_argument('--render-path', type=str, default="./render", help='Path to the output folder.')
    parser.add_argument('--output-image', type=str, default="output.png", help='Path to the output image.')
    parser_args = parser.parse_args()
    target_image_path = parser_args.target_image
    if target_image_path is None:
        raise ValueError("Target image path is not specified in command line.")
    target_image = cv2.imread(target_image_path)

    triangles = parser_args.amount_of_triangles
    if triangles is None:
        raise ValueError("Amount of triangles is not specified in command line.")
    amount_of_triangle = triangles

# ----- RENDER FILES -----

    render_dir = parser_args.render_path
    render_history_dir = os.path.join(render_dir, "history")
    os.makedirs(render_dir, exist_ok=True)
    os.makedirs(render_history_dir, exist_ok=True)

    render_items = [item for item in os.listdir(render_dir + "/") if item != "history"]
    
    if len(render_items) != 0:
        render_history = [int(name) for name in os.listdir(render_history_dir) if name.isdigit()]
        render_history_next_number = max(render_history, default=0) + 1
        render_history_new_dir = os.path.join(render_history_dir, f"{render_history_next_number:04d}")
        os.makedirs(render_history_new_dir)
        
        for item in render_items:
            src = os.path.join(render_dir, item)
            dst = os.path.join(render_history_new_dir, item)
            os.rename(src, dst)

    with open(parser_args.config_file, 'r') as file:
        config = json.load(file)
    
    with open(os.path.join(render_dir, "config_used.json"), "w", encoding="utf-8") as file:
        config["amount_of_triangle"] = amount_of_triangle
        json.dump(config, file, indent=4, ensure_ascii=False)
    
    target_copy_path = os.path.join(render_dir, "image_used.png")
    cv2.imwrite(target_copy_path, target_image)

# --------------------

    n_population_size = config["n_population_size"]

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

    mutation_method = config.get("mutation_method", "gene")
    mutation_probability = config.get("mutation_probability", 0.05)
    mutation_M = config.get("mutation_M", None)

    implementation = config["implementation"]

    stop_condition = config["stop_condition"]
    stop_condition_max_time_seconds = config.get("stop_condition_max_time_seconds", float('inf'))
    stop_condition_max_generations = config.get("stop_condition_max_generations", float('inf'))
    stop_condition_acceptable_solution = config.get("stop_condition_acceptable_solution", 1.0)

    stop_condition_structure_generations = config.get("stop_condition_structure_generations", 10)
    stop_condition_structure_percentage = config.get("stop_condition_structure_percentage", 0.2)
    stop_condition_structure_delta = config.get("stop_condition_structure_delta", 0.001)

    stop_condition_content_generations = config.get("stop_condition_content_generations", 10)
    stop_condition_content_delta = config.get("stop_condition_content_delta", 0.001)

    valid_stop_conditions = ["max_time_seconds", "max_generations", "acceptable_solution", "structure", "content"]
    if stop_condition not in valid_stop_conditions:
        raise ValueError(f"Invalid stop condition: {stop_condition}")

    n_population = generate_initial_population(target_image, n_population_size, amount_of_triangle)
    fitness_obj = Fitness(n_population, target_image)

    stop = False
    start_time = time.time()
    generation_count = 0
    best_fitness_so_far = 0
    relevant_population_history = []
    stable_structure_generations = 0
    best_fitness_history = []
    stable_content_generations = 0

    with open(parser_args.target_csv, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Generacion", "Fitness_Max", "Generational Breach","Time"])
        
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

            mutation_obj = Mutation(mutation_probability, target_image, mutation_M)
            if hasattr(mutation_obj, mutation_method):
                mutation_func = getattr(mutation_obj, mutation_method)
                for child in k_children:
                    mutation_func(child)
            else:
                raise ValueError(f"Invalid mutation method: {mutation_method}")

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

            if stop_condition == "structure":
                m_relevant_population = int(n_population_size * stop_condition_structure_percentage)
                relevant_population = sorted(n_population, key=lambda ind: ind.fitness, reverse=True)[:m_relevant_population]
                relevant_population_history.append(relevant_population)

                if len(relevant_population_history) > stop_condition_structure_generations:
                    old_relevant_population = relevant_population_history[0]
                    changed_individuals = 0

                    for i in range(m_relevant_population):
                        if relevant_population[i].get_triangles() != old_relevant_population[i].get_triangles():
                            changed_individuals += 1

                    change_percentage = changed_individuals / m_relevant_population

                    if change_percentage <= stop_condition_structure_delta:
                        stable_structure_generations += 1
                    else:
                        stable_structure_generations = 0

                    relevant_population_history.pop(0)

            if stop_condition == "content":
                current_best_individual = max(n_population, key=lambda ind: ind.fitness)
                best_fitness_so_far = current_best_individual.fitness
                best_fitness_history.append(best_fitness_so_far)

                if len(best_fitness_history) > stop_condition_content_generations:
                    current_best_fitness = best_fitness_history[-1]
                    old_best_fitness = best_fitness_history[0]

                    if abs(current_best_fitness - old_best_fitness) <= stop_condition_content_delta:
                        stable_content_generations += 1
                    else:
                        stable_content_generations = 0
                    best_fitness_history.pop(0)

            if stop_condition == "acceptable_solution":
                current_best_individual = max(n_population, key=lambda individual: individual.fitness)
                best_fitness_so_far = current_best_individual.fitness

            if generation_count % parser_args.render_division == 0:
                best_individual_so_far = sorted(n_population, key=lambda ind: ind.fitness, reverse=True)[0]
                render_path = f"render/generation_{generation_count}.png"
                cv2.imwrite(render_path, fitness_obj.render_individual(best_individual_so_far))

            generational_breach = sum(1 for individual in n_population if individual in k_children) / n_population_size
            current_best_individual = max(n_population, key=lambda individual: fitness_obj.fitness(individual))
            best_fitness_so_far = fitness_obj.fitness(current_best_individual)
            writer.writerow([generation_count, best_fitness_so_far, generational_breach, f"{time.time() - start_time:.2f}s" ])
            
            if parser_args.print_progress:
                print(f"Generation: {generation_count}")
                print(f"Breach: {generational_breach:.2f}")
                print(f"Best Fitness: {best_fitness_so_far:.2f}")
                print(f"Time passed: {time.time() - start_time:.2f}s\n")

            if stop_condition == "max_time_seconds" and (time.time() - start_time) >= stop_condition_max_time_seconds:
                stop = True
            elif stop_condition == "max_generations" and generation_count >= stop_condition_max_generations:
                stop = True
            elif stop_condition == "acceptable_solution" and best_fitness_so_far >= stop_condition_acceptable_solution:
                stop = True
            elif stop_condition == "structure" and stable_structure_generations >= stop_condition_structure_generations:
                stop = True
            elif stop_condition == "content" and stable_content_generations >= stop_condition_content_generations:
                stop = True

    best_individual = sorted(n_population, key=lambda ind: ind.fitness, reverse=True)[0]
    error = (1.0 / best_individual.fitness) - 1.0

    print("\n--- Stop Condition Reached ---")
    print(f"Executed Generations: {generation_count}")
    print(f"Total Time: {time.time() - start_time:.2f} seconds")
    print(f"Best Fitness: {best_individual.fitness:.4f}")
    print(f"Error: {error:.4f}")

    cv2.imwrite(parser_args.output_image, fitness_obj.render_individual(best_individual))
    create_svg_from_individual(best_individual)
