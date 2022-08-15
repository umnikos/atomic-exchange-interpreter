from components import *


def sync(i, ii):
    a, = Input()
    b, = Input()
    l = [a,b]

    a, = NumberArrow(a,1)
    a,b = BlackArrow(a,b)
    b, = BlackArrow(b)

    o, = Output(a)
    oo, = Output(b)
    return Enclosure([i,ii],2,l,[o,oo])

if __name__ == "__main__":
    i, = Input()
    numbers, = NumberArrow(*Zeros(), 123)
    x,y = sync(i,numbers)
    Disposal(x)
    o, = Output(y)
    IOEnclosure(i,o).run()

