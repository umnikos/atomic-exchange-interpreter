from components import *

def fibonacci():
    one = NumberArrow((Zero(),0), 1)
    bottom = Intersection(None,(one,0))
    split = Splitter((bottom,0))
    zero = Zero()
    top = Intersection((split,0),(zero,0))
    for_output = Splitter((top,0))
    o = Output((for_output,1))
    arrow = WhiteArrow((split,1),(for_output,0))
    Disposal((arrow,0))
    sum = Sum((arrow,1))
    bottom.insert_input(0,(sum,0))

    return Enclosure([],1,[],[o])

if __name__ == "__main__":
    f = fibonacci()
    o = Output((f,0))
    e = IOEnclosure(o)
    e.run()

