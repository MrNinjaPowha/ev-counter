import os
from pickle import dump, load, UnpicklingError
from typing import Any, Callable


class VariableHandler(dict):
    """A dict containing values for the EVCounter. To access a nested value separate the different levels with a colon.
    If the value being accessed is in a list, just put the index after the last colon.

    Examples: 'generation', 'total:evs', 'goals:3'
    """
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
        """Sets a value in self."""
        self._set_value_in(name, value, self)
        if self._trackers.get(name):
            for tracker in self._trackers.get(name):
                tracker()

    def get_value(self, name: str) -> Any:
        """Returns a value from self."""
        return self._get_value_from(name, self)

    def add_tracker(self, name: str, callback: Callable[[], Any]):
        """Add a tracker for a value in self.
        :param name: the name of the value to track.
        :param callback: the function to be called when the value is changed.
        """
        if self._trackers.get(name):
            self._trackers.get(name).append(callback)
        else:
            self._trackers.update({name: [callback]})

    def save_pokemon(self, name: str):
        """Saves the current values in self under the specified name."""
        data = self._load_data()
        data.update({name: self._flatten(self)})

        with open(self.data_dir, 'wb') as file:
            dump(data, file)

    def load_pokemon(self, name: str):
        """Loads values of the Pokémon with the specified name and sets all values in self."""
        data = self._load_data()

        for key, value in data.get(name).items():
            self.set_value(key, value)

    def get_saved_pokemons(self) -> list[str]:
        """Returns a list of all the saved Pokémon names."""
        data = []

        for value in sorted(self._load_data().keys()):
            data.append(value)

        return data

    def _load_data(self) -> dict[str, dict[str, Any]]:
        """Returns a dict with the saved data values. If the file does not exist it will be created as an empty file."""
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
        """A recursive function that will split the name parameter at ':' and go through the values parameter, which
        should at first be self, to find and set the specified value.
        """
        names = name.split(':', 1)

        if len(names) > 1:
            self._set_value_in(names[1], value, self.get(names[0]))
        elif isinstance(values, dict):
            values.update({name: value})
        elif isinstance(values, list):
            values[int(name)] = value

    def _get_value_from(self, name: str, values: dict | list) -> Any:
        """A recursive function that will split the name parameter at ':' and go through the values parameter, which
        should at first be self, to find and return the specified value.
        """
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
        """A recursive function that will return the variable handler as a dict where all inner dicts and lists have
        been flattened and are indexed with keys in the same style as the name parameter in the get and set functions.
        """
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
