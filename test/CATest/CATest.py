from automata.Symbol import Symbol
from automata.CellularAutomaton import CellularAutomaton, CALog


Zero = Symbol("0", color = (200, 200, 200))
One = Symbol("1", color = (50, 50, 50))

ca = CellularAutomaton(18, 3, [Zero, One], Zero)

if __name__ == "__main__":
    log = CALog(ca, 10, None, None)
    ca([One], log = log)
    log.createImage()
    print(1)