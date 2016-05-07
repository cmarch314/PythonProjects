def lets(iterable):
    for i in iterable:
        yield i

def transform(iterable,f):
    result = []
    for i in iterable:
        result.append(f(i))
    return result


def running_count(iterable,p):
    i = 0
    result = []
    for v in iterable:
        if p(v):
            i+=1
        result.append(i)
    return result
    pass
    
def n_with_pad(iterable,n,pad=None):
    result = []
    iterable = iter(iterable)
    while n>0:
        try:
            result.append(next(iterable))
        except:
            result.append(pad)
        n-=1
    return result
def sequence(*args):
    l = args
    result = []
    for i in l:
        for j in i:
            result.append(j)
    return result
    
def alternate(*args):
    args = [iter(i) for i in args]
    br = 0
    result = []
    while br != len(args):
        br = 0
        for iterable in args:
            try:
                result.append(next(iterable))
            except:
                br += 1
            
    return result    
if __name__ == '__main__':
    import driver
    driver.driver()
