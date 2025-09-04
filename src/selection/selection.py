import heapq
import math
import random


class Selection:

    def __init__(self, population, fitness_obj):
        self.population = population
        self.fitness_obj = fitness_obj

    def elite(self, k_selection_size):
        n_population_size = len(self.population)

        fitness_list = [(individual, self.fitness_obj.fitness(individual)) for individual in self.population]

        if k_selection_size < n_population_size:
            heap = []
            for individual, fitness in fitness_list:
                if len(heap) < k_selection_size:
                    heapq.heappush(heap, (fitness, individual))
                else:
                    if fitness > heap[0][0]:
                        heapq.heapreplace(heap, (fitness, individual))

            sorted_pop = [individual for fitness, individual in sorted(heap, key=lambda x: x[0], reverse=True)]

        else:
            sorted_pop = [individual for individual, fitness in sorted(fitness_list, key=lambda x: x[1], reverse=True)]

        selected = []
        for i, individual in enumerate(sorted_pop):
            n_i = math.ceil((k_selection_size - i) / n_population_size)
            selected.extend([individual] * n_i)

            if len(selected) >= k_selection_size:
                selected = selected[:k_selection_size]
                break

        return selected

    def roulette(self, k_selection_size):
        individuals, qi_values = self._accumulated_qi()

        selected = []
        for _ in range(k_selection_size):
            r = random.random()
            selected_index = self._binary_search(qi_values, r)
            selected.append(individuals[selected_index])

        return selected

    def universal(self, k_selection_size):
        individuals, qi_values = self._accumulated_qi()

        selected = []
        r = random.random()
        for j in range(k_selection_size):
            rj = (r + j) / k_selection_size
            rj = rj % 1
            selected_index = self._binary_search(qi_values, rj)
            selected.append(individuals[selected_index])

        return selected

    def ranking(self, k_selection_size):
        n_population_size = len(self.population)

        fitness_list = [(individual, self.fitness_obj.fitness(individual)) for individual in self.population]
        sorted_fitness = sorted(fitness_list, key=lambda x: x[1], reverse=True)

        pseudo_fitness = []
        for rank, (individual, fitness) in enumerate(sorted_fitness, start=1):
            f_prime = (n_population_size - rank) / n_population_size
            pseudo_fitness.append((individual, f_prime))

        acc = 0
        individuals, qi_values = [], []
        for individual, f_prime in pseudo_fitness:
            acc += f_prime
            individuals.append(individual)
            qi_values.append(acc)

        qi_values = [q / acc for q in qi_values]

        selected = []
        for _ in range(k_selection_size):
            r = random.random()
            selected_index = self._binary_search(qi_values, r)
            selected.append(individuals[selected_index])

        return selected

    def boltzmann(self, k_selection_size, generation, T0, Tc, k):
        T = Tc + (T0 -Tc) * math.exp(-k * generation)

        exp_values = []
        for individual in self.population:
            fitness = self.fitness_obj.fitness(individual)
            exp_values.append((individual, math.exp(fitness / T)))

        avg_exp = sum(val for individual, val in exp_values) / len(exp_values)
        pseudo_fitness = [(individual, val / avg_exp) for individual, val in exp_values]

        acc = 0
        individuals, qi_values = [], []
        for individual, pf in pseudo_fitness:
            acc += pf
            individuals.append(individual)
            qi_values.append(acc)

        qi_values = [q / acc for q in qi_values]

        selected = []
        for _ in range(k_selection_size):
            r = random.random()
            selected_index = self._binary_search(qi_values, r)
            selected.append(individuals[selected_index])

        return selected

    def deterministic_tournaments(self, n_population_size, m_selection_size):
        selected = []
        for _ in range(m_selection_size):
            competitors = random.sample(self.population, n_population_size)
            best = max(competitors, key=lambda individual: self.fitness_obj.fitness(individual))
            selected.append(best)

        return selected

    def _accumulated_qi(self):
        relative_fitness = [(individual, self.fitness_obj.relative_fitness(individual)) for individual in self.population]

        accumulated = []
        acc = 0
        for individual, pi in relative_fitness:
            acc += pi
            accumulated.append((individual, acc))

        individuals = [individual for individual, qi in accumulated]
        qi_values = [qi for individual, qi in accumulated]

        return individuals, qi_values

    @staticmethod
    def _binary_search(qi_values, target):
        left = 0
        right= len(qi_values) - 1
        while left < right:
            mid = (left + right) // 2
            if qi_values[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left