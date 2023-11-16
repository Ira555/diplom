import itertools
from datetime import datetime
from skfuzzy import control as ctrl


class Rules:
    @staticmethod
    def _score_to_number(_score: str):
        if _score == 'very poor':
            return 1
        if _score == 'poor':
            return 2
        if _score == 'average':
            return 3
        if _score == 'good':
            return 4
        return 5

    @staticmethod
    def _score_to_string(_score):
        if _score <= 4:
            return 'very poor'
        if _score <= 8:
            return 'poor'
        if _score <= 12:
            return 'average'
        if _score <= 16:
            return 'good'

        return 'excellent'

    @staticmethod
    def _get_result(_arg1=None, _arg2=None, _arg3=None, _arg4=None):
        _score = 0

        if _arg1 is not None:
            _score += Rules._score_to_number(_arg1)
        if _arg2 is not None:
            _score += Rules._score_to_number(_arg2)
        if _arg3 is not None:
            _score += Rules._score_to_number(_arg3)
        if _arg4 is not None:
            _score += Rules._score_to_number(_arg4)

        return Rules._score_to_string(_score)

    def _create_combinations(self, sets=None):
        _ratings = ['very poor', 'poor', 'average', 'good', 'excellent']
        _combinations = list(itertools.product(_ratings, repeat=4))

        _rules = []
        for _combination in _combinations:
            _second_score = sets['SecondScore'][_combination[0]]
            _midterm_exam = sets['MidtermExam'][_combination[1]]
            _login = sets['Logins'][_combination[2]]
            _reads = sets['Reads'][_combination[3]]

            _result = sets['Results'][self._get_result(_combination[0],
                                                       _combination[1],
                                                       _combination[2],
                                                       _combination[3])]

            _rules.append(ctrl.Rule(_second_score & _midterm_exam & _login & _reads, _result))

        return _rules

    def __init__(self, sets=None):
        if sets is None:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : Invalid sets.')
            return

        self._hardcoded_rules = self._create_combinations(sets.get_hardcoded_sets().get_sets())
        self._genetic_rules = self._create_combinations(sets.get_genetic_sets().get_sets())

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : Rules created.')

    def get_hardcoded_rules(self):
        return self._hardcoded_rules

    def print_hardcoded_rules(self):
        print(f'\n ===------------------------------------- Hardcoded rules.')
        for value in self._hardcoded_rules:
            print(f'{value}')
        print(f' ===------------------------------------- \n')

    def get_genetic_rules(self):
        return self._genetic_rules

    def print_genetic_rules(self):
        print(f'\n ===------------------------------------- Genetic rules.')
        for value in self._genetic_rules:
            print(f'{value}')
        print(f' ===------------------------------------- \n')