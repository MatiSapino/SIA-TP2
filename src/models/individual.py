class Individual:

    def __init__(self):
        self.triangles = []
        self.fitness = None
        self.relative_fitness = None

    def update_fitness(self, fitness):
        self.fitness = fitness

    def update_relative_fitness(self, relative_fitness):
        self.relative_fitness = relative_fitness

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    def get_triangles(self):
        return self.triangles

    @classmethod
    def from_triangles(cls, triangles):
        individual = cls()
        individual.triangles = triangles
        return individual