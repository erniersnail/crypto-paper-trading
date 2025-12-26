"""
Given a string s consisting of lowercase English Letters. 
return the first non-repeating character in s. If there is no non-repeating character, return '$
"""

string = "geeksforgeeks"
n = len(string)
new = {}
count = 0

for s in string:
    if s in new:
        new[s] += 1
    else:
        count = 1
        new[s] = count
        
print(new)
