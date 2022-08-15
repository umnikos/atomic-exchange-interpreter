from components import *
from sync import sync

def split(ii):
    i, = Input()
    l = [i]
    z, = Zeros()
    z,i = sync(z,i) #s

    left_i, = Input()
    right_i, = Input()
    left, = Intersection(left_i, z)
    right, = Intersection(right_i, i)

    d,dd,ddd,dddd = Diamond(left, right)
    Disposal(dddd)

    increment, = NumberArrow(d,1)

    left_i.connect_to_output(increment)
    right_i.connect_to_output(dd)

    o, = Output(ddd)
    return Enclosure([ii],1,l,[o])

if __name__ == "__main__":
    i, = Input()
    s, = split(i)
    o, = Output(s)
    IOEnclosure(i,o).run()

