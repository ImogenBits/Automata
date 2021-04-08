from automata.Symbol import Alphabet, Symbol
from automata.CellularAutomaton import CellularAutomaton, CALog
from automata.Tape import Tape


Zero = Symbol("0", color = (200, 200, 200))
One = Symbol("1", color = (50, 50, 50))

ca = CellularAutomaton(18, 3, Alphabet([Zero, One]), Zero)

if __name__ == "__main__":
    log = CALog(ca, 10, 250)
    ca(Tape(Zero, [One]), log = log)
    log.createImage().show()