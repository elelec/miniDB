from btree import Btree
from random import randrange
import sys
'''
Test the Btree
'''


NUM = min(int(sys.argv[1]), 30)
B = int(sys.argv[2])

lst = []

while len(lst)!=NUM:
	new_v = randrange(30)
	if new_v not in lst:
		lst.append(new_v)


# To test script changes with the same sequence, saving to a file is allowed
print(len(sys.argv))
if len(sys.argv) < 3 or sys.argv[3] != "load":
	dataBack = open('lastLine.txt', 'w')
	for i in lst:
		dataBack.writelines(str(i) + "\n")
	dataBack.close()
else:
	print("loaded previous sequence")
	dataBack = open('lastLine.txt', 'r')
	lines = dataBack.readlines()
	
	lst = []
	for i in lines:
		lst.append(int(i))
	
	dataBack.close()

bt = Btree(B)

for ind, el in enumerate(lst):
	#print(el, ind)
	bt.insert(el, ind)


bt.plot("Pre")
bt.delete(20)
bt.plot("Post")

#bt.show()

print(lst)

