from TuringMachine import TM, Dir, Special

def transformInput(inputList):
    res = ""
    for line in inputList:
        res += "#" + "{:b}".format(int(line.strip()))
    return [c for c in res[1:]]

# making things easier to type
L, N, R = Dir.L, Dir.N, Dir.R
X = Special.X
B = "B"
a, b, c, T = "a", "b", "c", "T"
numStates = 4

# data that defines the TM
states = {i for i in range(numStates)}
sigma = {a, b, c}
gamma = sigma.union({T})
final = {3}
delta = {
    0: {T: (T, L, 0),
        B: (B, R, 3),
        b: (b, L, 0),
        a: (T, R, 1)},
    1: {a: (a, R, 1),
        T: (T, R, 1),
        b: (T, R, 2)},
    2: {b: (b, R, 2),
        T: (T, R, 2),
        c: (T, L, 0)},
}


tm = TM(states, gamma, B, sigma, 0, final, delta)

inputWord = "aaabbbccc"


tm(inputWord, False, True)