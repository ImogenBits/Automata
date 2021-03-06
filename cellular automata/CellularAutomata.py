import itertools
import random

class CellularAutomata():
    def __init__(self, rule_number=120, already_in_base=False, neighborhood=3, states=('0', '1'),
                    random_first_row=False, width=100, colors=None, first_row=None):
        # Set up basic info about automata.
        self.neighborhood = neighborhood
        self.states = states
        self.rule_number = rule_number
        self.maximum_rule_number = len(self.states) ** (len(self.states) ** self.neighborhood)
        self.width = width

        if not colors:
            self.colors = {
                # Colors assigned to each possible state
                "0": (255, 255, 255),
                "1": (255, 144, 251),
                "2": (160, 220, 252),
            }
        else:
            self.colors = colors

        # `rule_input_keys` is the list of all combinations of the state that are `neighborhood`
        # ... characters in length in reverse order that they're provided, like so:
        # `['222', '221', '220' '212' '211' '210' '202', '201', '200' ...]`
        self.rule_input_keys = list(map(''.join, itertools.product(self.states, repeat=self.neighborhood)))[::-1]

        # Use own dictionary as input length
        #self.width = len(self.rule_input_keys)

        if rule_number:
            if not already_in_base:
                self.rule_number = self._convert_rule_to_base(rule_number)
            self.rule_dictionary = self._create_rule_dictionary()
        else:
            self.rule_dictionary = None

        # If we have a randomly assigned first row, randomly decide values for each cell
        if random_first_row:
            self.curr_row = [random.choice(self.states) for _ in range(self.width)]
        elif first_row:
            self.curr_row = list(first_row)
        elif not first_row:
            # Center the problem string on the first row
            self.curr_row = ['0' for _ in range(self.width)]
            self.curr_row[self.width//2] = '1'
        
        

    # Converts `rule_number` to target base `len(states)`, with a maximum value of...
    # ... `maximum_rule_number = len(states) ** (len(states) ** neighborohood)`
    # Anything above that just uses unnecessary computer cycles, as they're...
    # ... equivalent to `rule_number % maximum_rule_number`
    def _convert_rule_to_base(self, rule_number):
        # Treat 0 as special otherwise we're dividing by 0
        if rule_number == 0:
            # Return a number that's just the length of
            return ''.join(['0'] * (len(self.states) ** self.neighborhood))
        if rule_number > self.maximum_rule_number:
            rule_number = rule_number % self.maximum_rule_number
        # We will generate the new rule one digit at a time, so we'll add the digits to a list
        new_rule_number_digits = []
        # Generate each digit of the new rule number in the target base
        while rule_number:
            rule_number, remainder = divmod(rule_number, len(self.states))
            new_rule_number_digits.append(str(remainder))
        
        # Complicated. Rule numbers in Cellular Automata are defined by the following
        new_rule_number = ''.join(new_rule_number_digits)[::-1].zfill(len(self.states) ** self.neighborhood)
        return new_rule_number

    # Returns a dictionary of possible inputs to the digits of
    def _create_rule_dictionary(self):
        # Maps the keys produced to the digits of `rule_number`
        return dict(zip(self.rule_input_keys, self.rule_number))
    
    def _decide_value_for_cell(self, cell_index, rules):
        # First cell used
        p_cell = (cell_index - self.neighborhood//2)
        # Joins the current values for the cells and uses it as 
        input = "".join([self.curr_row[j % self.width] for j in range(p_cell, p_cell + self.neighborhood)])
        value = rules[input]
        return value

    # Expects a string similar to `011010001` to be passed in to determine the values of the rule outputs
    # `rule_values` is assumed to be in-base. We only check if it's the correct length to be used
    def advance_generation(self, rule_values=None):
        if rule_values:
            if len(rule_values) == len(self.rule_input_keys):
                # Use a custom transition function
                rule_dict = dict(zip(self.rule_input_keys, rule_values))
            else: # If the lengths don't match up...
                print("`rule_values` passed in is incorrect length to be used. Break time.")
                print("Length of rule_input_keys: " + str(len(self.rule_input_keys))
                    + "\nLength of rule_values: " + str(len(rule_values)))
                rule_dict = dict()
        else:
            rule_dict = self.rule_dictionary

        new_row = [self._decide_value_for_cell(cell_index, rule_dict) for cell_index in range(len(self.curr_row))]
        self.curr_row = new_row
