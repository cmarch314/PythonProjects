from collections import defaultdict
from goody       import safe_open

# Prompt the user for a file name (to 'r'ead) and ensure the name of the file
# entered exists: see the sample file xrefin.txt; observe what happens if you
# enter the name of a file that does not exist
file = safe_open('Enter name of file to cross-reference','r','Illegal file name')

# When accessing the value associated with any key, substitute a parameterless call
# to set -set()- as the association, if the key is not present in the defaultdict.
xref = defaultdict(set)

# Iterate over every line_number and line in the file
#    Strip the newline off the right end of the text and covert it to all lower case
#    If the result is not an empty line
#      Iterate over a list of words separated by the space character
#        Add the current line_number to the set of line numbers associated with each word
#          (recall for defaultdict, if xref[word] does not exist, associate it with
#          set() before mutating the set to include line_number
for line_number,text in enumerate(file,1):
    text = text.rstrip().lower()
    if len(text) != 0:
        for word in text.split(' '):
            xref[word].add(line_number)
 
# Compute the maximum length of all words that are keys in xref
# Iterate over every word and its associated set in the in xref, in the standard order
#    Print every word formatted to be left-justified in the appropriate field-width,
#      followed by a string that joins together the string equivalent of the values
#      in the set, in sorted order
#       
max_len = max(len(x) for x in xref.keys())
for word,lines in sorted(xref.items()):
    print( ('{word:<'+str(max_len)+'}: {lines}').
           format(word=word,lines=', '.join(str(x) for x in sorted(lines))))

# For example, if max_len is 10, then the string object that format operates on is
# '{word:<10}: {lines}' which specifies the value matching word is left justified in
# a fixed field width of 10. See 6.1.3.1 in the Python Library for the meanings of the
# parts of format specification.

# str(x) for x in sorted(lines) produces a generator for a tuple containing the string
# equivalent of each set of lines: if the set were {2, 5, 1} think of the result being
# able to iterate over the tuple ('1', '2', '5')

# The call to join produces one big string, built by using ', ' to separate all the
# strings the generator for a tuple: '1, 2, 5'