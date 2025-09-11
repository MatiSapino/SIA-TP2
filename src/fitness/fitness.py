import numpy as np
import cv2

from src.models.individual import Individual


class Fitness:

    def __init__(self, population, target_image):
        self.population = population
        self.target_image = target_image
        self.target_lab = cv2.cvtColor(target_image, cv2.COLOR_BGR2LAB)

    def fitness(self, individual: Individual):
        if individual.fitness is not None:
            return individual.fitness

        generated_brg = self.render_individual(individual)
        generated_lab = cv2.cvtColor(generated_brg, cv2.COLOR_BGR2LAB)

        lab_diff = np.abs(self.target_lab.astype("float") - generated_lab.astype("float"))
        error = float(np.mean(lab_diff))

        fitness = 1.0 / (1.0 + error)

        individual.update_fitness(fitness)
        return fitness

    def relative_fitness(self, individual):
        total_fitness = sum(self.fitness(ind) for ind in self.population)
        relative_fitness = self.fitness(individual) /total_fitness
        individual.update_relative_fitness(relative_fitness)
        return relative_fitness

    def render_individual(self, individual):
        canvas = np.ones_like(self.target_image, dtype=np.uint8) * 255

        for triangle in individual.get_triangles():
            r, g, b, a = triangle.gen_color
            alpha = a / 255

            points = np.array(triangle.gen_triangle, np.int32).reshape((-1, 1, 2))

            triangle_layer = canvas.copy()
            cv2.fillPoly(triangle_layer, [points], (b, g, r))

            canvas = cv2.addWeighted(triangle_layer, alpha, canvas, 1 - alpha, 0)

        return canvas