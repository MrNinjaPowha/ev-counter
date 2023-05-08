from tkinter import Variable, TclError, Misc


class NullableIntVar(Variable):
    """An extended tk variable that works like the IntVar but can also be an empty string."""
    def __init__(self, master: Misc = None, value=None, name: str = None):
        super().__init__(master, value, name)

    def get(self):
        """Return the value of the variable as an integer."""
        value = self._tk.globalgetvar(self._name)
        if not value:
            return 0
        try:
            return self._tk.getint(value)
        except (TypeError, TclError):
            return int(self._tk.getdouble(value))
