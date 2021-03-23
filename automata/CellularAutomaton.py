from __future__ import annotations
import itertools
import random
from PIL import Image, ImageDraw
from collections import deque
from os import error

from automata.Symbol import Symbol, SymbolIter
from automata.Tape import Tape

Color = tuple[int, int, int]
RuleDict = dict[tuple[Symbol, ...], Symbol]
RuleNumber = int

def digitAt(num: int, pos: int, base: int = 10) -> int:
    return (num // (base ** pos)) % base

def anyGeneric(input: tuple[Symbol, ...]) -> bool:
    for s in input:
        if s.isGeneric:
            return True
    return False


class RuleFunc:
    def __init__(self,
                 rule: RuleDict | RuleNumber,
                 neighborhoood: int,
                 alphabet: set[Symbol] | list[Symbol]
                 ) -> None:
        self.dict: RuleDict = {}
        if isinstance(rule, RuleNumber) and isinstance(alphabet, list):
            i = 0
            l = len(alphabet)
            for comb in itertools.product(alphabet, repeat=neighborhoood):
                self.dict[comb] = alphabet[digitAt(rule, i, l)]
                i += 1
        elif isinstance(rule, dict) and isinstance(alphabet, set):
            for input, output in rule.items():
                if anyGeneric(input):
                    for tup, out in SymbolIter(input, output, alphabet):
                        self.dict[tup] = out
                else:
                    self.dict[input] = output
        else:
            raise error(f"""Created a RuleFunc with RuleNumber {rule}
                            but the alphabet was a set""")
    
    def __call__(self, input: tuple[Symbol, ...]) -> Symbol:
        return self.dict[input]

class CellularAutomaton:
    def __init__(self,
                 rule: RuleFunc | RuleDict | RuleNumber,
                 neighborhood: int = 3,
                 alphabet: set[Symbol] | list[Symbol] = {Symbol("0"), Symbol("1")},
                 blank: Symbol = Symbol("0")
                 ) -> None:
        self.neighborhood = neighborhood
        self.blank = blank
        self.alphabet = alphabet.copy()
        alphSize = len(self.alphabet)
        self.maximumRuleNumber = alphSize ** (alphSize ** self.neighborhood)

        if isinstance(rule, RuleFunc):
            self.ruleFunc = rule
        else:
            self.ruleFunc = RuleFunc(rule, neighborhood, alphabet)

        self.tape = Tape(blank)
    
    def reset(self):
        self.tape.clear()

    def getID(self) -> tuple[Tape, int, int]:
        a, b = self.tape.bounds()
        return (self.tape.copy(), a, b)

    def step(self):
        hasChanged = False
        neighborhood = self.neighborhood
        left, right = self.tape.bounds()
        buffer = deque([self.blank] * neighborhood,
                        maxlen = neighborhood)
        cOff = self.neighborhood // 2
        for i in range(left - neighborhood, right):
            tape = self.tape
            buffer.append(tape.read(i + neighborhood - 1))
            newSymbol = self.ruleFunc(tuple(buffer))
            if tape.read(i + cOff) != newSymbol:
                hasChanged = True
                tape.write(i + cOff, newSymbol)
        if not hasChanged:
            self.shouldHalt = True

    def __call__(self,
                 input: list[Symbol] |None = None,
                 randInputlength: int | None = None,
                 log: CALog | None = None,
                 ) -> list[Symbol]:
        self.reset()
        if input is not None:
            self.tape.input(input)
        elif input is None and randInputlength:
            alphList = list(self.alphabet)
            self.tape.input([random.choice(alphList)
                             for _ in range(randInputlength)])
        else:
            raise error("provide either input or randInputLength")

        self.shouldHalt = False
        if log is None:
            while not self.shouldHalt:
                self.step()
        else:
            i = 0
            log.log()
            while not self.shouldHalt and i <= 100:
                self.step()
                i += 1
                log.log()


        return self.tape.asList()


class CALog:
    def __init__(self,
                 ca: CellularAutomaton,
                 scale: int = 1,
                 width: int | None = 200,
                 generations: int | None = 100
                 ) -> None:
        self.ca = ca
        self.scale = scale
        self.width = width
        self.buffer = 3 * scale
        self.generations = generations
        self.arr: list[tuple[Tape, int, int]] = []

    def log(self) -> None:
        self.arr.append(self.ca.getID())

    def createImage(self) -> None:
        if self.width is None:
            self.width = 0
            for (l, _, _) in self.arr:
                le = len(l)
                if le > self.width:
                    self.width = le

        if self.generations is None:
            self.generations = len(self.arr)

        _, start, end = self.arr[0]
        for (_, a, b) in self.arr:
            if a < start:
                start = a
            if end < b:
                end = b
        
        if end - start <= self.width:
            imStart = start
        else:
            startLen = len(self.arr[0][0])
            imStart = -((self.width - startLen) // 2)
        

        imWidth = self.scale * self.width + 2 * self.buffer
        imHeight = self.scale * self.generations + 2 * self.buffer


        self.image = Image.new("RGB", (imWidth, imHeight), "#000000")
        image = ImageDraw.ImageDraw(self.image)

        for i, (gen, start, end) in enumerate(self.arr):
            arr: list[Symbol] = []
            if imStart <= start:
                arr = [self.ca.blank] * (start - imStart)
            arr += gen
            if len(arr) < self.width:
                arr += [self.ca.blank] * (self.width - len(arr))
            elif len(arr) > self.width:
                arr = arr[:self.width]

            for j, symbol in enumerate(arr):
                x = self.buffer + self.scale * j
                y = self.buffer + self.scale * i
                image.rectangle([x, y, x + self.scale, y + self.scale],
                                fill = symbol.color)
        
        self.image.show()
