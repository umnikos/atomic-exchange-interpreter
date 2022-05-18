from components import *

i = Input()
z = Input()

left_i = Intersection(None, (z,0))
right_i = Intersection(None, (i,0))
diamond = Diamond((left_i,0), (right_i,0))
increment = NumberArrow((diamond,0),1)
left_i.insert_input(0,(increment,0))
right_i.insert_input(0,(diamond,1))
o = Output((diamond,2))

ii = Input()
zz = Zeros()
ee = Enclosure([(ii,0),(zz,0)],1,[i,z],[o])
oo = Output((ee,0))

e = IOEnclosure(ii,oo)
e.run()
