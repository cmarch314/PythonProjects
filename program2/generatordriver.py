from generator import transform, running_count, n_with_pad, sequence, alternate

# A generator for iterating through any iterable (mostly used to
#  iterate through the letters in a string).
# It is present and called to ensure that your generator code works on
#   general iterable parameters (not just a string, list, etc.)
# For example, although we can call len(string) we cannot call
#   len(lets(string)), so the generator functions you write should not
#   call len on their parameters
def lets(iterable):
    for i in iterable:
        yield i

        

for i in transform('abCdeFg',str.upper):
    print(i,end=' ')
print()

for i in transform(lets('abCdeFg'),str.upper):
    print(i,end=' ')
print()

  
   
for i in running_count('bananastand',lambda x : x in 'aeiou'): # is vowel
    print(i,end=' ')
print()

for i in running_count(lets('bananastand'),lambda x : x in 'aeiou'): # is vowel
    print(i,end=' ')
print()



for i in n_with_pad('abcdefg',3,None):
    print(i,end=' ')
print()

for i in n_with_pad('abcdefg',10,'?'):
    print(i,end=' ')
print()

for i in n_with_pad('abcdefg',10):
    print(i,end=' ')
print()

for i in n_with_pad(lets('abcdefg'),10):
    print(i,end=' ')
print()



for i in sequence('abcde','fg','hijk'):
    print(i,end=' ')
print()

for i in sequence(lets('abcde'),lets('fg'),lets('hijk')):
    print(i,end=' ')
print()



for i in alternate('abcde','fg','hijk'):
    print(i,end=' ')
print()

for i in alternate(lets('abcde'),lets('fg'),lets('hijk')):
    print(i,end=' ')
print()