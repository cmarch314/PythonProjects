import random
from goody         import irange
from priorityqueue import PriorityQueue
from performance   import Performance

if __name__ == '__main__':
    
    def setup(size):
        global ec
        
        ec = PriorityQueue([random.randint(0,size-1) for i in range(size)])
        
    def code(merges,size):
        global ec
        for i in range(merges):
            ec.remove()

    for i in irange(0,8):
        size = 10000 * 2**i
        p = Performance(lambda : code(10000,size), lambda:setup(size),5,'\n\nPriorityQueue of size ' + str(size))
        p.evaluate()
        p.analyze()