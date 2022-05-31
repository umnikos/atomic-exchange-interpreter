from components import *
i, = Input()
s, = Sum(i)
o, = Output(s)

e = IOEnclosure(i,o)
e.run()
