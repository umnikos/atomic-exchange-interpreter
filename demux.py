from components import *

# cond controls where atoms from line go
# they go to the first output if cond>0
# they go to the second line if cond==0
def demux(line, cond):
    a, = Input()
    b, = Input()
    l = [a,b]
    a,s = Splitter(a)
    b,s = BlackArrow(b,s)
    Disposal(b)
    d,dd,ddd,dddd = Diamond(a,s)
    Disposal(dd)
    Disposal(dddd)
    t, = Output(d)
    f, = Output(ddd)

    return Enclosure([line, cond], 2, l, [t, f])

if __name__ == "__main__":
    i, = Input()
    x, y = Splitter(i)
    t,f = demux(x,y)
    Disposal(f)
    o, = Output(t)
    IOEnclosure(i,o).run()

