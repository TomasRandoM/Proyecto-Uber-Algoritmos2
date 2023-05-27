import dictionary

a= ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "e22", "e23", "e532", "e12", "e84", "e11", "e13", "e14", "e15"]
dict2 = dictionary.dictionary(a)
print(dict2)

for i in a:
    print(dictionary.hashFunction(i, len(dict2)))
