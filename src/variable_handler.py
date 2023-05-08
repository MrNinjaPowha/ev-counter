import os
from pickle import dump, load, UnpicklingError
from typing import Any, Callable


class VariableHandler(dict):
    def __init__(self, data_dir: str = 'saved.pkl'):
        super().__init__({
            'generation': 0,
            'item': 0,
            'has_pokerus': False,
            'evs': [0 for _ in range(6)],
            'goals': [0 for _ in range(6)],
            'differences': [0 for _ in range(6)],
            'total': {
                'evs': 0,
                'goals': 0,
                'differences': 0
            }
        })

        self.data_dir = data_dir

        self._trackers: dict[str, list[Callable]] = {}

    def set_value(self, name: str, value):
        self._set_value_in(name, value, self)
        if self._trackers.get(name):
            for tracker in self._trackers.get(name):
                tracker()

    def get_value(self, name: str) -> Any:
        return self._get_value_from(name, self)

    def add_tracker(self, name: str, callback: Callable[[], Any]):
        if self._trackers.get(name):
            self._trackers.get(name).append(callback)
        else:
            self._trackers.update({name: [callback]})

    def save_pokemon(self, name: str):
        data = self._load_data()
        data.update({name: self._flatten(self)})
        print(data)

        with open(self.data_dir, 'wb') as file:
            dump(data, file)

    def load_pokemon(self, name: str):
        data = self._load_data()

        for key, value in data.get(name).items():
            self.set_value(key, value)

    def get_saved_pokemons(self) -> list[str]:
        data = []

        for value in sorted(self._load_data().keys()):
            data.append(value)

        return data

    def _load_data(self) -> dict[str, dict[str, Any]]:
        if not os.path.exists(self.data_dir):
            with open(self.data_dir, 'wb'):
                pass

        with open(self.data_dir, 'rb') as file:
            try:
                data = load(file)
            except (EOFError, UnpicklingError):
                data = {}

        if not data:
            return {}

        return data

    def _set_value_in(self, name: str, value, values: dict | list):
        names = name.split(':', 1)

        if len(names) > 1:
            self._set_value_in(names[1], value, self.get(names[0]))
        elif isinstance(values, dict):
            values.update({name: value})
        elif isinstance(values, list):
            values[int(name)] = value

    def _get_value_from(self, name: str, values: dict | list) -> Any:
        value = None
        names = name.split(':', 1)

        if len(names) > 1:
            value = self._get_value_from(names[1], self.get(names[0]))
        elif isinstance(values, dict):
            value = values.get(name)
        elif isinstance(values, list):
            value = values[int(name)]

        return value

    def _flatten(self, values: dict | list, prefix: str = '') -> dict[str, Any]:
        flat_dict = {}

        for key, value in values.items():
            full_key = f'{prefix}:{key}' if prefix else key
            if isinstance(value, dict):
                flat_dict.update(self._flatten(value, full_key))
            elif isinstance(value, list):
                for i, list_value in enumerate(value):
                    flat_dict.update({f'{full_key}:{i}': list_value})
            else:
                flat_dict.update({full_key: value})

        return flat_dict
