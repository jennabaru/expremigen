import itertools
import math

from expremigen.pattern import Pattern
from expremigen.pattern import flatten

class Pconst(Pattern):
    def __init__(self, constant=0, repeats=math.inf):
        super().__init__()
        self.constant = constant
        self.repeats = repeats

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__, self.constant, self.repeats)

    def __iter__(self):
        return flatten(c for c in itertools.repeat(self.constant, self.repeats))
