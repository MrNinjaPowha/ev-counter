from tkinter import StringVar, Misc
from tkinter.ttk import OptionMenu

from src.variable_handler import VariableHandler


class ItemMenu(OptionMenu):
    """A ttk option-menu with options for all the different EV-training held items."""
    def __init__(self, master: Misc, variable_handler: VariableHandler):
        self.items = [
            'None',
            'Macho Brace',
            'Power Weight',
            'Power Bracer',
            'Power Belt',
            'Power Lens',
            'Power Band',
            'Power Anklet'
        ]

        self._value = StringVar(master, self.items[0])
        self._value.trace_add('write', lambda *_: variable_handler.set_value('item', self.get_item()))
        variable_handler.add_tracker(
            'item', lambda: self._value.set(self.items[variable_handler.get_value('item')])
        )
        super().__init__(master, self._value, self._value.get(), *self.items)

    def get_item(self) -> int:
        """Returns the list index for the value of the option button."""
        return self.items.index(self._value.get())
