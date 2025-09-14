import heapq
import math
import random
from concurrent.futures import ProcessPoolExecutor


def evaluate_individual(args):
    individual, fitness_obj, idx = args
    fitness = fitness_obj.fitness(individual)

    return individual, fitness, idx


class Selection:

    def __init__(self, population, fitness_obj, use_threads):
        self.population = population
        self.fitness_obj = fitness_obj
        self.use_threads = use_threads



    def elite(self, k_selection_size):
        n_population_size = len(self.population)

        # fitness_list = [(individual, self.fitness_obj.fitness(individual)) for individual in self.population]
        if self.use_threads:
            tasks = [(ind, self.fitness_obj, i) for i, ind in enumerate(self.population)]
            print("ANtes de with")
            with ProcessPoolExecutor(max_workers=4) as executor:
                fitness_list = list(executor.map(evaluate_individual, tasks))
            print("despues de with")
        else:
            fitness_list = [(individual, self.fitness_obj.fitness(individual), i)
                        for i, individual in enumerate(self.population)]

        if k_selection_size < n_population_size:
            heap = []
            for individual, fitness, i in fitness_list:
                if len(heap) < k_selection_size:
                    heapq.heappush(heap, (fitness, i, individual))
                else:
                    if fitness > heap[0][0]:
                        heapq.heapreplace(heap, (fitness, i, individual))

            sorted_pop = [individual for fitness, _, individual in sorted(heap, key=lambda x: x[0], reverse=True)]

        else:
            sorted_pop = [individual for individual, fitness, _ in
                          sorted(fitness_list, key=lambda x: x[1], reverse=True)]

        selected = []
        for i, individual in enumerate(sorted_pop):
            n_i = math.ceil((k_selection_size - i) / n_population_size)
            selected.extend([individual] * n_i)

            if len(selected) >= k_selection_size:
                selected = selected[:k_selection_size]
                break

        return selected

    def roulette(self, k_selection_size):
        fitness_list = [(individual, self.fitness_obj.relative_fitness(individual)) for individual in self.population]
        return self._roulette(k_selection_size, fitness_list)

    def _roulette(self, k_selection_size, fitness_list):
        individuals, qi_values = self._accumulated_qi(fitness_list)

        selected = []
        for _ in range(k_selection_size):
            r = random.random()
            selected_index = self._binary_search(qi_values, r)
            selected.append(individuals[selected_index])

        return selected

    def universal(self, k_selection_size):
        fitness_list = [(individual, self.fitness_obj.relative_fitness(individual)) for individual in self.population]
        individuals, qi_values = self._accumulated_qi(fitness_list)

        selected = []
        r = random.random()
        for j in range(k_selection_size):
            rj = (r + j) / k_selection_size
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

        return self._roulette(k_selection_size, pseudo_fitness)

    def boltzmann(self, k_selection_size, temperature_c, temperature_0, k_constant, t_generation):
        temperature = temperature_c + (temperature_0 - temperature_c) * math.exp(-k_constant * t_generation)

        exp_values = []
        for individual in self.population:
            fitness = self.fitness_obj.fitness(individual)
            exp_values.append((individual, math.exp(fitness / temperature)))

        avg_exp = sum(val for individual, val in exp_values) / len(exp_values)
        pseudo_fitness = [(individual, val / avg_exp) for individual, val in exp_values]

        return self._roulette(k_selection_size, pseudo_fitness)

    def deterministic_tournaments(self, k_selection_size, m_selection_size):
        n_population_size = self.population

        selected = []
        for _ in range(k_selection_size):
            competitors = random.sample(n_population_size, m_selection_size)
            best = max(competitors, key=lambda individual: self.fitness_obj.fitness(individual))
            selected.append(best)

        return selected

    def probabilistic_tournaments(self, k_selection_size, threshold):
        n_population_size = self.population

        selected = []
        for _ in range(k_selection_size):
            individual1, individual2 = random.sample(n_population_size, 2)
            fitness1 = self.fitness_obj.fitness(individual1)
            fitness2 = self.fitness_obj.fitness(individual2)

            r = random.random()
            if r < threshold:
                winner = individual1 if fitness1 > fitness2 else individual2
            else:
                winner = individual1 if fitness1 <= fitness2 else individual2

            selected.append(winner)

        return selected

    @staticmethod
    def _accumulated_qi(fitness_list):
        acc = 0
        individuals, qi_values = [], []
        for individual, pi in fitness_list:
            acc += pi
            individuals.append(individual)
            qi_values.append(acc)

        qi_values = [qi / acc for qi in qi_values]

        return individuals, qi_values

    @staticmethod
    def _binary_search(qi_values, target):
        left = 0
        right = len(qi_values) - 1
        while left < right:
            mid = (left + right) // 2
            if qi_values[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left
