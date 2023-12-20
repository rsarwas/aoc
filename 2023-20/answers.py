"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
from collections import namedtuple
from queue import SimpleQueue

INPUT = "input.txt"
HIGH = 1
LOW = 0

Action = namedtuple("Action", "source pulse destination")


class Broadcaster:
    """Module is protocol or an abstract super class.
    It servers to document the required methods of all
    the module classes define below.
    This isn't very Pythonic, but it helps me understand how the classes should work

    destinations is a list of module names. When a pulse is received  and the conditions are
    correct, this module will send a pulse (create an action in the FIFO queue), to each of the
    destinations in order."""

    def __init__(self, destinations) -> None:
        """Initialize the module with a list of destination modules"""
        self.destinations = destinations

    def is_default(self):
        """Is this class in it's default state.
        If all of the modules are in the default state, then we have finished a loop"""
        return True

    def receive(self, action, queue):
        """Update internal state and and if appropriate, send pulses."""
        me = action.destination
        self.send(me, action.pulse, queue)

    def send(self, me, pulse, queue):
        """Send (add action to queue) pulse from me to all my destinations."""
        for target in self.destinations:
            new_action = Action(me, pulse, target)
            queue.put(new_action)
            # print(f"{me} -> {pulse} -> {target}")


class Flipflop(Broadcaster):
    """Flip-flop modules are either on or off; they are initially off."""

    def __init__(self, destinations) -> None:
        super().__init__(destinations)
        self.state = "off"

    def is_default(self):
        """Is this class in it's default state."""
        return self.state == "off"

    def receive(self, action, queue):
        """If a flip-flop module receives a high pulse, it is ignored and
        nothing happens. However, if a flip-flop module receives a low pulse,
        it flips between on and off. If it was off, it turns on and sends a
        high pulse. If it was on, it turns off and sends a low pulse."""
        me = action.destination
        if action.pulse == HIGH:
            return
        if self.state == "on":
            self.state = "off"
            self.send(me, LOW, queue)
        else:
            self.state = "on"
            self.send(me, HIGH, queue)


class Conjunction(Broadcaster):
    """Conjunctions remember the type of the most recent pulse received from each of
    their connected input modules; they initially default to remembering a low pulse
    for each input."""

    def __init__(self, destinations) -> None:
        super().__init__(destinations)
        self.memory = {}

    def add_input(self, source):
        """Needs to set the memory to low for each input"""
        self.memory[source] = LOW

    def is_default(self):
        """Returns True IFF all the previous inputs are LOW"""
        return self.all(LOW)

    def all(self, state):
        """Returns True IFF all the previous inputs have the same state"""
        for pulse in self.memory.values():
            if pulse != state:
                return False
        return True

    def receive(self, action, queue):
        """When a pulse is received, the conjunction module first updates its
        memory for that input. Then, if it remembers high pulses for all inputs, it sends a
        low pulse; otherwise, it sends a high pulse."""
        source = action.source
        me = action.destination
        pulse = action.pulse
        self.memory[source] = pulse
        if self.all(HIGH):
            self.send(me, LOW, queue)
        else:
            self.send(me, HIGH, queue)


def part1(lines):
    """Solve part 1 of the problem."""
    modules = parse(lines)
    initialize_conjunctions(modules)
    button_press = Action("button", LOW, "broadcaster")
    n = 1000
    high_low, low_count = process(n, button_press, modules)
    return high_low * low_count


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    modules = {}
    for line in lines:
        line = line.strip()
        name, destinations = line.split(" -> ")
        destinations = destinations.split(", ")
        if name == "broadcaster":
            module = Broadcaster(destinations)
        else:
            kind = name[0]
            name = name[1:]
            if kind == "&":
                module = Conjunction(destinations)
            else:  # kind == "%"
                module = Flipflop(destinations)
        modules[name] = module
    return modules


def initialize_conjunctions(modules):
    """Conjunctions need to know all of their inputs."""
    for name, conjunction in modules.items():
        if isinstance(conjunction, Conjunction):
            for source, other_module in modules.items():
                if name in other_module.destinations:
                    conjunction.add_input(source)


def process(max_n, initial_action, modules):
    """Process actions n times and return the number of high and low pulses sent.
    If all the modules are in their default state after a button push, then the
    next push will repeat the same cycle as though the initial button was pushed."""
    high_low, low_count = 0, 0
    default_state = False
    n = 0
    while not default_state and n < max_n:
        n += 1
        actions = SimpleQueue()
        actions.put(initial_action)
        while not actions.empty():
            action = actions.get()
            # print(f"{action.source} -> {action.pulse} -> {action.destination}")
            if action.pulse == LOW:
                low_count += 1
            else:  # action.pulse == HIGH
                high_low += 1
            try:
                module = modules[action.destination]
            except KeyError:
                # print(f"pulse set to {action.destination} diverted to /dev/null")
                continue
            module.receive(action, actions)
        default_state = all_default(modules)
        # print(n, high_low, low_count, default_state)
    multiple = max_n // n
    if max_n % n != 0:
        print(f"1000 not divisible by cycle size {n}")
    return high_low * multiple, low_count * multiple


def all_default(modules):
    """Return True is all the modules are in their default state."""
    for module in modules.values():
        if not module.is_default():
            return False
    return True


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
