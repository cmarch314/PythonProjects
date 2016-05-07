# Calvin Choi, Lab 1
# Ho Choi, Lab 1
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from collections import defaultdict

def read_graph(file: str) -> dict:
    ''' Takes an open (file) parameter. Returns the dict
        that represents the graph
    '''
    with open(file, 'r') as nodes:
        list_of_nodes = nodes.readlines()
        for i in range(len(list_of_nodes)):
            list_of_nodes[i] = list_of_nodes[i].rstrip().split(';')
        #print(list_of_nodes)
        
        node_dict = defaultdict(set)
        for node in list_of_nodes:
            node_dict[node[0]].add(node[1])
        #print(node_dict)
        
        return node_dict
             
        
def print_graph(d: dict) -> None:
    ''' Prints the graph in an appropriate form
    '''
    list_of_keys = []
    for key in d:
        list_of_keys.append(key)
    #print(list_of_keys)
    
    list_of_keys.sort()
    #print(list_of_keys)
    
    print("\nGraph: source -> {destination} edges")
    for i in range(len(list_of_keys)):
        print('   {} -> {}'.format(list_of_keys[i], d[list_of_keys[i]]))
        
    return None
    

def reachable(d: dict, node: str) -> {str}:
    ''' Returns a set of all nodes reachable by the user-specified start node
    '''
    exploring_nodes = [n for n in d[node]]                 #### ho choi - changed 3 lines with comprehensions
    reached_nodes = {e for e in exploring_nodes}
    reached_nodes.add(node)
    '''
    for n in d[node]:
        exploring_nodes.append(n)   # the 1st set of destination nodes
    
    reached_nodes.add(node)         # add the first starting node
    
    for n in exploring_nodes:
        reached_nodes.add(n)        # add all the reached nodes from the first node
    '''    
    #print("The starting set of exploring nodes is: ", exploring_nodes)
    
    while exploring_nodes != []:   
        new_nodes = d[exploring_nodes[0]]  # get the next node to check for destination nodes (which is the 1st item in the list)
        #print("Testing node: ", exploring_nodes[0])
        #print("The destination nodes: ", new_nodes)
        for n in new_nodes:                # for each destination node
            if n not in exploring_nodes:   # if this destination node is not already in the list for nodes to be tested
                exploring_nodes.append(n)  # then we need to add this node to test it for other reachable nodes
                #print("Exploring nodes did not have ", n, "so we are adding it to the list to be checked")
            reached_nodes.add(n)           # and for each destination node, just add it to the set of reached nodes. It won't repeat because it's just adding into a set.
            #print("Our current list of reached_nodes: ", reached_nodes)
        exploring_nodes.pop(0)             # after we are done, we will remove this node that we just checked from the front of the list. 
        
    return reached_nodes


if __name__ == '__main__':
    graph_file = input("Enter file with graph: ")
    node_dict = read_graph(graph_file)
    #print(node_dict)
    print_graph(node_dict)                 # this one is correct
    
    #node_dict2 = read_graph('graph2.txt')
    #print_graph(node_dict2)                 # this one I am assuming to be correct
    
    #node_dict3 = read_graph('graph3.txt')
    #print_graph(node_dict3)                 # this one I am also assuming to be correct
    
    while True:
        start_node = input('\nEnter starting node: ')
        if start_node == 'quit':
            break
        list_of_valid_nodes = []
    
        for n in node_dict:
            list_of_valid_nodes.append(n)     # create a list of valid nodes
        
        if start_node not in list_of_valid_nodes:   # if the user-inputed node is not a valid node
            print("  Entry Error: '" + start_node + "' ;  Not a source node")
            print("  Please enter a legal string")
            continue
            
        reachable_nodes = reachable(node_dict, start_node)
        print('From', start_node, 'the reachable nodes are', reachable_nodes)
        
        