import numpy as np


class Metric:
    def __init__(self):
        self.values = []

    def add_measure(self, value):
        self.values.append(value)

    def all_nan(self):
        return all(np.isnan(x) for x in self.values)

    def apply(self, np_function):
        if self.all_nan():
            return 0
        return float(np_function(self.values))

    def min(self):
        return self.apply(np.nanmin)

    def max(self):
        return self.apply(np.nanmax)

    def sum(self):
        return self.apply(np.nansum)

    def avg(self):
        values = [n for n in self.values if not np.isnan(n)]
        if len(values) == 0:
            return 0
        return self.sum() / len(values)

    def last(self):
        values = [n for n in self.values if not np.isnan(n)]
        return values[-1] if values else None