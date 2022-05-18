from components import *

i = Input()
s = Sum((i,0))
o = Output((s,0))

e = IOEnclosure(i,o)
e.run()
