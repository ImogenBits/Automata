from automata.Tape import *
from automata.Symbol import *


z = Symbol("0")
a = Symbol("a")
b = Symbol("b")
c = Symbol("c")
d = Symbol("d")


aTape = Tape(z)
aTape.input([a, b, c, d] * 10, -10)

#bTape = aTape[5:10]
cTape = aTape[5:-10:-2]



print(aTape)