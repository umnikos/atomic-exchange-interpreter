from components import *

z = Zero()
o = Output((z,0))

e = IOEnclosure(Input(),o)
e.run()

