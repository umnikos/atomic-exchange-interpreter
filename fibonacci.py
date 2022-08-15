from components import *

def fibonacci():
    one, = NumberArrow(*Zero(), 1)
    to_loop, = Input()
    bottom, = Intersection(to_loop,one)

    split,middle = Splitter(bottom)
    top, = Intersection(middle,*Zero())

    for_output,the_rest = Splitter(top)
    o, = Output(for_output)

    trash,arrow = WhiteArrow(split,the_rest)
    Disposal(trash)

    sum, = Sum(arrow)
    to_loop.connect_to_output(sum)

    return Enclosure([],1,[],[o])

if __name__ == "__main__":
    f, = fibonacci()
    o, = Output(f)
    IOEnclosure(o).run()

