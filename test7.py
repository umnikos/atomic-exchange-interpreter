from components import *

z = Zero()
i = Input()
m = Intersection((z,0),(i,0))
o = Output((m,0))

e = IOEnclosure(i,o)
e.run()

