from components import *

def if(line, cond):
    a, = Input()
    b, = Input()
    s,ss = Split(a)
    c,cc = BlackArrow(b,ss)
    Disposal(c)
    d,dd,ddd,dddd = Diamond(s,cc)
    Disposal(dd)
    Disposal(dddd)
    t, = Output(d)
    f, = Output(ddd)

    return Enclosure([line, cond], 2, [a, b], [t, f])


