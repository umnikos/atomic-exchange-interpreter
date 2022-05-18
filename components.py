from bisect import insort
from copy import deepcopy

class Atom:
    def __init__(self):
        self.items = []

    def append(self, val):
        insort(self.items, val)

    def pop_big(self):
        return self.items.pop()

    def pop_small(self):
        return self.items.pop(0)

    def empty(self):
        return not bool(self.items)

    def weight(self):
        return sum(self.items)

class Component:
    def __init__(self, inputs, output_count):
        self.inputs = inputs
        self.output_queues = [[] for _ in range(output_count)]
        self.tugged = False
        self.halt_announcer = None

    def insert_input(self, index, input):
        if self.inputs[index] == None:
            self.inputs[index] = input
        else:
            1/0

    def tug(self, i):
        while True:
            if self.output_queues[i]:
                return True
            if self.tugged:
                return False
            self.tugged = True
            if self.compute(i):
                self.tugged = False
                if self.output_queues[i]:
                    return True
                continue
            self.tugged = False
            return False

    def on_halt_event(self):
        # intersections are the ones who care about this
        # and return if they passed anything through
        return False

    def compute(self,_):
        # child components will implement this
        return 1/0

    def pop(self, i):
        return self.output_queues[i].pop(0)

class Input(Component):
    def __init__(self):
        super().__init__([], 1)

    def compute(self,_):
        # enclosures will handle putting things inside the output queue
        return False

class Output(Component):
    def __init__(self, i):
        super().__init__([i],1)

    def compute(self,_):
        (c,i) = self.inputs[0]
        if c.tug(i):
            self.output_queues[0].append(c.pop(i))
            return True
        return False

class Sum(Component):
    def __init__(self, i):
        super().__init__([i],1)

    def compute(self,_):
        (c,i) = self.inputs[0]
        if c.tug(i):
            a = c.pop(i)
            a.items = [sum(a.items)]
            self.output_queues[0].append(a)
            return True
        return False

class Enclosure(Component):
    def update_halt_announce_list(self, o):
        self.halt_announce_list.append(o)
        for (c,i) in o.inputs:
            if c not in self.halt_announce_list:
                self.update_halt_announce_list(c)

    def announce_halt_event(self):
        r = False
        for c in self.halt_announce_list:
            r = c.on_halt_event() or r
        return r

    def __init__(self, inputs, output_count, internal_inputs, internal_outputs):
        super().__init__(inputs, output_count)
        self.internal_inputs = internal_inputs
        self.internal_outputs = internal_outputs
        self.halt_announce_list = []
        for o in self.internal_outputs:
            self.update_halt_announce_list(o)

    def compute(self,i):
        while True:
            if self.internal_outputs[i].tug(0):
                self.output_queues[i].append(self.internal_outputs[i].pop(0))
                return True
            r = self.announce_halt_event()
            if r:
                continue
            # halted, time for input
            if not self.inputs:
                return False
            will_do = True
            for (c,i) in self.inputs:
                if not c.tug(i):
                    will_do = False
                    break
            if not will_do:
                return False
            for k in range(len(self.inputs)):
                (c,i) = self.inputs[k]
                self.internal_inputs[k].output_queues[0].append(c.pop(i))

class IOEnclosure(Enclosure):
    def __init__(self, internal_input, internal_output):
        super().__init__([],1,[internal_input],[internal_output])

    def pop(self,i):
        print(super().pop(0).items)
        return None

    def run(self):
        while True:
            while self.compute(0):
                self.pop(0)
            try:
                l = input()
            except EOFError:
                l = ''
            if not l:
                # no more input and nothing to compute without the input
                return
            a = Atom()
            for n in map(int, l.split()):
                a.append(n)
            self.internal_inputs[0].output_queues[0].append(a)

class Splitter(Component):
    def __init__(self, input):
        super().__init__([input],2)

    def compute(self,_):
        (c,i) = self.inputs[0]
        if c.tug(i):
            a = c.pop(i)
            b = deepcopy(a)
            self.output_queues[0].append(a)
            self.output_queues[1].append(b)
            return True
        return False

class VoidList:
    def append(self, x):
        pass

    def pop(self, x):
        pass

    def pop(self):
        pass

class Disposal(Component):
    def __init__(self, input):
        super().__init__([input],0)
        (c,i) = input
        c.output_queues[i] = VoidList()

class Zero(Component):
    def __init__(self):
        super().__init__([], 1)
        self.output_queues[0].append(Atom())

    def compute(self,_):
        return False

class Zeros(Component):
    def __init__(self):
        super().__init__([], 1)

    def compute(self,_):
        self.output_queues[0].append(Atom())
        return True

class Intersection(Component):
    def __init__(self, primary, secondary):
        super().__init__([primary, secondary], 1)

    def compute(self,_):
        (c,i) = self.inputs[0]
        if c.tug(i):
            a = c.pop(i)
            self.output_queues[0].append(a)
            return True
        # secondary input could be tugged here or not
        # I don't think it matters either way
        return False

    def on_halt_event(self):
        (c,i) = self.inputs[1]
        if c.tug(i):
            a = c.pop(i)
            self.output_queues[0].append(a)
            return True
        return False

class BlackArrow(Component):
    def __init__(self, source, dest=None):
        if dest:
            super().__init__([source, dest], 2)
        else:
            z = Zeros()
            super().__init__([source, (z,0)], 2)
            Disposal((self,1))

    def compute(self,_):
        (c,i) = self.inputs[0]
        (d,j) = self.inputs[1]
        if c.tug(i) and d.tug(j):
            a = c.pop(i)
            b = d.pop(j)
            if not a.empty():
                b.append(a.pop_small())
            self.output_queues[0].append(a)
            self.output_queues[1].append(b)
            return True
        return False

# basically the same as BlackArrow but copy-pasting is easier
class WhiteArrow(Component):
    def __init__(self, source, dest=None):
        if dest:
            super().__init__([source, dest], 2)
        else:
            z = Zeros()
            super().__init__([source, (z,0)], 2)
            Disposal((self,1))

    def compute(self,_):
        (c,i) = self.inputs[0]
        (d,j) = self.inputs[1]
        if c.tug(i) and d.tug(j):
            a = c.pop(i)
            b = d.pop(j)
            if not a.empty():
                b.append(a.pop_big())
            self.output_queues[0].append(a)
            self.output_queues[1].append(b)
            return True
        return False

class NumberArrow(Component):
    def __init__(self, line, num):
        super().__init__([line], 1)
        self.num = num

    def compute(self,_):
        (c,i) = self.inputs[0]
        if c.tug(i):
            a = c.pop(i)
            a.append(self.num)
            self.output_queues[0].append(a)
            return True
        return False

class Diamond(Component):
    # left side is black, right side is white
    def __init__(self, left, right):
        super().__init__([left,right],4)

    def compute(self,_):
        (c,i) = self.inputs[0]
        (d,j) = self.inputs[1]
        if c.tug(i) and d.tug(j):
            a = c.pop(i)
            b = d.pop(j)
            aw = a.weight()
            bw = b.weight()
            if aw == bw:
                self.output_queues[2].append(a)
                self.output_queues[3].append(b)
            else:
                if aw < bw:
                    left = a
                    right = b
                else:
                    left = b
                    right = a
                self.output_queues[0].append(left)
                self.output_queues[1].append(right)
            return True
        return False



