import datetime
import src.sets
import src.rules
import src.panda
import src.utils


def print_note():
    print('\n')
    print('Practice App')
    print('\n')
    print('Available commands:')
    print('------------------------------------')
    print('- [read_initial] : read initial data from csv file for further computation.')
    print('- [print_initial] : print initial.')
    print('------------------------------------')
    print('- [sets_initialize | rules_initialize] : initialize genetic & hardcoded sets | rules. {only once}')
    print('- [sets_hardcoded_views | sets_genetic_views] : show views.')
    print('- [rules_hardcoded_print | rules_genetic_print] : print rules.')
    print('------------------------------------')
    print('- [panda_hardcoded_initialize | panda_genetic_initialize] : initialize hardcoded | genetic Panda object. {only once}')
    print('-------------------')
    print('- [panda_genetic_compute | panda_hardcoded_compute] : compute result based on { initial } csv file { with predefined format }, and store to out file.')
    print('------------------------------------')
    print('- [read_results] : read result from compute { out } csv file.')
    print('- [print_results] : print computation results.')
    print('------------------------------------')
    print('- [print_native_ranges] : print native genetic ranges.')
    print('------------------------------------')
    print('- [quit] : quit from the program.')
    print('\n')


if __name__ == "__main__":
    print_note()

    _initial_data = src.utils.InitialData()
    _computation_data = src.utils.ComputationData()

    _sets = None
    _rules = None
    _panda_genetic = None
    _panda_hardcoded = None

    print('\n')

    while True:
        cmd = input(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")} -> Enter a command: ')

        if cmd == 'read_initial':
            _initial_data.read('res/information.csv', ';')
        elif cmd == 'print_initial':
            _initial_data.print()
        elif cmd == 'sets_initialize':
            if _sets is not None:
                print('! Sets already initialized !')
                continue
            if _initial_data.len() is None:
                print('! Please execute: read_initial !')
                continue
            _sets = src.sets.Sets(_initial_data.get())
        elif cmd == 'print_native_ranges':
            if _sets is None:
                print('! Please execute: sets_initialize !')
                continue
            _info = _sets.get_native_ranges()
            for _key, _values in _info[0].items():
                print('{} : {}')



        elif cmd == 'rules_initialize':
            if _sets is None:
                print('! Please execute: sets_initialize !')
                continue
            if _rules is not None:
                print('! Rules already initialized !')
                continue
            _rules = src.rules.Rules(_sets)
        elif cmd == 'sets_hardcoded_views':
            if _sets is None:
                print('! Please execute: sets_initialize !')
                continue
            _sets.hardcoded_views()
        elif cmd == 'sets_genetic_views':
            if _sets is None:
                print('! Please execute: sets_initialize !')
                continue
            _sets.genetic_views()
        elif cmd == 'rules_hardcoded_print':
            if _rules is None:
                print('! Please execute: rules_initialize !')
                continue
            _rules.print_hardcoded_rules()
        elif cmd == 'rules_genetic_print':
            if _rules is None:
                print('! Please execute: rules_initialize !')
                continue
            _rules.print_genetic_rules()
        elif cmd == 'panda_hardcoded_initialize':
            if _sets is None:
                print('! Please execute: sets_initialize !')
                continue
            if _rules is None:
                print('! Please execute: rules_initialize !')
                continue
            if _panda_hardcoded is not None:
                print('! PANDA HARDCODED already initialized !')
                continue
            _panda_hardcoded = src.panda.Panda('hardcoded', _rules.get_hardcoded_rules())
        elif cmd == 'panda_hardcoded_compute':
            if _panda_hardcoded is None:
                print('! Please execute: panda_hardcoded_initialize !')
                continue
            _computation = _panda_hardcoded.compute(_initial_data.get(), _initial_data.len())
            _computation_data.write(_computation, 'hardcoded_computation')
        elif cmd == 'panda_genetic_initialize':
            if _sets is None:
                print('! Please execute: sets_initialize !')
                continue
            if _rules is None:
                print('! Please execute: rules_initialize !')
                continue
            if _panda_genetic is not None:
                print('! PANDA GENETIC already initialized !')
                continue
            _panda_genetic = src.panda.Panda('genetic', _rules.get_genetic_rules())
        elif cmd == 'panda_genetic_compute':
            if _panda_genetic is None:
                print('! Please execute: panda_genetic_initialize !')
                continue
            _computation = _panda_genetic.compute(_initial_data.get(), _initial_data.len())
            _computation_data.write(_computation, 'genetic_computation')
        elif cmd == 'read_results':
            _file_name = input("Enter a file name {example : ComputationData_20231001020556997984.json} with computation results: ")
            _computation_data.read(_file_name)
        elif cmd == 'print_results':
            _computation_data.print()
        elif cmd == 'quit':
            break
