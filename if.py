from components import *

def if(line, cond):
    a = Input()
    b = Input()
    s = Split((a,0))
    c = BlackArrow((b,0),(s,1))
    Disposal((c,0))
    d = Diamond((s,0),(c,1))
    Disposal((d,1))
    Disposal((d,3))
    t = Output((d,0))
    f = Output((d,2))

    return Enclosure([line, cond], 2, [a, b], [t, f])


