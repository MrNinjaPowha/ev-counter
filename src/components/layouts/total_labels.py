from tkinter import Misc, IntVar
from tkinter.ttk import Label
from typing import Literal

from src.components.blocks.difference_label import DifferenceLabel
from src.variable_handler import VariableHandler

Values = Literal['evs', 'goals']


class TotalLabels:
    """A row of 3 ttk labels that will calculate the totals of evs, goals, and differences."""
    def __init__(self, master: Misc, variable_handler: VariableHandler, row: int = 0, first_column: int = 0):
        self.variable_handler = variable_handler

        self._values: dict[Values, IntVar] = {
            'evs': IntVar(master, 0),
            'goals': IntVar(master, 0)
        }

        self._evs_total = Label(master, textvariable=self._values.get('evs'))
        self._evs_total.grid(row=row, column=first_column)

        self._goals_total = Label(master, textvariable=self._values.get('goals'))
        self._goals_total.grid(row=row, column=first_column + 1)

        self._differences_total = DifferenceLabel(master)
        self._differences_total.grid(row=row, column=first_column + 2)

        # Add variable trackers
        for i in range(6):
            variable_handler.add_tracker(f'evs:{i}', self.update)
            variable_handler.add_tracker(f'goals:{i}', self.update)

    def update(self):
        """Recalculate all totals."""
        evs_total = 0
        goals_total = 0

        for i in range(6):
            evs_total += self.variable_handler.get_value(f'evs:{i}')
            goals_total += self.variable_handler.get_value(f'goals:{i}')

        self._values.get('evs').set(evs_total)
        self._values.get('goals').set(goals_total)
        self._differences_total.set_value(goals_total - evs_total)

        self.variable_handler.set_value('total:evs', evs_total)
        self.variable_handler.set_value('total:goals', goals_total)
        self.variable_handler.set_value('total:differences', goals_total - evs_total)
