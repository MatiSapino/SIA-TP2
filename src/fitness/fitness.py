import numpy as np
import cv2


class Fitness:

    def __init__(self, population, target_image):
        self.population = population
        self.target_image = target_image

    def fitness(self, individual):
        generated = self.render_individual(individual)
        error = float(np.mean((self.target_image - generated) ** 2))
        fitness = 1 / (1 + error)
        return fitness

    def relative_fitness(self, individual):
        total_fitness = sum(self.fitness(ind) for ind in self.population)
        return self.fitness(individual) /total_fitness

    def render_individual(self, individual):
        canvas = np.ones_like(self.target_image, dtype=np.uint8) * 255

        r, g, b, a = individual.gen_color
        alpha = a / 255

        points = np.array(individual.gen_triangle, np.int32).reshape((-1, 1, 2))

        triangle_layer = canvas.copy()
        cv2.fillPoly(triangle_layer, [points], (r, g, b))

        blended = cv2.addWeighted(triangle_layer, alpha, canvas, 1 - alpha, 0)

        return blended