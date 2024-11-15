from components import *
from sync import sync
from demux import demux
from split import split

def mul(ii):
    i, = Input()

    z, = Zeros()

    count,inc = WhiteArrow(i,z)
    count, = split(count)
    acc, = Zeros()
    acc,inc = sync(acc,inc)
    acc,count = sync(acc,count) # not needed?

    acc_i, = Input()
    acc, = Intersection(acc_i, acc)

    inc_i, = Input()
    inc, = Intersection(inc_i, inc)

    count_i, = Input()
    count, = Intersection(count_i, count)

    # not needed?
    acc,inc = sync(acc,inc)
    acc,count = sync(acc,count)
    acc,inc = sync(acc,inc)

    count, count1 = Splitter(count)
    count, count2 = Splitter(count)
    count, count3 = Splitter(count)

    acc, out = demux(acc, count2)
    inc, trash = demux(inc, count3)
    Disposal(trash)
    count, trash = demux(count, count1)
    Disposal(trash)

    count, = BlackArrow(count)
    count_i.connect_to_output(count)

    inc, inc2 = Splitter(inc)
    inc2, acc = WhiteArrow(inc2, acc)
    Disposal(inc2)
    acc, = Sum(acc)

    acc_i.connect_to_output(acc)
    inc_i.connect_to_output(inc)

    o, = Output(out)

    return Enclosure([ii],1,[i],[o])

if __name__ == "__main__":
    ii, = Input()
    m, = mul(ii)
    oo, = Output(m)
    IOEnclosure(ii,oo).run()

