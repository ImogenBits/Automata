import random

class TuringMachine():
    def __init__(self, states=('A', 'B'), starting_state='A', alphabet=('0', '1', '2'),
            # Wolfram's (2, 3), Turing Machine
            transition_function={'A':{'0':('1',1,'B'), '1':('2',-1,'A'), '2':('1',-1,'A')},
                                'B':{'0':('2',-1,'A'), '1':('2',1,'B'), '2':('0',1,'A')}},
            halting_state=None, tape_length=None, random_start=False, pointer=None, colors=None):
        self.states = states
        self.state = starting_state
        self.alphabet = alphabet
        self.transition_function = transition_function 
        self.halting_state = halting_state

        if not colors:
            self.colors = {
                "A": (255, 150, 0),     # Orange
                "B": (50, 190, 0),      # Green

                # Colors assigned to each possible state
                "0": (255, 255, 255),         # Black
                "1": (255, 144, 251),   # White
                "2": (160, 220, 252),       # Blue
            }
        else:
            self.colors = colors

        # If the tape has a maximum length, it will automatically wrap-around.
        self.tape_length = tape_length
        if random_start:
            self.tape = [random.choice(self.alphabet) for _ in range(tape_length)]
        else:
            self.tape = ['0' for _ in range(tape_length)]
        # Set up point at midway point
        if pointer:
            self.pointer = min(pointer, tape_length-1)
        elif tape_length and not pointer:
            self.pointer = tape_length//2

    def advance_generation(self):
        if self.state != self.halting_state:
            # Select the rule based on the TM State and the value under the pointer
            rule = self.transition_function[self.state][self.tape[self.pointer]]
            self.tape[self.pointer] = rule[0]
            self.pointer = (self.pointer + rule[1]) % self.tape_length
            if rule[2] in self.states:
                self.state = rule[2]
            else:
                self.state = 'pass' # haha try debugging this later, you stupid bitch
