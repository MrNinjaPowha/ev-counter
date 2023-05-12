from tkinter import IntVar, Misc
from tkinter.ttk import Label

from src.variable_handler import VariableHandler


class TotalLabel(Label):
    """A ttk label that will calculate the total of a column of 6 inputs."""
    def __init__(self, master: Misc, variable_handler: VariableHandler, total_of: str):
        self.variable_handler = variable_handler
        self.total_of = total_of

        self._value = IntVar(master, 0)
        super().__init__(master, textvariable=self._value)

        for i in range(6):
            variable_handler.add_tracker(f'{total_of}:{i}', self.recalculate)

    def recalculate(self):
        """Recalculates and sets the new total."""
        total = 0

        for i in range(6):
            total += self.variable_handler.get_value(f'{self.total_of}:{i}')

        self._value.set(total)
        self.variable_handler.set_value(f'total:{self.total_of}', total)
