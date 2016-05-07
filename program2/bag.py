from collections import defaultdict
from goody import type_as_str
import random
import re
class Bag:
    def __init__(self,iterable=[]):
        self._set = defaultdict(int)
        '''
        if (re.match(re.compile("({.}+\[\d+\])(,{.}+\[\d+\])*"),str(iterable))):
            iterable = re.findall("({.}+\[\d+\])",iterable)
        '''
        for element in iterable:
            self._set[element]+=1
    def _getlist(self,exclude=None):
        result = []
        temp = []
        for k,v in self._set.items():
            result.extend([k for j in range(v) if k != exclude])
        while len(result)>0:
            temp.append(result.pop(random.randrange(len(result))))
        return temp
    def __repr__(self):
        return "Bag({})".format(self._getlist())
    def __str__(self):
        result = "Bag("
        for k,v in self._set.items():
            result += "{}[{}],".format(k,v) 
        result =  result.rstrip(",")+")"
        return result
    
    def __len__(self):
        return len(self._getlist())
    
    def unique(self)->int:
        return len(self._set.keys())
    
    def __contains__(self,item):
        if not(item in self._set.keys()):
            return False
        return self._set[item]>0
    
    def count(self,item):
        if item in self._set.keys():
            return int(self._set[item])
        else:
            return 0
    def add(self,item):
        if item in self._set:
            self._set[item] += 1
        else:
            self._set[item] = 1
    def remove(self,item):
        if not(item in self._set.keys()):
            raise ValueError
        self._set[item] -= 1 
        if self._set[item] == 0:
            del self._set[item]
    def __eq__(self,right):
        if type(self) != type(right):
            raise TypeError
        return sorted(self._getlist()) == sorted(right._getlist())
    def __ne__(self,right):
        return not(self.__eq__(right))
    
    def __iter__(self):
        self._n = 0
        self._list = self._getlist()
        return self
    def __next__(self):
        if self._n >= len(self._list):
            raise StopIteration
        self._n +=1
        return self._list[self._n-1]
    
    def sorted(self):
        return sorted(self._getlist())
if __name__ == '__main__':
    import driver
    driver.driver()
    
