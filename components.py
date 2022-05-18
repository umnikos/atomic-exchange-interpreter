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
        self.halt_announcer = None

    def tug(self, i):
        if self.tugged:
            return False
        if self.output_queues[i]:
            return True
        self.tugged = True
        if self.compute(i):
            self.tugged = False
            return True
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
            self.output_queues[0].append(a)
            self.output_queues[1].append(a)
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







