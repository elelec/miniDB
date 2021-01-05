




# Node

def remove(self, value):
	for index, existing_val in enumerate(self.values):
		if value == existing_val:
			self.values.pop(index)
			self.ptrs.pop(index)
			break


# Btree

def merge(self, node_left, node_right, oldParValue = None):
	print("PREPREMERGE")
	if node_left == node_right or node_left.parent != node_right.parent:
		return False
	
	print("PREMERGE")
	## Finds the point where the two nodes meet in the parent node
	par = node_left
	parInd = None
	
	while par != None:
		if par.parent == None:
			return False
		par = self.nodes[par.parent]
		
		if oldParValue in par.values:
			parInd = par.values.index(oldParValue)
			break
		
	if parInd is None:
		return False
	
	## Merges the two nodes
	node_left.values = node_left.values + node_right.values
	node_left.ptrs = node_left.ptrs + node_right.ptrs
	
	parVal = par.values[parInd]
	
	print("MERGE")
	# removes the right node from the parent
	for i in par.ptrs:
		if self.nodes[i] == node_right:
			par.ptrs.remove(i)
			par.values.remove(parVal)
			print("FOUND")
			break

	#par.remove(parVal)
	#par.values.pop(index)
	#par.ptrs.pop(index)
	
	
	return True

def delete(self, value):
	## finds the index of the value's node

	nodeIndex = self._search(value)
	nod = self.nodes[nodeIndex]
	print(str(nod.values) + str(nod.ptrs) + str(nod.is_leaf))
	
	if not value in nod.values:
		print("Could not find value in tree!")
		return
	
	#ptr = self.nodes[nod.parent].find(value)
	
	if nod.parent != None:
		print("Parent: " + str(self.nodes[nod.parent].values) + str(self.nodes[nod.parent].ptrs))
	else:
		print("Node is root")
	
	# Checks if the value exists in internal nodes
	isInInternal = False
	checkNode = nod
	while checkNode.parent != None:
		checkNode = self.nodes[checkNode.parent]
		if value in checkNode.values:
			isInInternal = True
			break
	
##########################################################################
########## Case the value isn't present in the internal nodes ############
##########################################################################
	if not isInInternal:
		print("Case 1 leaf only")
		nod.remove(value)
		
		if len(nod.values) < int(self.b / 2):
			print("Node too small")
			sib = self.nodes[nod.right_sibling]
			
			par = self.nodes[nod.parent]
			while not sib.values[0] in par.values:
				par = self.nodes[par.parent]
			
			nod.insert(sib.values[0], sib.ptrs[0])
			ptr = sib.find(sib.values[1])
			par.values[par.values.index(sib.values[0])] = sib.values[1]
			sib.remove(sib.values[0])

#############################################################################################
########## Case the value is present and the internal node will follow the rules ############
#############################################################################################
	else:
		print("Case 2 exists in internal")
		par = self.nodes[nod.parent]
		while not nod.values[0] in par.values:
			par = self.nodes[par.parent]
		
		if len(nod.values) - 1 > int(self.b / 2):
			print("More than min keys")
			nod.remove(value)
			par.values[par.values.index(value)] = nod.values[0]
		elif len(nod.values) - 1 == int(self.b / 2):
			print("Exactly minimum keys")
			nod.remove(value)
			
			sib = self.nodes[nod.left_sibling]
			if len(sib.values) - 1 < len(self.nodes[nod.right_sibling].values) - 1:
				print("right")
				sib = self.nodes[nod.right_sibling]
				par.values[par.values.index(value)] = nod.values[0]
				nod.insert(sib.values[0], sib.ptrs[0])
				sib.remove(sib.values[0])
			else:
				print("left")
				par.values[par.values.index(value)] = sib.values[-1]
				nod.insert(sib.values[-1], sib.ptrs[-1])
				sib.remove(sib.values[-1])
		elif par.parent != None and len(self.nodes[par.parent].values) == 1:
			print("Empty grandparent node")
			nod.remove(value)
			if nod.right_sibling != None and self.merge(nod, self.nodes[nod.right_sibling], value) == False:
				self.merge(self.nodes[nod.left_sibling], nod, value)
		else:
			nod.remove(value)
			print("Other")
			if nod.right_sibling != None and self.merge(nod, self.nodes[nod.right_sibling], value) == False:
				self.merge(self.nodes[nod.left_sibling], nod, value)
			
			