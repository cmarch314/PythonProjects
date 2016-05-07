import re, traceback
import keyword

def pnamedtuple(type_name, field_names, mutable=False):
    def show_listing(s):
        for i,l in enumerate(s.split('\n'),1):
            print('{num: >3} {text}'.format(num=i, text = l.rstrip()))


    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    
    
    if type(field_names) == type(str()):
        field_names = field_names.split(" ")
        
    if type(field_names) == type(list()):
        field_list = [i.rstrip(",") for i in field_names if i != ""]
    else:
        raise SyntaxError
    type_name = str(type_name).rstrip("")
    type_pattern = re.compile("^[a-zA-Z]+\w*$")
    
    if not(re.match(type_pattern, str(type_name))):
        raise SyntaxError
    
    for j in field_list:
        if j in keyword.kwlist:
            raise SyntaxError
        if not(re.match(type_pattern,str(j))):
            raise SyntaxError
    class_template = '''\
class {name}():
    def __init__(self, {field_dots}, mutable = {mutable}):
        {parameter}
        self._fields = [{field_string_list}]
        self._mutable = mutable
    
    def __repr__(self):
        return '{name}({repr_parameter})'.format({repr_para2})
    
    {get_function}
    {get_function_by_num}
    
    def __getitem__ (self, num):
        try:
            result = eval("self.get_"+str(num)+"()")
        except:
            raise IndexError
        return result
        
    def __eq__(self,right):
        if(type(self) != type(right)):
            return False
        {equality}
        return self._mutable == right._mutable
        
    def _replace(self, **kargs):
        if(self._mutable):
            for k,v in kargs.items():
                self.__dict__[k] = v
        else:
            duplicated_class = eval(str(self))
            for i in kargs.keys():
                if not i in duplicated_class.__dict__.keys():
                    raise TypeError
            duplicated_class.__dict__.update(kargs)
            return duplicated_class
    
    def __setattr__(self,name,value):
        if(not("_mutable" in self.__dict__)):
            self.__dict__[name] = value
        elif (self._mutable):
            self.__dict__[name] = value
        else:
            raise AttributeError
        
        '''
       
    class_definition = \
        class_template.format(name = type_name,parameter = "\n        ".join(["self."+i+" = "+i for i in field_list]),\
                               field_dots = ",".join([i for i in field_list]),\
                               field_string_list = ",".join(["'"+i+"'" for i in field_list]),\
                               repr_parameter = ",".join([i+"={"+i+"}" for i in field_list]),\
                               repr_para2 = ",".join([i+"=self."+i for i in field_list]),\
                               mutable = mutable,\
                               get_function = "\n\n    ".join(["def get_"+i+"(self):\n        return self."+i for i in field_list]),\
                               get_function_by_num = "\n\n    ".join(["def get_"+str(i)+"(self):\n        return self."+field_list[i] for i in range(len(field_list))])\
                               ,equality = "\n        ".join(["if self."+i+" != right."+i+":\n            return False" for i in field_list]))
    ''' 
     def __setattr__(self,name,value):
        assert not(name in self.__dict__),"min,max are immutable"
        assert (name == "min" or name=="max"), "Class is immutable"
        self.__dict__[name] = value
    '''
    
    
    # For initial debugging, always show the source code of the class
    #show_listing(class_definition)
    
    # Execute the class_definition string in a local name_space and bind the
    #   name source_code in its dictionary to the class_defintion; return the
    #   class object created; if there is a syntax error, list the class and
    #   show the error
    name_space = dict(__name__='pnamedtuple_{type_name}'.format(type_name=type_name))
    try:
        exec(class_definition, name_space)
        name_space[type_name].source_code = class_definition
    except SyntaxError:
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    import driver
    driver.driver()
