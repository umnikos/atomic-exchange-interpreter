from components import *

i = Input()
s = Sum((i,0))
c = Splitter((s,0))
o = Output((c,0))
d = Disposal((c,1))

e = IOEnclosure(i,o)
e.run()

print(c.output_queues)


