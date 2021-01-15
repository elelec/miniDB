

class MultiIndex:
	
	indices = []
	def __init__(self):
		self.indices = []
	
	def setMultiIndex(self, name, value, type):
		for i in self.indices:
			if i.name == name:
				i.value = value
				i.type = type
				return
		
		self.indices.append(Index(name, value, type))
		#print(self.indices[-1].name)
	
	def removeMultiIndex(self, name):
		for i in self.indices:
			if i.name == name:
				self.indices.pop(i)

class Index:
	
	name = ""
	value = 0
	type = "str"
	
	def __init__(self, name, value. type):
		self.name = name
		self.value = value
		self.type = type


# Node

def remove(self, value):
	for index, existing_val in enumerate(self.values):
		if value == existing_val:
			self.values.pop(index)
			self.indices.pop(index)
			
			if self.is_leaf:
				self.ptrs.pop(index)
			break


# Btree

def setColumn(self, nodeValue, columnName, columnValue, columnType):
	index = self._search(nodeValue)
	
	if index != None:
		node = self.nodes[index]
		index = node.values.index(nodeValue)
		
		if (index != None):
			node.indices[index].setMultiIndex(node.indices[index], columnName, columnValue, columnType)
			print(node.indices[index].indices[-1].name + ", " + str(node.indices[index].indices[-1].value))

def removeColumn(self, nodeValue, columnName):
	index = self._search(nodeValue)
	
	if index != None:
		node = self.nodes[index]
		index = node.values.index(nodeValue)
		
		if (index != None):
			node.indices[index].removeMultiIndex(node.indices[index], columnName)
			print(node.indices[index].indices[-1].name + ", " + str(node.indices[index].indices[-1].value))

def merge(self, node_left, node_right, oldParValue = None):
	if node_left == node_right:
		print("Merge node conditions not met")
		return False
	
	# Flips the nodes if left is right
	if len(node_left.values) > 0 and len(node_right.values) > 0:
		if node_left.values[0] > node_right.values[0]:
			temp = node_left
			node_left = node_right
			node_right = temp
	
	if node_left.parent and self.nodes[node_left.parent] == node_right:
		temp = node_left
		node_left = node_right
		node_right = temp
	
	## Finds the point where the two nodes meet in the parent node
	#par = node_left.parent
	par = self.nodes[node_right.parent]
	
	# removes the right node from the parent
	for p in self.nodes:
		if p.is_leaf:
			continue
		
		for i in p.ptrs:
			if self.nodes[i] == node_right:
				print("Merged")
				#deleteParentNodeValue(self, node_right.values[0])
				
				## Merges the two nodes
				node_left.values = node_left.values + node_right.values
				node_left.ptrs = node_left.ptrs + node_right.ptrs
				node_left.indices = node_left.indices + node_right.indices
			
				indPtrs = p.ptrs.index(i)
				p.ptrs.pop(indPtrs)
				return True

	print("Didn't find node")
	
	
	return False

def delete(self, value):
	## finds the index of the value's node

	nodeIndex = self._search(value)
	nod = self.nodes[nodeIndex]
	nodPtr = self._search(value)
	emptyInternal = False
	
	if not value in nod.values:
		#print("Could not find value in tree!")
		return False
	
	print(str(value) + ", " + str(nod.values) + str(nod.ptrs) + str(nod.is_leaf))
	print("[" + str(len(nod.values)) + "], [" + str(len(nod.ptrs)) + "], [" + str(len(nod.indices)) + "]")
	
	#ptr = self.nodes[nod.parent].find(value)
	
	#if nod.parent != None:
	#	print("Parent: " + str(self.nodes[nod.parent].values) + str(self.nodes[nod.parent].ptrs))
	#else:
	#	print("Node is root")
	
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
		
		if len(nod.values) == int(self.b / 2):
			print("Node too small")
			sib = getNodeSiblings(self, nod, value)
			
			if sib == None or len(sib) == 0:
				print("No common parent sibling found")
				return False
			
			sib = sib[0]
			par = self.nodes[nod.parent]
			
			if len(nod.values) == 0:
				#self.merge(nod, sib)
				removeNodeFromParent(self, nod)
				
			return True


#############################################################################################
########## Case the value is present and the internal node will follow the rules ############
#############################################################################################
	else:
		print("Case 2 exists in internal")
		par = self.nodes[nod.parent]
		while not nod.values[0] in par.values:
			if par.parent == None:
				print("No tree thing. Value len is " + str(len(nod.values)))
				return False
			par = self.nodes[par.parent]
		
		
		sib = None
		itemInd = 0
		if nod.left_sibling == None and nod.right_sibling == None:
			print("Could not find any siblings")
		elif nod.left_sibling == None or (nod.right_sibling != None and self.nodes[nod.right_sibling].parent == nod.parent):
			sib = self.nodes[nod.right_sibling]
			itemInd = 0
			print("Priority Sibling: Right")
		else:
			sib = self.nodes[nod.left_sibling]
			itemInd = -1
			print("Priority Sibling: Left")
		
		sib = getNodeSiblings(self, nod, value)
		
		if len(nod.values) - 1 <= int(self.b / 2):
			print("Exactly minimum keys")
			ptr = nod.values.index(value)
			
			# Delete the keys
			nod.remove(value)
			if sib != None:
				# Borrow a key from sibling
				sibValue = sib[0].values[sib[1]]
				# Fill empty space with sibling or last value
				if len(nod.values) > 0:
					print("is num 1")
					sibValue = nod.values[0]
					replaceParentNodeValue(self, value, sibValue)
				elif sib[1] != 0 and len(sib[0].values) > 1:
					print("is num 2")
					replaceParentNodeValue(self, value, sibValue)
					shiftValueToNode(self, sibValue, sib[0], nod)
				else:
					print("is num 3")
					deleteParentNodeValue(self, value)
				
				if len(nod.values) == 0:
					removeNodeFromParent(self, nod)
			else:
				if len(nod.values) > 0:
					replaceParentNodeValue(self, value, nod.values[0])
				else:
					print("No sib value to replace")
					deleteParentNodeValue(self, value)
		elif len(nod.values) - 1 > int(self.b / 2):
			
			# Delete the keys
			nod.remove(value)
			# Delete from internal
			# Fill empty space with successor
			if len(nod.values) == 0:
				removeNodeFromParent(self, nod)
			else:
				replaceParentNodeValue(self, value, nod.values[0])
		
