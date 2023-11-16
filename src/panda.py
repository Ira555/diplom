from datetime import datetime
from skfuzzy import control as ctrl


class Panda:
    def __init__(self, name: str, rules=None):
        if rules is None:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : Invalid rules.')
            return

        self._name = name
        self._control_system = ctrl.ControlSystem(rules)
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : ({self._name}) Control system created.')

        self._control_system_simulation = ctrl.ControlSystemSimulation(self._control_system)
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : ({self._name}) Control system simulation created.')

    def compute(self, _dictionary: dict, _rows: int):
        _first_computations = {}
        for _row in range(0, _rows):
            for _key, _values in _dictionary.items():
                self._control_system_simulation.input[_key] = _values[_row]

            self._control_system_simulation.compute()
            _first_computations[_row] = self._control_system_simulation.output["Results"]

        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} --------------------------> : ({self._name}) Computation finished.')
        return _first_computations
