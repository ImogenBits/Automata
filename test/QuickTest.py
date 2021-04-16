from automata.Tape import *
from automata.Symbol import *





class A:
    var = 1

    def __init__(self):
        self.pr()

    def pr(self):
        print(self.var)

class B(A):
    var = 2
    def __init__(self):
        print("ASDAS")
        super().__init__()


o: A
o = B()
