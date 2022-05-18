from bisect import insort

class Atom:
    def __init__(self):
        self.items = []

    def append(self, val):
        insort(self.items, val)

    def pop_big(self):
        return self.items.pop()

    def pop_small(self):
        return self.items.pop(0)

class Component:
    def __init__(self, inputs, output_count):
        self.inputs = inputs
        self.output_queues = [[]]*output_count
        self.tugged = False
        self.halting = False

    def tug(self, i):
        if self.tugged:
            return False
        if self.output_queues[i]:
            return True
        self.tugged = True
        if self.compute():
            self.tugged = False
            return True
        self.tugged = False
        return False

    def compute(self):
        # child components will implement this
        return 1/0

    def pop(self, i):
        return self.output_queues[i].pop(0)

class Input(Component):
    def __init__(self):
        super().__init__([], 1)
        self.closed = False

    def compute(self):
        if self.closed:
            return False
        line = input()
        if line == "close":
            self.closed = True
            return False
        atom = Atom()
        for i in map(int,line.split()):
            atom.append(i)
        self.output_queues[0].append(atom)
        return True

class Output(Component):
    def __init__(self, i):
        super().__init__([i],1)

    def compute(self):
        (c,i) = self.inputs[0]
        if c.tug(i):
            self.output_queues[0].append(c.pop(i))
            return True
        return False

    def pop(self, i):
        print(self.output_queues[i].pop(0).items)

class Sum(Component):
    def __init__(self, i):
        super().__init__([i],1)

    def compute(self):
        (c,i) = self.inputs[0]
        if c.tug(i):
            a = c.pop(i)
            a.items = [sum(a.items)]
            self.output_queues[0].append(a)
            return True
        return False

class Enclosure(Component):
    def __init__(self, inputs, output_count, internal_inputs, internal_outputs):
        super().__init__(self, inputs, output_count)
        self.internal_inputs = internal_inputs
        self.internal_outputs = internal_outputs
        # 0 = running
        # 1 = halting event
        # 2 = halted

    def compute(self):
        pass

