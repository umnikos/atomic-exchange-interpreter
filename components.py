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

class OutputQueue:
    def __init__(self, parent, i):
        self.parent = parent
        self.i = i
        self.queue = []

    def component(self):
        return self.parent

    def tug(self):
        return self.parent.tug(self.i)

    def __bool__(self):
        return bool(self.queue)

    def pop(self):
        return self.queue.pop(0)

    def append(self, a):
        return self.queue.append(a)

    def push(self, a):
        return self.append(a)

    # this is used for making loops
    def connect_to_output(self, out):
        if self.parent == None:
            self.queue = out.queue
            self.parent = out.parent


class Component:
    def __init__(self, inputs: list[OutputQueue], output_count: int):
        self.inputs = inputs
        self.output_queues = [OutputQueue(self, i) for i in range(output_count)]
        self.tugged = False
        self.halt_announcer = None

    def __iter__(self):
        return iter(self.output_queues)

    # if this is baffling look at the same method for OutputQueue
    def component(self):
        return self

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
        assert False, "Unimplemented compute() method of Component"

    def pop(self, i):
        return self.output_queues[i].pop()

class Input(Component):
    def __init__(self):
        super().__init__([], 1)
        self.output_queues[0].parent = None # allows to be connected to something else

    def compute(self,_):
        # enclosures will handle putting things inside the output queue
        return False

class Output(Component):
    def __init__(self, i: OutputQueue):
        super().__init__([i],1)

    def compute(self,_):
        c = self.inputs[0]
        if c.tug():
            self.output_queues[0].append(c.pop())
            return True
        return False

class Sum(Component):
    def __init__(self, i: OutputQueue):
        super().__init__([i],1)

    def compute(self,_):
        c = self.inputs[0]
        if c.tug():
            a = c.pop()
            a.items = [sum(a.items)]
            self.output_queues[0].append(a)
            return True
        return False

class Enclosure(Component):
    def update_halt_announce_list(self, o):
        self.halt_announce_list.append(o)
        for q in o.inputs:
            if q.component() not in self.halt_announce_list:
                self.update_halt_announce_list(q.component())

    def announce_halt_event(self):
        r = False
        for c in self.halt_announce_list:
            r = c.on_halt_event() or r
        return r

    def __init__(self, inputs: list[OutputQueue], output_count: int, internal_inputs: list[Component], internal_outputs: list[Component]):
        super().__init__(inputs, output_count)
        self.internal_inputs = [x.component() for x in internal_inputs]
        self.internal_outputs = [x.component() for x in internal_outputs]
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
            will_do = False
            for k in range(len(self.inputs)):
                if self.internal_inputs[k].output_queues[0]:
                    continue
                if self.inputs[k].tug():
                    will_do = True
            if not will_do:
                return False
            for k in range(len(self.inputs)):
                q = self.inputs[k]
                if q.tug():
                    self.internal_inputs[k].output_queues[0].append(q.pop())

class IOEnclosure(Enclosure):
    def __init__(self, first, second=None):
        if second != None:
            super().__init__([],1,[first],[second])
            self.skip_input = False
        else:
            super().__init__([],1,[],[first])
            self.skip_input = True

    def pop(self,i):
        print(super().pop(0).items)

    def run(self):
        while True:
            while self.compute(0):
                self.pop(0)
            if self.skip_input:
                return
            try:
                l = input()
            except EOFError:
                l = ''
            if not l:
                # no more input and nothing to compute without the input
                return
            a = Atom()
            for n in map(int, l.split()):
                if n > 0:
                    a.append(n)
            self.internal_inputs[0].output_queues[0].append(a)

class Splitter(Component):
    def __init__(self, input):
        super().__init__([input],2)

    def compute(self,_):
        q = self.inputs[0]
        if q.tug():
            a = q.pop()
            b = deepcopy(a)
            self.output_queues[0].append(a)
            self.output_queues[1].append(b)
            return True
        return False

class VoidList:
    def append(self, x=None):
        pass

    def pop(self, x=None):
        pass

    def pop(self, x=None):
        pass

class Disposal(Component):
    def __init__(self, input):
        super().__init__([input],0)
        input.queue = VoidList()

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
    def __init__(self, primary: OutputQueue, secondary: OutputQueue):
        super().__init__([primary, secondary], 1)

    def compute(self,_):
        c = self.inputs[0]
        if c.tug():
            a = c.pop()
            self.output_queues[0].append(a)
            return True
        # secondary input could be tugged here or not
        # I don't think it matters either way
        return False

    def on_halt_event(self):
        c = self.inputs[1]
        if c.tug():
            a = c.pop()
            self.output_queues[0].append(a)
            return True
        return False

class BlackArrow(Component):
    def __init__(self, source: OutputQueue, dest=None):
        if dest != None:
            super().__init__([source, dest], 2)
        else:
            z, = Zeros()
            super().__init__([source, z], 2)
            Disposal(self.output_queues[1])

    def handle_atoms(self, a, b):
        if not a.empty():
            b.append(a.pop_small())

    def compute(self,_):
        c = self.inputs[0]
        d = self.inputs[1]
        if c.tug() and d.tug():
            a = c.pop()
            b = d.pop()
            self.handle_atoms(a,b)
            self.output_queues[0].append(a)
            self.output_queues[1].append(b)
            return True
        return False

class WhiteArrow(BlackArrow):
    def handle_atoms(self, a, b):
        if not a.empty():
            b.append(a.pop_big())

class NumberArrow(Component):
    def __init__(self, line: OutputQueue, num):
        super().__init__([line], 1)
        self.num = num

    def compute(self,_):
        c = self.inputs[0]
        if c.tug():
            a = c.pop()
            a.append(self.num)
            self.output_queues[0].append(a)
            return True
        return False

class Diamond(Component):
    # left side is black, right side is white
    def __init__(self, left: OutputQueue, right: OutputQueue):
        super().__init__([left,right],4)

    def compute(self,_):
        c = self.inputs[0]
        d = self.inputs[1]
        if c.tug() and d.tug():
            a = c.pop()
            b = d.pop()
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



