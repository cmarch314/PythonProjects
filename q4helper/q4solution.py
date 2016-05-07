#Helper functions for testing (both in this module and in bsc)
from predicate import is_prime

def primes(max=None):
    p = 2
    while max == None or p <= max:
        if is_prime(p):
            yield p
        p += 1
         
def lets(string):
    for let in string:
        yield let
        




def in_a_row(n,iterable):
    assert n>1,"n:{} (n should be greater then 2)".format(n)
    result = set()
    container = []
    iterable = iter(iterable)
    while True:
        try:
            container.append(next(iterable))
            if len(container) == n:
                if (container.count(container[0])==n):
                    result.add(container[0])
                container.pop(0)
        except:
            break
    return result
 
class Permutation:
    def __init__(self,p,start):
        self.p     = p
        self.start = start
        
    def __iter__(self):

        return iter(self.P_iter(self.p,self.start))
    
    class P_iter:
        def __init__(self,p,start):
            self.initial = False
            self.p = p
            self.start = start
        def __iter__(self):
            self.current  = self.start
            return self
        def __next__(self):
            temp = self.current
            self.current = self.p[self.current]
            if self.initial == True and temp == self.start:
                raise StopIteration
            self.initial = True
            return temp
            pass
class Permutation2:
    def __init__(self,p,start):
        self.p     = p
        self.start = start
        
    def __iter__(self):
        self.current = self.start
        while True:
            yield self.current
            self.current = self.p[self.current]
            if self.current == self.start:
                raise StopIteration
        
def differences(it1,it2):
    it1,it2 = iter(it1),iter(it2)
    result = []
    index = 0
    while True:
        try:
            x,y = next(it1), next(it2)
            if not(x == y):
                result.append((index,x,y))
            index+=1
        except:
            return iter(result)
        
def skipper(iterable,n=0):
        result = []
        index = 0
        iterable  = iter(iterable)
        while True:
            try:
                next_element = next(iterable)
                if index%(n+1) == 0:
                    result.append(next_element)
                index+=1
            except:
                return iter(result)

if __name__ == '__main__':
    import driver
    
    driver.driver() # type quit in driver to return and execute code below
    
    # Test in_a_row; add your own test cases
    print('Testing in_a_row')
    print(in_a_row(2,[4,4,2,6,6,9,6,7,7,3,2,2]))
    print(in_a_row(3,[5,3,7,7,7,2,3,8,5,4,4,4,6]))
    print(in_a_row(4,[5,5,5]))
    for i in range(5,1,-1):
        print('for',i,'=',in_a_row(i,map(lambda x : x.rstrip(),open('in_a_row.txt'))))
    
    
    # Test Permutation/Permuation2; add your own test cases
    print('\nTesting Permutation')
    for i in Permutation([4,0,3,1,2],0):
        print(i,end='')
    print()
    
    for i in Permutation([4,0,3,1,2],3):
        print(i,end='')
    print()
    
    for i in Permutation([0],0):
        print(i,end='')
    print()
    

    print('\nTesting Permutation2')
    for i in Permutation2([4,0,3,1,2],0):
        print(i,end='')
    print()
    
    for i in Permutation2([4,0,3,1,2],3):
        print(i,end='')
    print()
    
    for i in Permutation2([0],0):
        print(i,end='')
    print()
    

        
    # Test differences; add your own test cases
    print('\nTesting differences')
    for i in differences('abcdefghijklmnopqrstuvwxyz',
                         'abc#efghij;lmnopq;stuvwxyz/'):
        print(i,end='')
    print()
    
    for i in differences(lets('abcdefghijklmnopqrstuvwxyz///'),
                         lets('abc1ef2hijk3mnopqr4tuvwxyz')):
        print(i,end='')
    print()
    
    
    # Test skipper; add your own test cases
    print('\nTesting skipper')
    for i in skipper('abcdefghijklmnopqrstuvwxyz'):
        print(i,end='')
    print()

    for i in skipper('abcdefghijklmnopqrstuvwxyz',1):
        print(i,end='')
    print()

    for i in skipper('abcdefghijklmnopqrstuvwxyz',2):
        print(i,end='')
    print()

    # Primes 1-50: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
    # Skipping 2 : 2 7 17 29 41 
    for i in skipper(primes(50),2):
        print(i,end=' ')
    print()

