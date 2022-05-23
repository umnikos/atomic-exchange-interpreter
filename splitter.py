from components import *
from sync import sync

i = Input()
z = Zeros()
s = sync((z,0),(i,0))

left_i = Intersection(None, (s,0))
right_i = Intersection(None, (s,1))
diamond = Diamond((left_i,0), (right_i,0))
increment = NumberArrow((diamond,0),1)
left_i.insert_input(0,(increment,0))
right_i.insert_input(0,(diamond,1))
o = Output((diamond,2))

e = IOEnclosure(i,o)
e.run()
