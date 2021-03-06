from automata.TuringMachine import TransDict, TuringMachine, Direction
from automata.Symbol import Symbol

X = Symbol("X", True)

T0 = Symbol("0")
T1 = Symbol("1")
H = Symbol("#")

A  = Symbol("A")
S1  = Symbol("S1")
S2  = Symbol("S2")
P0  = Symbol("P0")
P1  = Symbol("P1")
C  = Symbol("C")
M0  = Symbol("M0")
M1  = Symbol("M1")
MA  = Symbol("MA")

L, N, R = Direction.L, Direction.N, Direction.R


states = set(range(78))
inputAlph = {
    T0,
    T1,
    H
}
B = Symbol("B")
tapeAlph = {
    Symbol("A"),
    Symbol("S1"),
    Symbol("S2"),
    Symbol("P0"),
    Symbol("P1"),
    Symbol("C"),
    Symbol("M0"),
    Symbol("M1"),
    Symbol("MA")
}.union(inputAlph).union({B})
finalStates = {
    51,
    73
}
transDict: TransDict
transDict = {
     0:{X: (1, X, L)},
     1:{X: (2, S1, L)},
     2:{X: (3, A, R)},
     3:{X: (3, X, R),
        H: (4, S2, R)},
     4:{T0: (4, T0, R),
        T1: (4, T1, R),
        H: (5, H, L),
        B: (5, B, L),
        P0:(5, T0, L),
        P1:(5, T1, L)},
     5:{T0: (6, P0, L),
        T1: (12, P1, L),
        S2:(74, S2, L)},
     6:{X: (6, X, L),
        S1:(7, S1, R)},
     7:{T0: (7, T0, R),
        T1: (7, T1, R),
        H: (8, H, L),
        S2:(8, S2, L),
        P0:(8, T0, L),
        P1:(8, T1, L)},
     8:{T0: (9, P0, L),
        T1: (11, P1, L),
        S1: (25, S1, L)},
     9:{X: (9, X, L),
        B: (10, T0, R),
        C: (10, T1, R)},
    10:{X: (10, X, R),
        S2: (4, S2, R)},
    11:{X: (11, X, L),
        B: (10, T1, R),
        C: (16, T0, L)},
    12:{X: (12, X, L),
        S1: (13, S1, R)},
    13:{T0: (13, T0, R),
        T1: (13, T1, R),
        H: (14, H, L),
        S2: (14, S2, L),
        P0: (14, T0, L),
        P1: (14, T1, L)},
    14:{T0: (11, P0, L),
        T1: (15, P1, L),
        S1: (26, S1, L)},
    15:{X: (15, X, L),
        B: (16, T0, L),
        C: (16, T1, L)},
    16:{B: (10, C, R)},
    17:{T0: (17, T0, R),
        T1: (17, T1, R),
        H: (18, H, L),
        S2: (18, S2, L),
        P0: (18, T0, L),
        P1: (18, T1, L)},
    18:{T0: (19, P0, L),
        T1: (20, P1, L),
        S1: (29, S1, L)},
    19:{X: (19, X, L),
        B: (21, T0, R),
        C: (21, T1, R)},
    20:{X: (20, X, L),
        B: (21, T1, R),
        C: (22, T0, L)},
    21:{X: (21, X, R),
        S1: (17, S1, R)},
    22:{B: (21, T1, R)},
    23:{T0: (23, T0, R),
        T1: (23, T1, R),
        H: (24, H, L),
        B: (24, B, L),
        P0: (24, T0, L),
        P1: (24, T1, L)},
    24:{T0: (25, P0, L),
        T1: (26, P1, L),
        S2: (29, S2, L)},
    25:{X: (25, X, L),
        B: (27, T0, R),
        C: (27, T1, R)},
    26:{X: (26, X, L),
        B: (27, T1, R),
        C: (28, T0, L)},
    27:{X: (27, X, R),
        S2: (23, S2, R)},
    28:{B: (27, T1, R)},
    29:{X: (29, X, L),
        A: (30, A, L)},
    30:{T0: (31, T0, L),
        X: (75, X, L)},
    31:{T0: (32, T0, L),
        X: (75, X, L)},
    32:{T1: (33, T1, L),
        X: (75, X, L)},
    33:{T0: (34, T0, L),
        X: (75, X, L)},
    34:{T0: (35, T0, L),
        X: (75, X, L)},
    35:{T1: (36, T1, L),
        X: (75, X, L)},
    36:{T1: (37, T1, L),
        X: (75, X, L)},
    37:{T1: (38, T1, L),
        X: (75, X, L)},
    38:{T1: (39, T1, L),
        X: (75, X, L)},
    39:{T1: (40, T1, L),
        X: (75, X, L)},
    40:{T1: (41, T1, L),
        X: (75, X, L)},
    41:{T0: (41, T0, L),
        B: (43, B, R),
        X: (75, X, L)},
    43:{X: (43, B, R),
        A: (44, MA, L)},
    44:{B: (52, P0, R)},
    45:{X: (45, X, L),
        B: (46, B, R)},
    46:{X: (46, B, R),
        A: (47, A, R)},
    47:{X: (47, X, R),
        S2: (48, H, R)},
    48:{X: (48, X, R),
        B: (49, B, L),
        H: (4, S2, R)},
    49:{X: (49, X, L),
        S1: (50, H, R)},
    50:{X: (50, X, R),
        H: (48, S1, R),
        B: (51, B, R)},
    51:{},
    52:{X: (52, X, R),
        S2: (53, S2, R)},
    53:{T0: (53, T0, R),
        T1: (53, T1, R),
        H: (54, H, L),
        B: (54, B, L),
        P0: (54, T0, L),
        P1: (54, T1, L)},
    54:{T0: (55, P0, L),
        T1: (58, P1, L),
        S2: (72, S2, L)},
    55:{X: (55, X, L),
        M0: (56, T0, L),
        M1: (56, T1, L),
        MA: (56, A, L)},
    56:{P0: (57, M0, L),
        P1: (57, M1, L)},
    57:{T0: (52, P0, R),
        T1: (52, P1, R),
        B: (52, P0, R)},
    58:{X: (58, X, L),
        S1: (59, S1, R)},
    59:{T0: (59, T0, R),
        T1: (59, T1, R),
        X: (60, X, L),
        P0: (60, T0, L),
        P1: (60, T1, L)},
    60:{T0: (61, P0, L),
        T1: (65, P1, L),
        S1: (68, S1, L)},
    61:{X: (61, X, L),
        A: (62, A, L),
        MA: (62, MA, L)},
    62:{X: (62, X, L),
        P0: (63, T0, L),
        P1: (63, T1, L)},
    63:{T0: (64, P0, R),
        T1: (64, P1, R),
        B: (64, P0, R)},
    64:{X: (64, X, R),
        S1: (59, S1, R)},
    65:{X: (65, X, L),
        A: (66, A, L),
        MA: (66, MA, L)},
    66:{X: (66, X, L),
        P0: (67, T1, L),
        P1: (76, T0, L)},
    67:{T0: (64, P0, R),
        T1: (64, P1, R),
        B: (64, P0, R)},
    68:{X: (68, X, L),
        P0: (69, T0, R),
        P1: (69, T1, R)},
    69:{X: (69, X, R),
        M0: (70, T0, L),
        M1: (70, T1, L),
        MA: (70, A, L)},
    70:{T0: (71, M0, L),
        T1: (71, M1, L)},
    71:{T0: (52, P0, R),
        T1: (52, P1, R)},
    72:{X: (72, X, L),
        MA: (72, B, L),
        A: (72, B, L),
        P0: (72, T0, L),
        P1: (72, T1, L),
        M0: (72, T0, L),
        M1: (72, T1, L),
        B: (73, B, R)},
    73:{},
    74:{X: (74, X, L),
        S1: (17, S1, R)},
    75:{X: (45, X, L)},
    76:{T1: (77, P0, L),
        T0: (64, P1, R),
        B: (64, P1, R)},
    77:{T1: (77, T0, L),
        T0: (64, T1, R),
        B: (64, T1, R)}
}


tm = TuringMachine(
    states,
    tapeAlph,
    B,
    inputAlph,
    0,
    finalStates,
    transDict
)

def transformInput(inputList: list[str]) -> list[Symbol]:
    res = ""
    for line in inputList:
        res += "#" + "{:b}".format(int(line.strip()))
    return [Symbol(c) for c in res[1:]]

inputWord: list[Symbol] = []

with open("test big input.txt", "r") as f:
    inputWord = transformInput(f.readlines())

tm(inputWord)