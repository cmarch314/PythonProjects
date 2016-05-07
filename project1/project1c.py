# Calvin Choi, Lab 1
# Ho Choi, Lab 1
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
from goody       import safe_open


def read_fa(file_passed):
    result = dict()
    resource =  file_passed
    for line in resource.readlines():
        key_dest = [[],[]]
        for i in range(int((len(line.split(";"))-1)/2)):
            key_dest[0].append(line.split(";")[2*i+1])
            key_dest[1].append(line.split(";")[2*i+2].rstrip("\n"))
        result[line.split(";")[0]] = dict(zip(key_dest[0],key_dest[1]))
    return result

def print_fa(d:dict):
    keys = sorted([d for d in d.keys()])
    print("\nFinite Automation Description")
    try:
        for key in keys:
            trans = sorted([(p,v) for p,v in d[key].items()],key = lambda a: a[0])
            print("{} transitions: {}".format(key, trans))
        print("")
    except:
        print("Invalid data")

def process(d:dict, start_state:str,inputs:list)->list:
    if(inputs == []):
        return [""]
    try:
        result = [start_state]
        result.append(( inputs[0] , d[start_state][str(inputs[0])] ))
        result.extend(process(d, d[start_state][str(inputs[0])],inputs[1:])[1:])
        return result
    except:
        return ["",(inputs[0],"terminated")]
    
def interpret(processed:list):
    try:
        print("\nStarting new simulation")
        print("Start state:{}".format(processed.pop(0)))
        new_state = "new state = "
        ill_input = "illegal input: "
        for i in range(len(processed)):
            print("input = {}; {}{}".format(processed[i][0],(new_state if processed[i][1] != "terminated" else ill_input), processed[i][1]))
        print("Stop state = {}".format((processed[-1][1]) if processed[-1][1] != "terminated" else "None"))
    except:
        print("Invalid data")          
if __name__ == "__main__":
    fa_file = safe_open("Enter file with finite automaton: ",'r','Illegal file name')
    readed = read_fa(fa_file)
    print_fa(readed)
    data = safe_open("Enter file with start-state and input: ",'r','Illegal file name')
    for i in data.readlines():
        interpret(process(readed, i.split(';')[0], i.rstrip("\n").split(";")[1:]))