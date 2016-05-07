## Ho Choi, Lab1
from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK implements __check_annotation__ by checking whether all the
      annotations passed to its constructor are OK; the first one that
      fails (raises AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (raise AssertionError) this classes raises AssertionError and prints its
      failure, along with a list of all annotations tried followed by the check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation():
    # must be True for checking to occur
    checking_on  = True
  
    # self._checking_on must also be true for checking to occur
    def __init__(self,f):
        self._f = f
        self.checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        if(param == "_return"):
            if isinstance(value, tuple):                
                assert isinstance(value[0],annot),check_history+": "+str(value[0])+" should "+str(annot)
            else:        
                assert isinstance(value, annot),check_history+": "+str(value)+" should "+str(annot)
        elif annot == None:
            pass   
        elif isinstance(annot, type):
            assert isinstance(value, annot),check_history+": "+str(value)+" should "+str(annot)
        elif isinstance(annot, list) or isinstance(annot, tuple):
            assert isinstance(value, type(annot)),check_history+": "+str(value)+" should "+str(type(annot))
            assert len(value) >= len(annot),check_history+": "+str(value)+" should "+str(type(annot))
            for i in range(len(value)):
                self.check(param, annot[i%len(annot)], value[i],check_history)
        elif isinstance(annot, dict):
            assert isinstance(value, type(annot)),check_history+": "+str(value)+" should "+str(type(annot))        
            for k,v in value.items():
                for key,value in annot.items():
                    self.check(param,key,k,check_history)
                    self.check(param,value,v,check_history)
        elif isinstance(annot, set) or isinstance(annot, frozenset):
            assert isinstance(value, type(annot)),check_history+": "+str(value)+" should "+str(type(annot))
            zipped = zip(annot, value)
            for i in zipped:
                self.check(param, i[0], i[1],check_history)
        elif inspect.isfunction(annot):
            try:
                assert annot(value)
            except:
                raise AssertionError
        else:
            if isinstance(annot,str):
                try:
                    func = eval("lambda "+param + ": "+annot)
                    assert func(value),check_history
                except:
                    raise AssertionError(check_history)
            else:
                try:
                    annot.__check_annotation__(self.check,param,value,check_history)
                except:
                    raise AssertionError(check_history)
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict, in the order parameters occur in the function's header)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if param.name not in bound_f_signature.arguments:
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments
        
        if not self.checking_on:
            return self._f(args)
        
        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
                            
        try:
            # Check the annotation for every parameter (if there is one)
            ordict = param_arg_bindings()
            annotationDict = self._f.__annotations__
            
            for k,v in annotationDict.items():
                if k != "return":
                    self.check(k, v, ordict[k],str(k))
            # Compute/remember the value of the decorated function

            # If 'return' is in the annotation, check it
            if "return" in annotationDict.keys():
                self.check("_return",annotationDict["return"],self._f(args))
            # Return the decorated answer
            
            

        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
#           print(80*'-')
#           for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
#           print(l.rstrip())
#           print(80*'-')
            raise
            



  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    def f(x:int):pass
    try:
        f = Check_Annotation(f)
        f(3)
        f('a')
    except:
        pass   
    import driver
    driver.driver()
