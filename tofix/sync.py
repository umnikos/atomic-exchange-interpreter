from components import *

def sync(i, ii):
    a = Input()
    b = Input()

    x = NumberArrow((a,0),1)
    y = BlackArrow((x,0),(b,0))
    z = BlackArrow((y,1))

    o = Output((y,0))
    oo = Output((z,0))

    return Enclosure([i,ii],2,[a,b],[o,oo])

