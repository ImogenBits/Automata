from __future__ import annotations
from automata.Automaton import Automaton
from automata.CellularAutomaton import CellularAutomaton
from automata.Tape import Tape
from PIL import Image, ImageDraw

class Log:
    def __init__(self,
                 automaton: Automaton,
                 scale: int = 10,
                 width: int | None = 200,
                 generations: int | None = 100,
                 ) -> None:
        self.automaton = automaton
        self.scale = scale
        self.width = width
        self.generations = generations
        self.arr: list[Tape] = []


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