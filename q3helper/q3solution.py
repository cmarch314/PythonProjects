import prompt,re
import math
from goody import type_as_str

def expand_re(pat_dict:{str:str}):
    for subj in pat_dict.keys():
        for key in pat_dict.keys():
            pattern = re.compile("#{}#".format(subj))
            pat_dict.update({key:re.sub(pattern, "({})".format(pat_dict[subj]), pat_dict[key])})
                
class Point:
    def __init__(self,x,y):
        if re.match("^[+-]?\d+$", str(x)) and re.match("^[+-]?\d+$", str(y)):
            self.x = int(x)
            self.y = int(y)
        else:
            raise AssertionError(type_as_str(self),"__init__")

    def __repr__(self):
        return "Point({},{})".format(self.x,self.y)

    def __str__(self):
        return "(x={},y={})".format(self.x,self.y)
    

    def __bool__(self):
        return (self.x,self.y) != (0,0)
        

    def __add__(self,right):
        if type(right) != type(Point(0,0)):
            raise TypeError
        return Point(self.x+right.x,self.y+right.y)
        

    def __mul__(self,left):
        if(re.match(re.compile("^[+-]?\d+$"), str(left)) != None):
            return Point(self.x*left,self.y*left)
        else:
            raise TypeError

    def __rmul__(self,left):
        if(re.match(re.compile("^[+-]?\d+$"), str(left)) != None):
            return Point(self.x*left,self.y*left)
        else:
            raise TypeError
        

    def __getitem__(self,index):
        if str(index) == "x" or str(index) == "0":
            return self.x
        elif str(index) == "y" or str(index) == "1":
            return self.y
        else:
            raise IndexError
        
    def __call__(self,x,y):
        self.__init__(x,y)

    def __lt__(self,P):
        if type(P) == type(Point(0,0)):
            return self.x*self.x + self.y*self.y < P.x * P.x + P.y*P.y
        else:
            try:
                return math.sqrt(self.x*self.x + self.y*self.y) < float(P)
            except:
                raise TypeError


from collections import defaultdict
class History:
    def __init__(self):
        self = defaultdict(list)
    def __setattr__(self,name,value):
        if(str(name).find("_prev")==-1):##disallow having "_prev" in name by searching result be nothing
            if(name in self.__dict__.keys()):
                self.__dict__[name].append(value)
            else:
                self.__dict__[name] = [value]
        else:## else raise Name Error
            raise NameError()

    def __getitem__(self,name):
        if (name>0):
            raise IndexError
        return dict((k,v[(int(name))-1]) if -1*int(name)+1 <= len(v) else (k,None) for (k,v) in self.__dict__.items() )

    def __getattr__(self,name):
        core_name = name.rstrip("_prev")
        _index = 0
        if re.match("\w(_prev)+",name):
            _index = (-1*len(re.findall("_prev",name))-1)
        if not(str(core_name) in self.__dict__.keys()):
            raise NameError
        if (len(self.__dict__[core_name])<int(math.fabs(_index))):
            return None      
        return self.__dict__[core_name][_index]
            


if __name__ == '__main__':
    
    if prompt.for_bool('Test expand?',True):
        pd = dict(digit=r'\d', integer=r'[=-]?#digit##digit#*')
        expand_re(pd)
        print('result =',pd)
        # produces/prints the dictionary {'digit': '\\d', 'integer': '[=-]?(\\d)(\\d)*'}
        
        pd = dict(integer       =r'[+-]?\d+',
                  integer_range =r'#integer#(..#integer#)?',
                  integer_list  =r'#integer_range#(?,#integer_range#)*',
                  integer_set   =r'{#integer_list#?}')
        expand_re(pd)
        print('result =',pd)
        # produces/prints the dictionary 
        # {'integer'      : '[+-]?\\d+',
        #  'integer_range': '([+-]?\\d+)(..([+-]?\\d+))?',
        #  'integer_list' : '(([+-]?\\d+)(..([+-]?\\d+))?)(?,(([+-]?\\d+)(..([+-]?\\d+))?))*',   
        #  'integer_set'  : '{((([+-]?\\d+)(..([+-]?\\d+))?)(?,(([+-]?\\d+)(..([+-]?\\d+))?))*)?}'
        # }
        
        pd = dict(a='correct',b='#a#',c='#b#',d='#c#',e='#d#',f='#e#',g='#f#')
        expand_re(pd)
        print('result =',pd)
        # produces/prints the dictionary 
        # {'d': '(((correct)))',
        #  'c': '((correct))',
        #  'b': '(correct)',
        #  'a': 'correct',
        #  'g': '((((((correct))))))',
        #  'f': '(((((correct)))))',
        #  'e': '((((correct))))'
        # }
    
    import driver
    driver.driver()
