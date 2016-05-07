import inspect
import predicate
from goody import irange
from random import shuffle


# Tree Node class and helper functions (to set up problem)

class TN:
    def __init__(self,value,left=None,right=None):
        self.value = value
        self.left  = left
        self.right = right

def add(atree,value):
    if atree == None:
        return TN(value)
    if value < atree.value:
        atree.left = add(atree.left,value)
        return atree
    elif value > atree.value:
        atree.right = add(atree.right,value)
        return atree
    else:
        return atree  # already in tree

def add_all(atree,values):
    for v in values:
        atree = add(atree,v)
    return atree



# List Node class and helper functions (to set up problem)

class LN:
    def __init__(self,value,next=None):
        self.value = value
        self.next  = next

def list_to_ll(l):
    if l == []:
        return None
    front = rear = LN(l[0])
    for v in l[1:]:
        rear.next = LN(v)
        rear = rear.next
    return front


# Tree/List functions you must write RECURSIVELY
def count(t,p):
    result = (count(t.left,p) if t.left != None else 0) + (count(t.right,p) if t.right != None else 0)
    if p(t.value):
        result +=1
    return result 

def equal(ll1,ll2):
    if ll1.value != ll2.value:
        return False
    if ll1.next!= None and ll2.next!=None:
        return equal(ll1.next, ll2.next)
    if type(ll1.next)!= type(ll2.next):
        return False
    return True
    
    return equal(ll1.next, ll2.next)
def min_max(ll):
    if ll == None:
        return None
    if ll.next!= None:
        MM = min_max(ll.next)
    else:
        MM = tuple([ll.value, ll.value])
    return tuple([ll.value if ll.value < MM[0] else MM[0],ll.value if ll.value > MM[0] else MM[0]])

# Define Dumpable here
# It must appear before Counter (so can be used as a base class)
class Dumpable:
    def get_state(self):
        d = {(k,v) for k,v in self.__dict__.items() if not inspect.isfunction(v)}
        return d
class Counter(Dumpable):
    def __init__(self,init_value=0):
        self._value = init_value

    def __str__(self):
        return str(self._value)
        
    def reset(self):
        self._value = 0
        
    def inc(self):
        self._value += 1
        
    def value_of(self):
        return self._value

 
class Modular_Counter(Counter):
    def __init__(self,value,modulus):
        Counter.__init__(self,value)
        self._modulus = modulus
    
    def __str__(self):
        return Counter.__str__(self)+' mod '+str(self._modulus)
        
    def inc(self):
        if self.value_of() == self._modulus - 1:
            Counter.reset(self)
        else:
            Counter.inc(self)
        
    def modulus_of(self):
        return self._modulus



# Testing Script

if __name__ == '__main__':
    
    print('Testing count')
    values = [i for i in irange(1,100)] 
    print('Count of primes in list =', sum(1 for i in values if predicate.is_prime(i)))
    for i in range(5):
        shuffle(values)
        t = add_all(None,values)
        print('Count of primes in randomly built tree =',count(t,predicate.is_prime))
              
    print('\nTesting equal')           
    a = list_to_ll(['one','two','three','four'])
    b = list_to_ll(['one','two','three','four'])
    c = list_to_ll(['one','two','three'])
    d = list_to_ll(['one','two','three','four','five'])
    e = list_to_ll(['one','two','four','four'])
    
    print('These are equal:', equal(a,b))
    print('These are unequal:',equal(a,c), equal(a,d), equal(a,e))
    
    print('\nTesting min_max')   
    print(min_max(None))
    print(min_max(list_to_ll([0])))
    print(min_max(list_to_ll([7, 3, 5, 2, 0])))
    print(min_max(list_to_ll([1, 3, 5, 2, 7])))
    values = [i for i in irange(1,100)] 
    for i in range(5):
        shuffle(values)
        print(min_max(list_to_ll(values)))

    print('\nTesting Dumpable vis Modular_Counter')
    c = Counter(5)           
    c.afunc = lambda x : x + 1
    mc = Modular_Counter(0,3)
    mc.afunc = lambda x : x + 1
    print(c.get_state())
    print(mc.get_state())
 
    

