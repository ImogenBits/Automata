from automata.Tape import *
from automata.Symbol import *
from automata.CellularAutomaton import *






ca = CellularAutomaton(94)
log = CALog(ca, 10, 200, 100)

ca([Symbol("1", (1, 1, 1))], log, 100)

log.createImage().show()