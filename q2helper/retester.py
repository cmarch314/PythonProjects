import re
import prompt
from goody import safe_open 

def embed(value):
    return (None if value == None else "\""+value+"\"")
    
def test_match(pat,txt):
    m = re.match(pat,txt)
    if not m:
        print("    No match")
    else:
        print("    match =",m.groups())
        for g in range(0,len(m.groups())+1):
            print("    group #",g,":span",m.span(g)," = ",embed(m.group(g)),sep="")
 
    
def test_search(pat,txt):
    m = re.search(pat,txt)
    if not m:
        print("    No match")
    else:
        print("    match =",m.groups())
        for g in range(0,len(m.groups())+1):
            print("    group #",g,":",m.span(g)," = ",embed(m.group(g)),sep="")
 
    
def test_findall(pat,txt):
    fa = re.findall(pat,txt)
    if not fa:
        print("    No match")
    else:
        print("    findall =",fa)
        mn = 0
        for x in fa:
            mn += 1
            print("    match #"+str(mn))
            if isinstance(x,str):
                print("        string =",x)
            else:
                gn = 0
                for g in x:
                    gn += 1
                    print("        group #"+str(gn),"=",g)
                    
                    
def test_substitute(pat,rpl,txt):
    print("    result string =",re.sub(pat,rpl,txt))


def test_split(pat,txt):
    print("    result list =",re.split(pat,txt))
    
    
def repeat(func,**kargs):
    while True:
        test = prompt.for_string("Enter txt",default="")
        kargs["txt"] = test
        if test == "" :
            break;
        func(**kargs)
    
def batch(func,**kargs):
    in_file = safe_open("Enter batch file for txt", "r", "Cannot find that file")
    for test in in_file:
        kargs["txt"] = text = test.strip()
        print("Trying txt =",text)
        func(**kargs)
    
    
if __name__ == "__main__": 
    print("Begin Regular Expression (re) testing") 
    commandPrompt = \
"""
Operations                re methods          General
  et - enter txt            m  - match          rm/bm   - repeat/batch match
  ep - enter pat            s  - search         rs/bs   - repeat/batch search
  er - enter rpl            fa - findall        rfa/bfs - repeat/batch findall
  ?  - show t/p/r           su - substitute     rsu/bsu - repeat/batch substitute
                            sp - split          rsp/bsp - repeat/batch split
                                                .       - exec(...)
                                                q       - quit
\nCommand""" 
    pat = ""
    txt = ""
    rpl = ""
    while True:
        try:
            action = prompt.for_string(commandPrompt, is_legal=(lambda x : x in ['et','ep','er','?','m','s','fa','su','sp','rm','bm','rs','bs','rfa','bfa','rsu','bsu','rsp','bsp','.','q']))
            if   action == 'et' : txt = prompt.for_string("Enter txt")
            elif action == 'ep' : pat = prompt.for_string("Enter pat")
            elif action == 'er' : rpl = prompt.for_string("Enter rpl",default="")
            elif action == '?'    : 
                print("    txt = ", txt)
                print("    pat = ", pat)
                print("    rpl = ", rpl)
            elif action == 'm'    : test_match(pat,txt)
            elif action == 's'    : test_search(pat,txt)
            elif action == 'fa' : test_findall(pat,txt)
            elif action == 'su' : test_substitute(pat,rpl,txt)
            elif action == 'sp' : test_split(pat,txt)
            elif action == 'rm' : repeat(test_match,pat=pat)
            elif action == 'rs' : repeat(test_search,pat=pat)
            elif action == 'rfa': repeat(test_findall,pat=pat)
            elif action == 'rsu': repeat(test_substitute,pat=pat,rpl=rpl)
            elif action == 'rsp': repeat(test_split,pat=pat)
            elif action == 'bm' : batch(test_match,pat=pat)
            elif action == 'bs' : batch(test_search,pat=pat)
            elif action == 'bfa': batch(test_findall,pat=pat)
            elif action == 'bsu': batch(test_substitute,pat=pat,rpl=rpl)
            elif action == 'bsp': batch(test_split,pat=pat)
            elif action == "."  : exec(prompt.for_string("    Enter command to exec (can use txt,pat,rpl)"))
            elif action == 'q'  : break
            else: print("    Unknown command")
        except AssertionError as report:
            print("    AssertionError exception caught:", report)
        except Exception as report:
            import traceback
            traceback.print_exc()
    print("\nFinshed Regular Expression (re) testing")