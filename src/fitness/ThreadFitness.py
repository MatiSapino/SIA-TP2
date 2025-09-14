from multiprocessing import shared_memory

import numpy as np
import cv2

from src.models.individual import Individual


class ThreadFitness:

    def __init__(self, image_shape, target_lab_name, lab_shape, lab_dtype):
        self.image_shape = image_shape
        self.shm_lab = shared_memory.SharedMemory(name=target_lab_name)
        self.target_lab = np.ndarray(lab_shape, dtype=lab_dtype, buffer=self.shm_lab.buf)


    def fitness(self, individual: Individual):
        if individual.fitness is not None:
            return individual.fitness

        generated_brg = self.render_individual(individual)
        generated_lab = cv2.cvtColor(generated_brg, cv2.COLOR_BGR2LAB)

        lab_diff = np.abs(self.target_lab.astype("float") - generated_lab.astype("float"))
        error = float(np.mean(lab_diff))

        scale = 20
        fitness = np.exp(-error / scale)

        individual.update_fitness(fitness)
        return fitness

    def relative_fitness(self, individual):
        raise NotImplementedError("Relative fitness is not implemented for threads")

    def close(self):
        self.shm_lab.close()

    def render_individual(self, individual):
        canvas = np.ones(self.image_shape, dtype=np.uint8) * 255

        for triangle in individual.get_triangles():
            r, g, b, a = triangle.gen_color
            alpha = a / 255

            points = np.array(triangle.gen_triangle, np.int32).reshape((-1, 1, 2))

            triangle_layer = canvas.copy()
            cv2.fillPoly(triangle_layer, [points], (b, g, r))

            canvas = cv2.addWeighted(triangle_layer, alpha, canvas, 1 - alpha, 0)

        return canvas