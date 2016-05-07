# Calvin Choi, Lab 1
# Ho Choi, Lab 1
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import safe_open
from collections import defaultdict

def read_ndfa(file_passed: str) -> dict:
    ''' Returns dictionary representing the non-deterministic finite automaton
    '''
    ndfa_dict = defaultdict(dict)
    lines_in_file = file_passed.readlines()
    for i in range(len(lines_in_file)):
        line = lines_in_file[i].rstrip('\n').split(';')
        inner_dict = defaultdict(set)
        for j in range(0, len(line[1:]), 2):
            inner_dict[line[1:][j]].add(line[1:][j + 1])
        ndfa_dict[line[0]] = inner_dict
        
    return ndfa_dict
            
        

def print_ndfa(d: dict) -> None:
    ''' Prints the ndfa in the appropriate form
    '''
    print("Non-Deterministic Finite Automaton")
    
    ndfa_list = []
    for key in d.keys():
        ndfa_list.append((key, sorted(d[key].items())))
    
    ndfa_list.sort()
    
    for i in ndfa_list:
        print("   {} transitions: {}".format(i[0], i[1]))
        
    return None
    
def process(d: dict, start_state: str, inputs: [str]) -> list:
    ''' Returns a list that contains the start-state followed by 
        tuples that show the input and resulting state after each
        transition. 
    '''
    result = [start_state]
    Possible_states = {start_state}
    for input_command in inputs:
        new_states = set()
        for pos_state in Possible_states:
            new_states.update(d[pos_state][input_command])
        if new_states != set():
            next_pair = tuple([input_command,new_states])
            Possible_states = new_states
            result.append(next_pair)
    return result
def interpret(process_result: list) -> None:
    ''' Prints the results of processing a ndfa on an input
    '''
    print("\nStarting new simulation")
    print("Start state = {}".format(process_result[0]))
    for input_state in process_result[1:]:
        print("   Input = {}; new possible states = {}".format(input_state[0], input_state[1]))
    print("Stop state(s) = {}".format(process_result[-1][1]))


if __name__ == '__main__':
    #ndfa = safe_open("Enter file with non-deterministic finite automaton",'r','Illegal file name')
    ndfa = open('ndfare.txt', 'r')  # for testing. 
    ndfa_dict = read_ndfa(ndfa)
    #print_ndfa(ndfa_dict)
    #simul_data = safe_open("Enter file with start-state and input", 'r', 'Illegal file name')
    simul_data = open('ndfainput2re.txt', 'r')  # for testing
    print()
    for sim in simul_data.readlines():
        processed = process(ndfa_dict, sim.rstrip('\n').split(';')[0], sim.rstrip('\n').split(';')[1:])
        interpret(processed)    
 
    