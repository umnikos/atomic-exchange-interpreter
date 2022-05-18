from components import *

i = Input()

z = Zero()
a = Zero()
b = NumberArrow((a,0),1)
c = NumberArrow((b,0),2)
d = NumberArrow((c,0),3)
e = NumberArrow((d,0),3)
black = BlackArrow((e,0),(z,0))
white = WhiteArrow((black,0),(black,1))
Disposal((white,1))

o = Output((white,0))

e = IOEnclosure(i,o)
e.run()

