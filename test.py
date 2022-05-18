from components import *

i = Input()
s = Sum((i,0))
o = Output((s,0))
ii = Input()
e = Enclosure([(ii,0)],1,[i],[o])
oo = Output((e,0))

a = Atom()
a.append(1)
a.append(2)
ii.output_queues[0].append(a)

print(oo.tug(0))
print(oo.pop(0).items)
