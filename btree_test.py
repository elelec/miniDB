from btree import Btree
from random import randrange, choice
import sys
from time import sleep
'''
Test the Btree
'''


NUM = int(sys.argv[1])
B = int(sys.argv[2])

lst = []

while len(lst)!=NUM:
	new_v = randrange(NUM)
	if new_v not in lst:
		lst.append(new_v)


# To test script changes with the same sequence, saving to a file is allowed
print(len(sys.argv))
if len(sys.argv) < 4 or sys.argv[3] != "load":
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
i = 0
for q in range(0, 5):
	n = randrange(NUM)
	
	if bt.delete(n) == True:
		i = i + 1
		bt.plot("/Step " + str(i))
		print("Step " + str(i))
		sleep(0.2)
		print("--------")
	#else:
	#	sleep(0.02)
	
#bt.delete(2)
#bt.setColumn(1, "Students", 14)
bt.plot("Post")

#bt.show()

print(lst)

