from automata.Tape import *
from automata.Symbol import *

z = Symbol("0")
a = Symbol("a")
b = Symbol("b")
c = Symbol("c")
d = Symbol("d")


aTape = Tape(z)
aTape.input([a, b, c, a, b, c, a, b, c], -3)

bTape = aTape[::]
cTape = aTape[:10:]

print(aTape)