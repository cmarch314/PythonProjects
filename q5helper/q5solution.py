from functools import reduce # for code_metric


def separate(p,l):
    if(len(l) == 0 ):
        return tuple([[],[]])
    result = [[],[]]
    value = l[0]
    if (p(value)):
        result[0].append(value)
    else:
        result[1].append(value)
        
    tuple_t = separate(p,l[1:])##recursive call!!
    
    result[0].extend(tuple_t[0])
    result[1].extend(tuple_t[1])
    
    return tuple(result)
    pass
def is_sorted(s):
    if len(s) <= 1:
        return True
    if s[0]<s[1]:
        return is_sorted(s[1:])
    return False
  
def sort(l):
    if (len(l) <= 1):
        return l
    compare = sort(l[1:])
    return separate(lambda x : l[0] >= x,compare)[0]+[l[0]]+separate(lambda x : l[0] >= x,compare)[1]
    pass
def compare(a,b):
    if len(a) == 0 or len(b) == 0:
        if(len(a)>len(b)):
            return ">"
        if(len(a)<len(b)):
            return "<"
        return "="
    if a[0]>b[0]:
        return ">"
    if a[0]<b[0]:
        return "<"
    return compare(a[1:],b[1:])
    
def code_metric(file):
    ## filter(lambda , iterable)
    ## map(lambda, iterable) 
    ## reduce(lambda, iterable)
    file = open(file,"r").readlines()
    
    filtered = filter(lambda x : x.strip(" ") != "\n" , file)
    mapped = map(lambda x : tuple([1,len(x.rstrip("\n").rstrip(" "))]),filtered)
    reduced = reduce(lambda x,y : tuple([x[0]+y[0],x[1]+y[1]]), mapped)
    return reduced
    




if __name__=="__main__":
    import predicate,random,driver
    from goody import irange
    
    driver.driver() # type quit in driver to return and execute code below
    
    print('Testing separate')
    print(separate(predicate.is_positive,[]))
    print(separate(predicate.is_positive,[1, -3, -2, 4, 0, -1, 8]))
    print(separate(predicate.is_prime,[i for i in irange(2,20)]))
    print(separate(lambda x : len(x) <= 3,'to be or not to be that is the question'.split(' ')))
     
    print('\nTesting is_sorted')
    print(is_sorted([]))
    print(is_sorted([1,2,3,4,5,6,7]))
    print(is_sorted([1,2,3,7,4,5,6]))
    print(is_sorted([1,2,3,4,5,6,5]))
    print(is_sorted([7,6,5,4,3,2,1]))
    
    print('\nTesting sort')
    print(sort([1,2,3,4,5,6,7]))
    print(sort([7,6,5,4,3,2,1]))
    print(sort([4,5,3,1,2,7,6]))
    print(sort([1,7,2,6,3,5,4]))
    l = [i+1 for i in range(30)]
    random.shuffle(l)
    print(l)
    print(sort(l))
    
    print('\nTesting sort')
    
    print('\nTesting compare')
    print(compare('','abc'))
    print(compare('abc',''))
    print(compare('',''))
    print(compare('abc','abc'))
    print(compare('bc','abc'))
    print(compare('abc','bc'))
    print(compare('aaaxc','aaabc'))
    print(compare('aaabc','aaaxc'))
    
    print('\nTesting code_metric')
    print(code_metric('cmtest.py'))
    print(code_metric('collatz.py'))
    print(code_metric('q5solution.py'))  # A function analyzing the file it is in
