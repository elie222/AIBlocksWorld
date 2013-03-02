class BlocksWorldSolver:
 
   ## Initialization code
   def __init__(self):
 	"""
		Initialize the gloal variables, and function dictionaries
		"""
		self.startState = {}
		self.goalState = {}
		self.method = {"BFS": breadthFirstSearch, "DFS": depthFirstSearch}
	   

	def setStartState(self, state):
		self.startState = state

	def setGoalState(self, state):
		self.goalState = state
		
		
	def solve(self, methodName)
		self.method[methodName]()
		
		
		
	def breadthFirstSearch():
	
	def depthFirstSearch():
	
	def nullHeuristic():
		"""
		A heuristic function estimates the cost from the current state to the nearest
		goal in the provided SearchProblem.  This heuristic is trivial.
		"""
		return 0
	
	def aStarSearch(heuristic=nullHeuristic):
		"Search the node that has the lowest combined cost and heuristic first."
		frontier = util.PriorityQueue()
		explored = []
		firstNode = (self.startState, None, 0, None)#state, action to reach, incremental cost, parent node
		frontier.push(firstNode, 0)

		while(not frontier.isEmpty()):
			curNode = frontier.pop()
			if(curNode[0] in explored):
				continue
			if(self.goalState == curNode[0]):
				return getStatePathFromNode(curNode)
			for successor in getSuccessors(curNode[0]):
				if(successor[0] not in explored):
					successorNode = (successor[0], successor[1], curNode[2]+successor[2], curNode)
					frontier.push(successorNode, curNode[2]+successor[2]+heuristic(successor[0]))
			explored.append(curNode[0])
		print "Error: no path from start state to goal state"
		
	def getSuccessors(state):
		if state[ARMHOLDING] == "NONE":
			
			
		else:
			
	def getStatePathFromNode(givenNode):
		"""
		return the path of the given node
		"""
		givenNodePath = []
		curNode = givenNode

		while(curNode[0] != self.startState):
			givenNodePath.append(curNode[1])
			curNode = curNode[3]
		givenNodePath.reverse()
		return givenNodePath
		
		
def runMain():
   """
   Test function to run all tests provided with project requirement
   documentation and a few more.
   """
   ## Test 1
   print "nn Running Test 1 n"
   ws = "((on C B), (ontable B), (ontable A), (clear A), (clear C), (armempty))"
   gs = "((on A B), (ontable B), (clear A))"
   s = BlocksWorldSolver()
   s.populateGoal(gs)
   s.populateWorld(ws)
   s.solve()
 
   ## Test 2
   print "nn Running Test 2 n"
   ws = "((on A B), (on C D), (ontable B), (ontable D), (clear A), (clear C), (armempty))"
   gs = "((on C B), (on D A), (ontable B), (clear D))"
   s = BlocksWorldSolver()
   s.populateGoal(gs)
   s.populateWorld(ws)
   s.solve()
 
   ## Test 3
   print "nn Running Test 3 n"
   ws = "((clear A), (armempty), (clear D), (ontable C),  (ontable D), (on B C), (on A B))"
   gs = "((ontable C), (ontable D), (on B D), (clear A), (on A C),  (clear B))"
   s = BlocksWorldSolver()
   s.populateGoal(gs)
   s.populateWorld(ws)
   s.solve()
 
   # Test 2 with extra goal state
   print "nn Running Test 2 with extra Goal State n"
   ws = "((on A B), (on C D), (ontable B), (ontable D), (clear A), (clear C), (armempty))"
   gs = "((on C B), (on D A), (ontable B), (clear D),(ontable A))"
   s = BlocksWorldSolver()
   s.populateGoal(gs)
   s.populateWorld(ws)
   s.solve()
 
if __name__ == "__main__" :
   runMain()
