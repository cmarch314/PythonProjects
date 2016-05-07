# Calvin Choi, Lab 1
# Ho Choi, Lab 1
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
from collections import defaultdict
from goody import safe_open
from goody import read_file_values
from random import randrange
def read_corpus(order_static:int, text_file)->dict:
    '''
    the function creates corpus(tuple:list(str))
    and return it.
    '''
    corpus = defaultdict(list)
    raw_words = []
    for word in read_file_values(text_file):
        raw_words.append(word.rstrip("\n"))               # create long list of all words from text_file
    for word_index in range(len(raw_words)-order_static):   # iterate based on lenth of the list by index 
        ## here is fun part, create tuple using comprehension removing \n in front of every first line's letter 
        ## using index tuple will iterate from index through index + order_static which will be tuple(list[index], list[index+1] ... list[index+order_static-1])
        ## then put the tuple into corpus as a key 
        ## append list[index+order_static] to value(list) if it is not in list
        if corpus[tuple(word.lstrip("\n") for word in raw_words[word_index:word_index+order_static])].count(raw_words[word_index + order_static].lstrip("\n")) == 0:
            corpus[tuple(word.lstrip("\n") for word in raw_words[word_index:word_index+order_static])].append(raw_words[word_index + order_static].lstrip("\n"))
    return corpus
def print_corpus(corpus:dict):
    '''
    min and max counts length of list in dict values by sorting and navigated using index
    in for loop, the state displays dictionary iterated and sorted by key
    at last print min and max
    '''
    min_len = len(sorted(corpus.values(), key = len)[0])
    max_len = len(sorted(corpus.values(), key = len)[-1])
    for key in sorted(corpus.keys()):
        print("{} can be followed by any of {}".format(key,corpus[key]))
    print("min/max = {}/{}".format(min_len,max_len))
        
def produce_text(corpus:dict, starting_words:list, count:int)->list:
    '''
    at the beginning, this function copies list of starting words.
    then iterates by counts which will be used as index of list
    new_index is randomly generated integer from length of value of dict 
    in randrange, passing list into tuple will gives key and the key will be shifted by +1 as loop proceeds.
    after generate new_index which will be choose the next word, result(list) will append the next word
    the word will be treated as last word in tuple of next key
    finally it returns result
    note: exception will handle end of path problem and the function will be terminated and returns list at that point.
    '''
    result = starting_words
    try:
        for index in range(count):
            new_index = randrange(len(corpus[tuple(result[index:index+len(starting_words)])]))
            result.append(corpus[tuple(result[index:index+len(starting_words)])]
                          [new_index])##randomly generated new index will choose next word.
    except:
        pass## end of path
    return result

if __name__ == "__main__":
    '''
    the main function will take file name
    and static value for positive integer
    then print it as valid format
    asking values of tuple based on order static value 
    '''
    file = safe_open('file to read','r','Illegal file name')
    while True:
        number = int(input("order static value(positive):"))
        if(number > 0):
            break
    readed = read_corpus(number,file)
    print_corpus(readed)
    starting_w = []
    for i in range(number):
        starting_w.append(input("enter word {}:".format(i+1)))
    result = produce_text(readed,starting_w, int(input("Enter #of words:")))
    print("random text = {}".format(result))
