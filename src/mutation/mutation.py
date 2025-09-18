import random


class Mutation:

    def __init__(self, mutation_probability, image, mutation_m=None):
        self.mutation_probability = mutation_probability
        self.image = image
        self.height, self.width = image.shape[:2]
        self.mutation_m = mutation_m

    def mutate_vertex(self, triangle):
        points = list(triangle.gen_triangle)
        idx = random.randint(0, 2)

        while True:
            new_point = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            points[idx] = new_point

            if len(set(points)) == 3 and self._area(*points) > 0:
                triangle.gen_triangle = tuple(points)
                break

    @staticmethod
    def _area(p1, p2, p3):
        return abs(
            p1[0] * (p2[1] - p3[1]) +
            p2[0] * (p3[1] - p1[1]) +
            p3[0] * (p1[1] - p2[1])
        ) / 2

    def gene(self, individual):
        if random.random() < self.mutation_probability:
            triangles = individual.get_triangles()
            idx = random.randint(0, len(triangles) - 1)
            triangle = triangles[idx]
            self._mutate_single_triangle(triangle)

    def multigen_limited(self, individual):
        triangles = individual.get_triangles()
        n = len(triangles)
        mutation_m = self.mutation_m if self.mutation_m is not None else n
        num_genes = random.randint(1, min(mutation_m, n))
        indices = random.sample(range(n), num_genes)
        for idx in indices:
            if random.random() < self.mutation_probability:
                triangle = triangles[idx]
                self._mutate_single_triangle(triangle)

    def multigen_uniform(self, individual):
        triangles = individual.get_triangles()
        for triangle in triangles:
            if random.random() < self.mutation_probability:
                self._mutate_single_triangle(triangle)

    def complete(self, individual):
        if random.random() < self.mutation_probability:
            triangles = individual.get_triangles()
            for triangle in triangles:
                self._mutate_single_triangle(triangle)

    def _mutate_single_triangle(self, triangle):
        mutation_type = random.choice(["color", "vertex", "both"])
        if mutation_type == "color":
            self.mutate_color(triangle)
        elif mutation_type == "vertex":
            self.mutate_vertex(triangle)
        else:
            self.mutate_color(triangle)
            self.mutate_vertex(triangle)

    @staticmethod
    def mutate_color(triangle):
        r, g, b, a = triangle.gen_color

        r = (r + random.randint(-10, 10)) % 256
        g = (g + random.randint(-10, 10)) % 256
        b = (b + random.randint(-10, 10)) % 256
        a = (a + random.randint(-10, 10)) % 256

        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        a = max(0, min(255, a))

        triangle.gen_color = (r, g, b, a)