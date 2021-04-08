from __future__ import annotations
import itertools
import random
from typing import Sequence
from PIL import Image, ImageDraw
from collections import deque
from os import error

from automata.Symbol import Alphabet, Symbol, SymbolIter
from automata.Tape import Tape

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
                 alphabet: Alphabet
                 ) -> None:
        self.dict: RuleDict = {}
        if isinstance(rule, RuleNumber):
            i = 0
            l = len(alphabet)
            for comb in itertools.product(alphabet, repeat=neighborhoood):
                self.dict[comb] = alphabet[digitAt(rule, i, l)]
                i += 1
        else:
            for input, output in rule.items():
                if anyGeneric(input):
                    for tup, out in SymbolIter(input, output, alphabet):
                        self.dict[tup] = out
                else:
                    self.dict[input] = output
    
    def __call__(self, input: tuple[Symbol, ...]) -> Symbol:
        return self.dict[input]

class CellularAutomaton:
    def __init__(self,
                 rule: RuleFunc | RuleDict | RuleNumber,
                 neighborhood: int = 3,
                 alphabet: Alphabet = Alphabet({Symbol("0"), Symbol("1")}),
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

    def getID(self) -> Tape:
        return self.tape.copy()

    def step(self) -> bool:
        hasChanged = False
        tape = self.tape
        neighborhood = self.neighborhood
        left, right = tape.bounds()
        buffer = deque([self.blank] * neighborhood, maxlen = neighborhood)
        cOff = self.neighborhood // 2
        for i in range(left - neighborhood + 1, right + 1):
            buffer.append(tape.read(i + neighborhood - 1))
            newSymbol = self.ruleFunc(tuple(buffer))
            if tape.read(i + cOff) != newSymbol:
                hasChanged = True
                tape.write(i + cOff, newSymbol)
                pass
        return not hasChanged

    def __call__(self,
                 input: Sequence[Symbol] | None = None,
                 randInputlength: int | None = None,
                 log: CALog | None = None,
                 steps: int | None = None
                 ) -> Tape:
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
            if steps is None:
                while not self.step():
                    pass
            else:
                i = 0
                while i < steps and not self.step():
                    pass
        else:
            if steps is None:
                log.log()
                while not self.step():
                    log.log()
                log.log()
            else:
                i = 0
                log.log()
                while i < steps and not self.step():
                    log.log()
                log.log()

        return self.tape.copy()


class CALog:
    def __init__(self,
                 ca: CellularAutomaton,
                 scale: int = 10,
                 width: int | None = 200,
                 generations: int | None = 100
                 ) -> None:
        self.ca = ca
        self.scale = scale
        self.width = width
        self.generations = generations
        self.arr: list[Tape] = []

    def log(self) -> None:
        self.arr.append(self.ca.getID())
        pass

    def createImage(self) -> Image.Image:
        generations, width = self.generations, self.width
        if generations is None:
            generations = len(self.arr)
        arr = self.arr[:generations]

        if width is None:
            width = 0
            for t in arr:
                width = max(width, len(t))
                
        lBound, rBound = 0, 0
        for t in arr:
            l, r = t.bounds()
            lBound = min(lBound, l)
            rBound = max(rBound, r)
        
        if rBound - lBound <= width:
            imStart = lBound - ((width - (rBound - lBound)) // 2)
        else:
            imStart = -((width - len(arr[0])) // 2)
        imEnd = imStart + width

        buffer = 3 * self.scale
        imWidth = self.scale * width + 2 * buffer
        imHeight = self.scale * generations + 2 * buffer

        self.image = Image.new("RGB", (imWidth, imHeight), "#000000")
        image = ImageDraw.ImageDraw(self.image)

        for i, t in enumerate(arr):
            for j, symbol in enumerate(t.copy(imStart, imEnd)):
                x = buffer + self.scale * j
                y = buffer + self.scale * i
                image.rectangle([x, y, x + self.scale, y + self.scale],
                                fill = symbol.color)

        return self.image
