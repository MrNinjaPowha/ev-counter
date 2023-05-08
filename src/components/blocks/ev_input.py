from tkinter import Misc
from tkinter.ttk import Entry

from helpers.nullable_int_var import NullableIntVar
from variable_handler import VariableHandler


class EVInput(Entry):
    """A tkk entry that accepts numbers between 0 and 255. The value can be increased with add_evs() and whenever the
    value is changed the on_change callback will be called.
    """
    def __init__(
            self, master: Misc, variable_handler: VariableHandler, name: str, stat: int
    ):
        self.variable_handler = variable_handler
        self.name = name
        self.stat = stat

        self._value = NullableIntVar(master, 0)
        self._value.trace_add('write', lambda *_: self.parse_value())
        self._value.trace_add('write', lambda *_: variable_handler.set_value(f'{name}:{stat}', self._value.get()))
        variable_handler.add_tracker(
            # Update value on data load
            f'{name}:{stat}', lambda: self.add_evs(variable_handler.get_value(f'{name}:{stat}'))
        )
        variable_handler.add_tracker('generation', lambda: self.add_evs(0))

        super().__init__(
            master, width=3, textvariable=self._value, validate='all',
            validatecommand=(master.register(self.validate_input), '%P', '%s')
        )
        self.bind('<FocusOut>', self.on_focus_out)

    def add_evs(self, value: int):
        """Adds evs to the entry value. If the value parameter had increased the value above 255 or 252, depending on
        the generation, the final value would still not go above that value.
        """
        new_value = self.get_value() + value
        if new_value > self.get_max_value():
            new_value = self.get_max_value()
        if self.variable_handler.get_value(f'total:{self.name}') - self.get_value() + new_value > 510:
            new_value = self.get_value() + 510 - self.variable_handler.get_value(f'total:{self.name}')

        self._value.set(new_value)

    def get_value(self) -> int:
        """Returns the value of the entry."""
        return self._value.get()

    def get_max_value(self) -> int:
        """Returns the max ev that can be put into one stat."""
        return 255 if self.variable_handler.get_value('generation') == 0 else 252

    def on_focus_out(self, _event):
        """Sets value to zero if it was an empty string."""
        if not self._value.get():
            self._value.set(0)

    def parse_value(self):
        """Removes any leading zeroes."""
        value = self._value.get()
        if not value:
            value = ''

        self._value.set(value)

    def validate_input(self, new_value: str, old_value: str) -> bool:
        """Returns true if the value is an int between 0 and 255, is an empty string and the column total does not
        exceed 510.
        """
        if not new_value:
            return True
        if not new_value.isnumeric():
            return False
        if int(new_value) < 0 or int(new_value) > self.get_max_value():
            return False

        if not old_value.isnumeric():
            # Makes sure that int(old_value) will work
            old_value = '0'

        if self.variable_handler.get_value(f'total:{self.name}') - int(old_value) + int(new_value) > 510:
            return False

        return True
