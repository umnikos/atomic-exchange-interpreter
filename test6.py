from components import *

z = Zeros()
o = Output((z,0))

e = IOEnclosure(Input(),o)
e.run()

