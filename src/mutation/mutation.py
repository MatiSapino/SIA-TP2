
import random

class Mutation:
	def __init__(self, mutation_probability, image, M=None):
		self.mutation_probability = mutation_probability
		self.image = image
		self.height, self.width = image.shape[:2]
		self.M = M

	def mutate_color(self, triangle):
		print("Mutating color")
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		a = random.randint(0, 255)
		triangle.gen_color = (r, g, b, a)

	def mutate_vertex(self, triangle):
		while True:
			triangle_points = [
				(random.randint(0, self.width - 1), random.randint(0, self.height - 1)),
				(random.randint(0, self.width - 1), random.randint(0, self.height - 1)),
				(random.randint(0, self.width - 1), random.randint(0, self.height - 1)),
			]
			if len(set(triangle_points)) == 3:
				break
		print("Mutating vertex")
		triangle.gen_triangle = tuple(triangle_points)

	def gene(self, individual):
		if random.random() < self.mutation_probability:
			triangles = individual.get_triangles()
			idx = random.randint(0, len(triangles) - 1)
			triangle = triangles[idx]
			mutation_type = random.choice(["color", "vertex", "both"])
			if mutation_type == "color":
				self.mutate_color(triangle)
			elif mutation_type == "vertex":
				self.mutate_vertex(triangle)
			else:
				self.mutate_color(triangle)
				self.mutate_vertex(triangle)

	def multigen_limited(self, individual):
		triangles = individual.get_triangles()
		n = len(triangles)
		M = self.M if self.M is not None else n
		num_genes = random.randint(1, min(M, n))
		indices = random.sample(range(n), num_genes)
		for idx in indices:
			if random.random() < self.mutation_probability:
				triangle = triangles[idx]
				mutation_type = random.choice(["color", "vertex", "both"])
				if mutation_type == "color":
					self.mutate_color(triangle)
				elif mutation_type == "vertex":
					self.mutate_vertex(triangle)
				else:
					self.mutate_color(triangle)
					self.mutate_vertex(triangle)

	def multigen_uniform(self, individual):
		triangles = individual.get_triangles()
		for triangle in triangles:
			if random.random() < self.mutation_probability:
				mutation_type = random.choice(["color", "vertex", "both"])
				if mutation_type == "color":
					self.mutate_color(triangle)
				elif mutation_type == "vertex":
					self.mutate_vertex(triangle)
				else:
					self.mutate_color(triangle)
					self.mutate_vertex(triangle)

	def complete(self, individual):
		if random.random() < self.mutation_probability:
			triangles = individual.get_triangles()
			for triangle in triangles:
				mutation_type = random.choice(["color", "vertex", "both"])
				if mutation_type == "color":
					self.mutate_color(triangle)
				elif mutation_type == "vertex":
					self.mutate_vertex(triangle)
				else:
					self.mutate_color(triangle)
					self.mutate_vertex(triangle)
