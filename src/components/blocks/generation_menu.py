from tkinter import StringVar, Misc
from tkinter.ttk import OptionMenu

from variable_handler import VariableHandler


class GenerationMenu(OptionMenu):
    """A ttk option-menu with options for generations where the EV mechanics differ."""
    def __init__(self, master: Misc, variable_handler: VariableHandler):
        self.generations = [
            'Gen I-VI',
            'Gen VII+'
        ]

        self._value = StringVar(master, self.generations[0])
        self._value.trace_add('write', lambda *_: variable_handler.set_value('generation', self.get_generation()))
        variable_handler.add_tracker(
            'generation', lambda: self._value.set(self.generations[variable_handler.get_value('generation')])
        )
        super().__init__(master, self._value, self._value.get(), *self.generations)

    def get_generation(self) -> int:
        """Returns the list index for the value of the option button."""
        return self.generations.index(self._value.get())
