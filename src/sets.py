import random
import numpy as np
import skfuzzy as fuzz
from datetime import datetime
from skfuzzy import control as ctrl
from deap import base, creator, tools, algorithms


class _HardcodedSets:

    def _configure_second_score_set(self):
        _universe = self._sets['SecondScore'].universe
        self._sets['SecondScore']['very poor'] = fuzz.trimf(_universe, [0, 0, 25])
        self._sets['SecondScore']['poor'] = fuzz.trimf(_universe, [0, 25, 50])
        self._sets['SecondScore']['average'] = fuzz.trimf(_universe, [25, 50, 75])
        self._sets['SecondScore']['good'] = fuzz.trimf(_universe, [50, 75, 100])
        self._sets['SecondScore']['excellent'] = fuzz.trimf(_universe, [75, 100, 100])

    def _configure_midterm_exam_set(self):
        _universe = self._sets['MidtermExam'].universe
        self._sets['MidtermExam']['very poor'] = fuzz.trimf(self._sets['MidtermExam'].universe, [0, 0, 23.75])
        self._sets['MidtermExam']['poor'] = fuzz.trimf(self._sets['MidtermExam'].universe, [0, 23.75, 47.5])
        self._sets['MidtermExam']['average'] = fuzz.trimf(self._sets['MidtermExam'].universe, [23.75, 47.5, 71.25])
        self._sets['MidtermExam']['good'] = fuzz.trimf(self._sets['MidtermExam'].universe, [47.5, 71.25, 88])
        self._sets['MidtermExam']['excellent'] = fuzz.trimf(self._sets['MidtermExam'].universe, [71.25, 88, 100])

    def _configure_logins_set(self):
        _universe = self._sets['Logins'].universe
        self._sets['Logins']['very poor'] = fuzz.trimf(self._sets['Logins'].universe, [0, 0, 20.75])
        self._sets['Logins']['poor'] = fuzz.trimf(self._sets['Logins'].universe, [0, 20.75, 50.5])
        self._sets['Logins']['average'] = fuzz.trimf(self._sets['Logins'].universe, [20.75, 50.5, 70.25])
        self._sets['Logins']['good'] = fuzz.trimf(self._sets['Logins'].universe, [50.5, 70.25, 283])
        self._sets['Logins']['excellent'] = fuzz.trimf(self._sets['Logins'].universe, [70.25, 283, 283])

    def _configure_reads_set(self):
        _universe = self._sets['Reads'].universe
        self._sets['Reads']['very poor'] = fuzz.trimf(_universe, [0, 0, 10.5])
        self._sets['Reads']['poor'] = fuzz.trimf(_universe, [0, 10.5, 20])
        self._sets['Reads']['average'] = fuzz.trimf(_universe, [10.5, 20, 40.5])
        self._sets['Reads']['good'] = fuzz.trimf(_universe, [20, 40.5, 110])
        self._sets['Reads']['excellent'] = fuzz.trimf(_universe, [40.5, 110, 110])

    def _configure_results_set(self):
        _universe = self._sets['Results'].universe
        self._sets['Results']['very poor'] = fuzz.trimf(_universe, [0, 0, 23.25])
        self._sets['Results']['poor'] = fuzz.trimf(_universe, [0, 23.25, 46.5])
        self._sets['Results']['average'] = fuzz.trimf(_universe, [23.25, 46.5, 69.75])
        self._sets['Results']['good'] = fuzz.trimf(_universe, [46.5, 69.75, 88])
        self._sets['Results']['excellent'] = fuzz.trimf(_universe, [69.75, 88, 100])

    def __init__(self):
        self._sets = {
            'SecondScore': ctrl.Antecedent(np.arange(0, 100, 1), 'SecondScore'),
            'MidtermExam': ctrl.Antecedent(np.arange(0, 100, 1), 'MidtermExam'),
            'Logins': ctrl.Antecedent(np.arange(0, 283, 1), 'Logins'),
            'Reads': ctrl.Antecedent(np.arange(0, 110, 1), 'Reads'),
            'Results': ctrl.Consequent(np.arange(0, 100, 1), 'Results')
        }

        self._configure_second_score_set()
        self._configure_midterm_exam_set()
        self._configure_logins_set()
        self._configure_reads_set()

        self._configure_results_set()

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : HardcodedSets created.')

    def get_sets(self):
        return self._sets

    def views(self):
        for key, value in self._sets.items():
            value.view()


