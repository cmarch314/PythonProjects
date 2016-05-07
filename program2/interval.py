# I used the following imports; feel free to add others
from goody import type_as_str
from math import sqrt
import re

class Interval:
    def __init__(self,mn,mx=None):
        mx = mn if (mx == None) else mx
        if (mx<mn):
            raise AssertionError
        self.min = mn
        self.max = mx
    @staticmethod
    def min_max(mn,mx=None):
        mx = mn if (mx == None) else mx
        try:
            return Interval(float(mn),float(mx))
        except:
            raise AssertionError
    @staticmethod
    def mid_err(mid,error = 0):
        try:
            return Interval(mid-error,mid+error)
        except:
            raise AssertionError
        
    def best(self):
        return (self.max+self.min)/2
    def error(self):
        return (self.max-self.min)/2
    def relative_error(self):
        return (self.error()/self.best())*100
    
    def __repr__(self):
        return "Interval({},{})".format(float(self.min),float(self.max))
    def __str__(self):
        return "{}(+/-{})".format(self.best(),self.error())
    def __bool__(self):
        return self.min != self.max
    
    ## Unary prefix(+/-)
    def __pos__(self):
        return self
    def __neg__(self):
        return Interval((-1)*self.max,(-1)*self.min)
    ## Arithmetic operands
    def _comb(self,op:str,other):
        '''
        this method would take two Intervals and operator between them
        and return min and max of combinations of all min and max after execute operator with them
        '''
        result = sorted([eval("self.min"+op+"other.min"), eval("self.min"+op+"other.max"),eval("self.max"+op+"other.min"),eval("self.max"+op+"other.max")])
        return Interval(result[0],result[-1])
    def _contains_zero(self):
        '''
        this will return true
        if Interval contains Zero
        '''
        if self.min * self.max <= 0:
            return True
        return False
    def __add__(self,other):
        if type(other) == type(self):
            return Interval._comb(other,"+",self)
        return self+Interval(other,other)
    def __radd__(self,other):
        if type(other) == type(self):
            return Interval._comb(other,"+",self)
        return Interval(other,other)+self
    def __sub__(self,right):
        if type(right) == type(self):
            return Interval._comb(self,"-",right)
        return self-Interval(right,right)
    def __rsub__(self,left):
        if type(left) == type(self):
            return Interval._comb(left,"-",self)
        return Interval(left,left)-self
    def __mul__(self,right):
        right = right+Interval(0,0)
        return Interval._comb(self,"*",right)
    def __rmul__(self,left):
        left = left+Interval(0,0)
        return Interval._comb(left,"*",self)
    def __truediv__(self,right):
        right = right+Interval(0)
        if right._contains_zero():
            raise ZeroDivisionError
        return Interval._comb(self,"/",right)
    def __rtruediv__(self,left):
        left = left+Interval(0)
        if self._contains_zero():
            raise ZeroDivisionError
        return Interval._comb(left,"/",self)
    def __pow__(self,n):
        if(re.match("^[+-]?\d+$",str(n))):
            n = n+Interval(0)
            return Interval._comb(self, "**", n)
        raise TypeError
    def __rpow__(self,x):
        raise TypeError
    
    ##rational operator
    compare_mode = ""
    mode_list = ["liberal","conservative"]
    @staticmethod
    def c_mode_test():
        return Interval.compare_mode in Interval.mode_list
    def __eq__(self,right):
        if type(right)!=type(self):
            raise TypeError
        return (self.min == right.min and self.max == right.max)
    def comp(self,other):
        other = other + Interval(0)
        if Interval.compare_mode == "liberal":
            pass
        elif Interval.compare_mode == "conservative":
            pass
        else:
            raise AssertionError("compare_mode:{} not in list ['liberal','conservative']".format(Interval.compare_mode))
        
    def __gt__(self,right): ## self > right
        assert Interval.c_mode_test(),"compare_mode:{} not in list ['liberal','conservative']".format(Interval.compare_mode)
        right = right + Interval(0)
        return (self.best() if Interval.compare_mode == "liberal" else self.min) > (right.best() if Interval.compare_mode == "liberal" else right.max)
    def __ge__(self,right): ## self >= right
        assert Interval.c_mode_test(),"compare_mode:{} not in list ['liberal','conservative']".format(Interval.compare_mode)
        right = right + Interval(0)
        return (self.best() if Interval.compare_mode == "liberal" else self.min) >= (right.best() if Interval.compare_mode == "liberal" else right.max)
    def __lt__(self,right): ## self < right
        assert Interval.c_mode_test(),"compare_mode:{} not in list ['liberal','conservative']".format(Interval.compare_mode)
        right = right + Interval(0)
        return (self.best() if Interval.compare_mode == "liberal" else self.max) < (right.best() if Interval.compare_mode == "liberal" else right.min)
    def __le__(self,right): ## self <= right
        assert Interval.c_mode_test(),"compare_mode:{} not in list ['liberal','conservative']".format(Interval.compare_mode)
        right = right + Interval(0)
        return (self.best() if Interval.compare_mode == "liberal" else self.max) <= (right.best() if Interval.compare_mode == "liberal" else right.min)
    def __ne__(self,right): ## self != right
        return not(self.__eq__(right))   
    
    ##abs,sqrt
    def __abs__(self):
        return Interval(0.0 if self._contains_zero() else sqrt((self*self).min),sqrt((self*self).max))
    
    def sqrt(self):
        return Interval(sqrt(self.min),sqrt(self.max))
    def __setattr__(self,name,value):
        assert not(name in self.__dict__),"min,max are immutable"
        assert (name == "min" or name=="max"), "Class is immutable"
        self.__dict__[name] = value
        
    
if __name__ == '__main__':
     
    #put code here to test Interval directly
        
    import driver
    driver.driver()
