import json
import pandas
from datetime import datetime


class ComputationData:
    def __init__(self):
        self._file_name = None
        self._information = None
        print(
            f'{datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")} --------------------------> : ComputationData constructed.')

    def write(self, computation: dict, base: str):
        self._file_name = f'results/{base}_ComputationData_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.json'

        with open(self._file_name, 'w') as file:
            file.write(json.dumps(computation, indent=4))

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : File: {self._file_name} written.')

    def read(self, _file_path: str):
        self._file_name = 'results/data/' + _file_path

        with open(self._file_name, 'r') as file:
            self._information = json.load(file)

    def print(self):
        if self._information is None:
            print('%Y-%m-%d %H:%M:%S.%f")} --------------------------> : READ DATA FIRST! ')
            return

        print(f'\n ===------------------------------------- ComputationData')
        print(f'{self._information}')
        print('===-------------------------------------\n')


class InitialData:
    def __init__(self):
        self._len = None
        self._file_name = None
        self._information = None
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : InitialData constructed.')

    def read(self, _name: str, _separator: str):
        _raw_data = pandas.read_csv(_name, delimiter=_separator)

        _SecondScore = []
        _MidtermExam = []
        _Logins = []
        _Reads = []

        for _index, _row in _raw_data.iterrows():
            _columns = _row.tolist()

            _SecondScore.append(_columns[0])
            _MidtermExam.append(_columns[1])
            _Logins.append(_columns[2])
            _Reads.append(_columns[3])

        self._file_name = _name
        self._len = len(_raw_data)
        self._information = {
            'SecondScore': _SecondScore,
            'MidtermExam': _MidtermExam,
            'Logins': _Logins,
            'Reads': _Reads
        }

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : File [{_name}] with separator [{_separator}] read.')

    def print(self):
        if self._information is None:
            print('%Y-%m-%d %H:%M:%S.%f")} --------------------------> : READ DATA FIRST! ')
            return

        print(f'\n ===------------------------------------- InitialData')
        for _key, _value in self._information.items():
            print(f'{_key}: {_value}')
        print('===-------------------------------------\n')

    def get(self):
        return self._information

    def len(self):
        return self._len