class _GeneticRanges:
    @staticmethod
    def _compute_accuracy(parameters: list, column: list):

        # обраховуємо точність меж на основі випадкових чисел з генетичного алгоритму

        _actual_categories = []
        very_poor, poor, average, good, excellent = parameters
        _categories = ["very poor", "poor", "average", "good", "excellent"]

        for score in column:
            if score <= poor:
                _actual_categories.append("very poor")
            elif score <= average:
                _actual_categories.append("poor")
            elif score <= good:
                _actual_categories.append("average")
            elif score <= excellent:
                _actual_categories.append("good")
            else:
                _actual_categories.append("excellent")

        accuracy = sum(1 for a, p in zip(_actual_categories, _categories) if a == p) / len(_categories)
        return accuracy,

    def _evaluate_second_score(self, parameters=None):
        return self._compute_accuracy(parameters, self._dictionary['SecondScore'])

    def _evaluate_midterm_exam(self, parameters=None):
        return self._compute_accuracy(parameters, self._dictionary['MidtermExam'])

    def _evaluate_logins(self, parameters=None):
        return self._compute_accuracy(parameters, self._dictionary['Logins'])

    def _evaluate_reads(self, parameters=None):
        return self._compute_accuracy(parameters, self._dictionary['Reads'])

    def _configure_creator(self, creator_type: str):
        self._toolbox = base.Toolbox()

        # конфігуримо специфічний генетичний конфігуратор і запускаємо функцію для генерацію
        # випадкових чисел для визначення точності меж

        if creator_type == 'SecondScore':
            def _compute_second_score():
                return [random.uniform(start, end) for start, end in self._maximums['SecondScore']]

            self._toolbox.register("individual", tools.initIterate, creator.Individual, _compute_second_score)
        if creator_type == 'MidtermExam':
            def _compute_midterm_exam():
                return [random.uniform(start, end) for start, end in self._maximums['MidtermExam']]

            self._toolbox.register("individual", tools.initIterate, creator.Individual, _compute_midterm_exam)
        if creator_type == 'Logins':
            def _compute_logins():
                return [random.uniform(start, end) for start, end in self._maximums['Logins']]

            self._toolbox.register("individual", tools.initIterate, creator.Individual, _compute_logins)
        if creator_type == 'Reads':
            def _compute_reads():
                return [random.uniform(start, end) for start, end in self._maximums['Reads']]

            self._toolbox.register("individual", tools.initIterate, creator.Individual, _compute_reads)

        self._toolbox.register("population", tools.initRepeat, list, self._toolbox.individual)
        self._toolbox.register("mate", tools.cxTwoPoint)
        self._toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=10, indpb=0.1)
        self._toolbox.register("select", tools.selTournament, tournsize=3)

        self._population = self._toolbox.population(n=self._population_size)

    def _compute_second_score(self):
        self._configure_creator('SecondScore')
        self._toolbox.register("evaluate", self._evaluate_second_score)

        algorithms.eaSimple(self._population, self._toolbox,
                            cxpb=self._two_mating_probability, mutpb=self._individual_mutating_probability,
                            ngen=self._generation_number, stats=None, halloffame=None, verbose=None)

        best_individual = tools.selBest(self._population, k=1)[0]
        return best_individual

    def _compute_midterm_exam(self):
        self._configure_creator('MidtermExam')
        self._toolbox.register("evaluate", self._evaluate_midterm_exam)

        algorithms.eaSimple(self._population, self._toolbox,
                            cxpb=self._two_mating_probability, mutpb=self._individual_mutating_probability,
                            ngen=self._generation_number, stats=None, halloffame=None, verbose=None)

        best_individual = tools.selBest(self._population, k=1)[0]
        return best_individual

    def _compute_logins(self):
        self._configure_creator('Logins')
        self._toolbox.register("evaluate", self._evaluate_logins)

        algorithms.eaSimple(self._population, self._toolbox,
                            cxpb=self._two_mating_probability, mutpb=self._individual_mutating_probability,
                            ngen=self._generation_number, stats=None, halloffame=None, verbose=None)

        best_individual = tools.selBest(self._population, k=1)[0]
        return best_individual

    def _compute_reads(self):
        self._configure_creator('Reads')
        self._toolbox.register("evaluate", self._evaluate_reads)

        algorithms.eaSimple(self._population, self._toolbox,
                            cxpb=self._two_mating_probability, mutpb=self._individual_mutating_probability,
                            ngen=self._generation_number, stats=None, halloffame=None, verbose=None)

        best_individual = tools.selBest(self._population, k=1)[0]
        return best_individual

    @staticmethod
    def _compute_results():
        return [26, 50, 68, 85, 100]

    def __init__(self):
        # створюємл і конфігуримо обєкт для генетичних сетів
        self._maximums = None
        self._dictionary = None
        self._genetic_sets = None

        self._population_size = 1
        self._generation_number = 2
        self._two_mating_probability = 0.7
        self._individual_mutating_probability = 0.1

        creator.create("FitnessMin", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        print(f'{datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")} --------------------------> : GeneticRanges created.')

    def is_sets_valid(self):
        is_valid = True
        for i in range(0, 4):
            is_valid &= self._genetic_sets[i][0] < self._genetic_sets[i][1] < self._genetic_sets[i][2] < self._genetic_sets[i][3] < self._genetic_sets[i][4]
        return is_valid

    def compute_(self):
        # рекурсивно обраховуємо генетичні сети
        self._genetic_sets = [self._compute_second_score(),
                              self._compute_midterm_exam(),
                              self._compute_logins(),
                              self._compute_reads(),
                              self._compute_results()]

        # 18 48 60 78 100
        if self.is_sets_valid():
            return self._genetic_sets

        # якщо генетичний обрахує сети у поганому порядку (тобто а більше рівне б а б менше рівне с), тобто не справджується
        # основна умова фазі алгоритму (а менше рівне б менше рівне с), то ми перерахуємо сети ще раз
        self.compute_()

    def compute(self, _dictionary: dict):
        self._dictionary = _dictionary
        self._maximums = {
            'SecondScore': [(0, 25), (25,50), (50, 71), (71, 88), (88, max(_dictionary['SecondScore']))],
            'MidtermExam': [(0, 25), (25, 50), (50, 71), (71, 88), (88, max(_dictionary['MidtermExam']))],
            'Logins': [(0, 10), (10, 20), (20, 50), (50, 120), (120, max(_dictionary['Logins']))],
            'Reads': [(0, 5), (5, 10), (10, 20), (20, 60), (60, max(_dictionary['Reads']))],
            'Results': [(0, 25), (25, 50), (50, 71), (71, 88), (88, 100)]
        }
        return [self._maximums, self.compute_()]

    def print(self):
        if self._genetic_sets is None:
            return

        print(f'---------------------------------------> : Genetic sets.')
        print(f'SecondScore : {self._genetic_sets[0]}')
        print(f'MidtermExam : {self._genetic_sets[1]}')
        print(f'Logins : {self._genetic_sets[2]}')
        print(f'Reads : {self._genetic_sets[3]}')

    def maximums(self):
        return self._maximums


class _GeneticSets:

    def _get_random_ranges(self, index: int, range_name: str):
        return [(0, self._genetic_ranges[1][index][0]),
                (self._genetic_ranges[1][index][0], self._genetic_ranges[1][index][1]),
                (self._genetic_ranges[1][index][1], self._genetic_ranges[1][index][2]),
                (self._genetic_ranges[1][index][2], self._genetic_ranges[1][index][3]),
                (self._genetic_ranges[1][index][3], self._genetic_ranges[0][range_name][4][1])]

    def _configure_set(self, _column_name: str, _column_index: int):
        # базуючись на генетично обрахованих межах ми створюємо сети для фаззі моделі

        _ranges = self._get_random_ranges(_column_index, _column_name)

        _a = [0, 0, _ranges[0][1]]
        _b = [_ranges[0][1], _ranges[1][0], _ranges[1][1]]
        _c = [_ranges[1][1], _ranges[1][1], _ranges[2][1]]
        _d = [_ranges[2][1], _ranges[2][1], _ranges[3][1]]
        _e = [_ranges[3][1], _ranges[4][0], _ranges[4][1]]

        self._sets[_column_name]['very poor'] = fuzz.trimf(self._sets[_column_name].universe, _a)
        self._sets[_column_name]['poor'] = fuzz.trimf(self._sets[_column_name].universe, _b)
        self._sets[_column_name]['average'] = fuzz.trimf(self._sets[_column_name].universe, _c)
        self._sets[_column_name]['good'] = fuzz.trimf(self._sets[_column_name].universe, _d)
        self._sets[_column_name]['excellent'] = fuzz.trimf(self._sets[_column_name].universe, _e)

    def __init__(self, _dictionary: dict):
        self._genetic_ranges = _GeneticRanges().compute(_dictionary)

        # отримуємо максимальні значення для кожного сету
        _second_score_max = self._genetic_ranges[0]['SecondScore'][4][1]
        _midterm_exam_max = self._genetic_ranges[0]['MidtermExam'][4][1]
        _logins_max = self._genetic_ranges[0]['Logins'][4][1]
        _reads_max = self._genetic_ranges[0]['Reads'][4][1]
        _results_max = self._genetic_ranges[0]['Results'][4][1]

        self._sets = {
            'SecondScore': ctrl.Antecedent(np.arange(0, _second_score_max, 1), 'SecondScore'),
            'MidtermExam': ctrl.Antecedent(np.arange(0, _midterm_exam_max, 1), 'MidtermExam'),
            'Logins': ctrl.Antecedent(np.arange(0, _logins_max, 1), 'Logins'),
            'Reads': ctrl.Antecedent(np.arange(0, _reads_max, 1), 'Reads'),
            'Results': ctrl.Consequent(np.arange(0, _results_max, 1), 'Results')
        }

        # створюємо самі генетичні сети
        self._configure_set('SecondScore', 0)
        self._configure_set('MidtermExam', 1)
        self._configure_set('Logins', 2)
        self._configure_set('Reads', 3)
        self._configure_set('Results', 4)

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : GeneticSets created.')

    def get_sets(self):
        return self._sets

    def get_native_ranges(self):
        return self._genetic_ranges

    def views(self):
        for key, value in self._sets.items():
            value.view()


class Sets:
    def __init__(self, _dictionary: dict):
        # для простоти ми комбінуємо константні сети і генетичні в один обєкт
        self._hardcoded_sets = _HardcodedSets()
        self._genetic_sets = _GeneticSets(_dictionary)

    def get_hardcoded_sets(self):
        return self._hardcoded_sets

    def get_genetic_sets(self):
        return self._genetic_sets

    def hardcoded_views(self):
        for key, value in self._hardcoded_sets.get_sets().items():
            value.view()

    def genetic_views(self):
        for key, value in self._genetic_sets.get_sets().items():
            value.view()

    def get_native_ranges(self):
        return self._genetic_sets.get_native_ranges()