#####################################################################
########## Case the height of the tree needs to decrease ############
#####################################################################
		print("Case 3 tree balance shift")
		
		if len(par.values) == 0:
			# Removes the parent node if it's empty
			if par.parent == None and len(par.values) == 0:
				newRootNodes = []
				for n in self.nodes:
					if n.parent == None:
						continue
					if self.nodes[n.parent] == par:
						newRootNodes.append(n)
				
				# Merges all children nodes
				for i in range(1, len(newRootNodes)):
					self.merge(newRootNodes[0], newRootNodes[i])
				self.root = self.nodes.index(newRootNodes[0])
			#else:
			#	# Gets siblings
			#	parSibs = getNodeSiblings(self, par, value)
			#	if parSibs == None:
			#		print("Couldn't get parent siblings")
			#		return False
			#	else:
			#		self.merge(parSibs[0], par)
		
		# Removes node and parent
		nod.remove(value)
		deleteParentNodeValue(self, value)
		
		# if len(nod.values) == 0:
		#	 self.merge(nod, sib)
		
		# rootNodes = []
		# for i in self.nodes:
			# if i.parent and i.parent == self.root:
				# rootNodes.append(i)
		
		# if len(rootNodes) > 1:
			# for j in range(1, len(rootNodes)):
				# self.merge(rootNodes[0], rootNodes[j])
	
	#removeEmpty(self, value)
	
	return True

def shiftValueToNode(self, value, oldNode, newNode):
	ind = oldNode.values.index(value)
	newNode.insert(value, oldNode.ptrs[ind], index = oldNode.indices[ind])
	oldNode.remove(value)

def removeEmpty(self, value):
	mergeEmptyParents(self, value)
	return
	
	for i in range(0, len(self.nodes), -1):
		if (self.nodes[i].is_leaf and len(self.nodes.values) == 0):
			print("Removed an empty node!")
			
			par = self.nodes[self.nodes[i].parent]
			for j in par.ptrs:
				if self.nodes[j] == self.nodes[i]:
					ind = par.ptrs.index(j)
					par.indices.pop(ind)
					par.ptrs.pop(ind)
					par.values.pop(ind)
			#self.nodes.pop(i)

def mergeEmptyParentsSingleNode(self, node):
	while node.parent != None:
		node = self.nodes[node.parent]
		if node.parent != None and not node.is_leaf:
		
			if len(node.values) > int(self.b / 2):
				continue
			
			sibs = getNodeSiblings(self, node, value)
			if sibs != None and len(sibs) != 0:
				if len(sibs[0].values) > int(self.b / 2):
					continue
				print(node)
				self.merge(node, sibs[0])
				print("Merged node " + str(node.values) + str(sibs[0].values))

def mergeEmptyParents(self, value):
	for node in self.nodes:
		if node.parent != None and node.is_leaf:
		
			if len(node.values) > int(self.b / 2):
				continue
			
			sibs = getNodeSiblings(self, node, value)
			if sibs != None and len(sibs) != 0:
				if len(sibs[0].values) > int(self.b / 2):
					continue
				print(node)
				self.merge(node, sibs[0])
				print("Merged node " + str(node.values) + str(sibs[0].values))

def replaceParentNodeValue(self, oldVal, newVal):
	# Checks if the vlaue already exists in the tree, and deletes the value from the node instead
	#for node in self.nodes:
	#	if node.is_leaf:
	#		continue
	#	
	#	if newVal in node.values:
	#		#deleteParentNodeValue(self, oldVal)
	#		return
	
	# Replaces old value with new
	for node in self.nodes:
		if node.is_leaf:
			continue
		
		if oldVal in node.values:
			node.values[node.values.index(oldVal)] = newVal

def deleteParentNodeValue(self, oldVal):
	for node in self.nodes:
		if node.is_leaf:
			continue
		
		if oldVal in node.values:
			node.remove(oldVal)
		
		#if node.parent == None:
		#	return
		
		#if node.parent and len(self.nodes[node.parent].values) == 0:
		#	sibs = getNodeSiblings(self, node, oldVal)
		#	if sibs != None:
		#		print("Merge within merge")
		#		self.merge(node, sibs[0])
		#	else:
		#		print("No merge inside merge")

def getNodeSiblings(self, node, value):
	nodeList = []
	
	for n in self.nodes:
		if n.parent == node.parent and n != node:
			nodeList.append(n)
		
	
	closestLeft = None
	closestRight = None
	
	for n in nodeList:
		if len(n.values) == 0:
			continue
		
		if n.values[0] < value:
			if closestLeft == None or n.values[0] > closestLeft.values[0]:
				closestLeft = n
		else:
			if closestRight == None or n.values[0] < closestRight.values[0]:
				closestRight = n
	
	if closestLeft == None:
		if closestRight == None:
			return None
		
		return [closestRight, 0]
	
	return [closestLeft, -1]
	
def removeNodeFromParent(self, node):
	if node.parent == None:
		return
	
	for i in self.nodes[node.parent].ptrs:
		if self.nodes[i] == node:
			self.nodes[node.parent].ptrs.remove(i)
