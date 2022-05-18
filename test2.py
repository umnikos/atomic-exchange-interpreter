from components import *

i = Input()
a = Atom()
a.append(1)
a.append(2)
i.output_queues[0].append(a)

s = Sum((i,0))
o = Output((s,0))

e = IOEnclosure(i,o)
e.run()
