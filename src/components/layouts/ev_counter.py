from tkinter import Misc
from tkinter.ttk import Frame, Label, Separator

from src.variable_handler import VariableHandler
from .add_buttons import AddButtons
from ..blocks.difference_label import DifferenceLabel
from ..blocks.ev_input import EVInput
from ..blocks.total_label import TotalLabel


class EVCounter(Frame):
    """Handles the EV inputs and goals, and setups labels"""
    def __init__(self, master: Misc, variable_handler: VariableHandler):
        super().__init__(master, padding=2)

        self.variable_handler = variable_handler

        # labels
        for column, title in enumerate(['Add', 'EVs', 'Goal', 'Difference']):
            Label(self, text=title).grid(row=0, column=1 + column, padx=10)
        for column, title in enumerate(['HP', 'Atk', 'Def', 'Sp.Atk', 'Sp.Def', 'Speed']):
            Label(self, text=title).grid(row=1 + column, column=0, padx=10)

        Separator(self, orient='horizontal').grid(row=7, columnspan=6, sticky='EW', pady=5)
        Label(self, text='Total').grid(row=8)

        AddButtons(self, self.add_evs).grid(row=1, column=1, rowspan=6)

        for i in range(6):
            DifferenceLabel(self, variable_handler, (f'evs:{i}', f'goals:{i}')).grid(row=1 + i, column=4)

        TotalLabel(self, variable_handler, 'evs').grid(row=8, column=2)
        TotalLabel(self, variable_handler, 'goals').grid(row=8, column=3)
        DifferenceLabel(self, variable_handler, ('total:evs', 'total:goals')).grid(row=8, column=4)

        self.ev_inputs = []
        for i in range(6):
            self.ev_inputs.append(EVInput(self, variable_handler, 'evs', i))
            self.ev_inputs[i].grid(row=1 + i, column=2)

            # goal inputs
            EVInput(self, variable_handler, 'goals', i).grid(row=1 + i, column=3)

    def add_evs(self, stat: int, value: int, shift_down: bool = False):
        """Adds evs to the specified stat.

        If shift_down is true then the extra evs gained from held items will be ignored
        """
        generation = self.variable_handler.get_value('generation')
        item = self.variable_handler.get_value('item')
        pokerus_multiplier = 2 if self.variable_handler.get_value('has_pokerus') else 1

        if item == 0 or shift_down:
            # No item held means no special case, shift key can also be used to ignore held item
            self.ev_inputs[stat].add_evs(pokerus_multiplier * value)
        elif item == 1:
            # Macho Brace doubles EV increase
            self.ev_inputs[stat].add_evs(2 * pokerus_multiplier * value)
        else:
            # Power Items increase a specific stat by 4 (8 after Gen 7)
            extra_evs = 4 if generation == 0 else 8
            self.ev_inputs[stat].add_evs(pokerus_multiplier * value)
            self.ev_inputs[item - 2].add_evs(pokerus_multiplier * extra_evs)
