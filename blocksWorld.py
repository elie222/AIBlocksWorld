import util
import copy

'''
TODO: 
Heuristic functions for A*
Solve the problem in other ways?
Create more complicated tests
GUI - using PyQt4 to do this.
'''

class BlocksWorldSolver:
    ## Initialization code
    def __init__(self):
 	"""
	Initialize the gloal variables, and function dictionaries
	"""
	self.startState = {}
	self.goalState = {}
	self.cranesNum = 1
	self.tableSpace = "infinite"
	self.method = {"BFS": breadthFirstSearch, "DFS": depthFirstSearch, "UCS": uniformCostSearch, "aStar": aStarSearch}

    """
    Start and goal states have to be fully defined.
    """
    def getStartState(self):
        return self.startState

    def getGoalState(self):
        return self.goalState
    
    def setStartState(self, state):
        self.startState = state

    def setGoalState(self, state):
        self.goalState = state
	### need to add the cranes to the state	
    def setCranesNum(self, num):
        self.cranesNum = num
		
    def setTableSpace(self, num):
        self.tableSpace = num

    def isGoalState(self, state):
        if state == self.getGoalState():
            return True
        else:
            return False

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """  
        ##print "state: \n" , state
        successors = []
        if state["HOLDING"] is None:
            # pick up a block that is clear
            for obj in state:
                if obj == "HOLDING":
                    continue
                successor = pickUp(state,obj)
                if not successor == None:
                    successors.append((successor,"PICK UP " + obj,1))                       
        else:
            # put down the block that is currently being held and put it on top of a clear block or the table
            for obj in state:
                if obj == "HOLDING":
                    continue
                successor = putDown(state,obj)
                if not successor is None:
                    successors.append((successor,"PUT DOWN " + state["HOLDING"] + " ON " + obj,1))
            if tableIsFree(state, self.tableSpace):        
				successor = putDown(state,"TABLE")
				if not successor is None:
					successors.append((successor,"PUT DOWN " + state["HOLDING"] + " ON TABLE",1))
        ##print "successors: \n" , successors    
        return successors
            
    def solve(self, methodName, heuristic=None):
		if heuristic == None:
			sol = self.method[methodName](self)
		else:
			sol = self.method[methodName](self,heuristic)
		if sol == "there is no solution to this problem":
			print sol
		else:
			print 'Solultion length:', len(sol)
			print 'Solution:\n', sol

"""
Return the state we get to when we pick up obj from state.
Returns None if the operation is illegal.
obj is a string. (eg. "A" or "B")
"""
def pickUp(state, obj):
##    print "\nPICK UP.\nstate:", state, "\nobj:", obj, "\n"

    if not state[obj]["under"] == None or not state["HOLDING"] == None:
        return None
        #raise Exception("Cannot pick up", obj)
    else:
        newState = copy.deepcopy(state)
        newState["HOLDING"] = obj
        newState[obj]["on"] = None

        if not state[obj]["on"] == "TABLE":
            newState[state[obj]["on"]]["under"] = None

        return newState
"""
Return the state we get to when we put down the object that is currently
being held onto obj.
Returns None if the operation is illegal.
obj is a string. (eg. "A" or "B" or "TABLE")
"""
def putDown(state, obj):
##    print "\nPUT UP.\nstate:", state, "\nobj:", obj, "\n"

	if state["HOLDING"] == None or obj == state["HOLDING"]:
		return None
	else:
		if not obj == "TABLE": 
			##print "state[HOLDING] = " , state["HOLDING"]
			##print obj , " is under: " , state[obj]["under"]
			if not (state[obj]["under"] == None):
				##print "in if: " , obj , " is under: " , state[obj]["under"]
				return None
		newState = copy.deepcopy(state)
		newState["HOLDING"] = None
		newState[state["HOLDING"]]["on"] = obj
		if not obj == "TABLE":
			newState[obj]["under"] = state["HOLDING"]
		return newState

def tableIsFree(state, maxSpace):
	if maxSpace == "infinite":
		return True
	usedSpace = 0
	for obj in state:
		if obj == "HOLDING":
			continue
		if state[obj]["on"] == "TABLE":
			usedSpace +=1
	if usedSpace > maxSpace:
		print "Error: exceeded table space"
		return False
	elif usedSpace == maxSpace:
		return False
	else:
		return True
"""
Algorithms
"""
def getStatePathFromNode(givenNode, problem):
  """
  return the path of the given node
  """
  givenNodePath = []
  curNode = givenNode

  while(curNode[0] != problem.getStartState()):
    givenNodePath.append(curNode[1])
    curNode = curNode[3]
  givenNodePath.reverse()
  return givenNodePath

## I don't know what this is, but I don't think we need it.
##def getStatePathFromNode(givenNode):
##    """
##    return the path of the given node
##    """
##    givenNodePath = []
##    curNode = givenNode
##
##    while(curNode[0] != self.startState):
##        givenNodePath.append(curNode[1])
##        curNode = curNode[3]
##    givenNodePath.reverse()
##    return givenNodePath

def depthOrBreadthFirstSearch(problem, container):
    """
    preform the depthFirstSearch or the breadthFirstSearch
    according to the given container
    """
    firstNode = (problem.getStartState(), None, 0, None)#state, action to reach, incremental cost, parent node
    container.push(firstNode)
    visitedStates = []
    while (not container.isEmpty()):
        curNode = container.pop()
        if (problem.isGoalState(curNode[0])):
            return getStatePathFromNode(curNode, problem)
        for successor in problem.getSuccessors(curNode[0]):
            if not successor[0] in visitedStates:
                successorNode = (successor[0], successor[1], successor[2], curNode)
                visitedStates.append(successor[0])
                container.push(successorNode)
    return "there is no solution to this problem"

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  container = util.Stack()  
  return depthOrBreadthFirstSearch(problem, container)

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  container = util.Queue()  
  return depthOrBreadthFirstSearch(problem, container)

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  return aStarSearch(problem)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  frontier = util.PriorityQueue()
  explored = []
  firstNode = (problem.getStartState(), None, 0, None)#state, action to reach, incremental cost, parent node
  frontier.push(firstNode, 0)

  while(not frontier.isEmpty()):
    curNode = frontier.pop()
    if(curNode[0] in explored):
      continue
    if(problem.isGoalState(curNode[0])):
      return getStatePathFromNode(curNode, problem)
    for successor in problem.getSuccessors(curNode[0]):
      if(successor[0] not in explored):
        successorNode = (successor[0], successor[1], curNode[2]+successor[2], curNode)
        frontier.push(successorNode, curNode[2]+successor[2]+heuristic(successor[0], problem))
    explored.append(curNode[0])
  return "there is no solution to this problem"

def anotherHeuristic(state, problem):
    '''
    This heuristic calculates the no. of differences between the goal state and the current state.
    '''
    h = 0
    goalState = problem.getGoalState()
    for x in state:
        if not state[x] == goalState[x]:
            h += 1
##    print 'anotherHeuristic. h =', h 
    return h

def anotherHeuristic2(state, problem):
    '''
    This heuristic calculates the no. of differences between the goal state and the current state.
    '''
    h = 0
    goalState = problem.getGoalState()
    for x in state:
        for y in state[x]:
            if not state[x][y] == goalState[x][y]:
                h += 1
##    print 'anotherHeuristic. h =', h 
    return h

def test(name, ws, gs, method, heuristic=None):
    print name
    s = BlocksWorldSolver()
    s.setStartState(ws)
    s.setGoalState(gs)

    s.solve(method, heuristic)
		
def runMain():
    """
    Test function to run all tests provided with project requirement
    documentation and a few more.
    """
    ## Test 1 - DFS Test
    name = "=== Running Test 1 - DFS ==="
    ws = {"A": {"on": "TABLE", "under": None}, "B": {"on": "TABLE", "under": "C"}, "C": {"on": "B", "under": None}, "HOLDING": None}
    gs = {'A': {'on': 'B', 'under': None}, 'B': {'on': 'TABLE', 'under': "A"}, 'C': {'on': 'TABLE', 'under': None}, "HOLDING": None}
    test(name, ws, gs, 'DFS')

    ## Test 2 - BFS Test
    print "\n=== Running Test 2 - BFS ==="
    ws = {"A": {"on": "TABLE", "under": None}, "B": {"on": "TABLE", "under": "C"}, "C": {"on": "B", "under": None}, "HOLDING": None}
    gs = {'A': {'on': 'B', 'under': None}, 'B': {'on': 'TABLE', 'under': "A"}, 'C': {'on': 'TABLE', 'under': None}, "HOLDING": None}
    s = BlocksWorldSolver()
    s.setStartState(ws)
    s.setGoalState(gs)
    
    s.solve("BFS")

    ## Test 3 - UCS Test
    print "\n=== Running Test 3 - UCS ==="
    ws = {"A": {"on": "TABLE", "under": None}, "B": {"on": "TABLE", "under": "C"}, "C": {"on": "B", "under": None}, "HOLDING": None}
    gs = {'A': {'on': 'B', 'under': None}, 'B': {'on': 'TABLE', 'under': "A"}, 'C': {'on': 'TABLE', 'under': None}, "HOLDING": None}
    s = BlocksWorldSolver()
    s.setStartState(ws)
    s.setGoalState(gs)
    
    s.solve("UCS")

    ## Test 4 - a* Test
    print "\n=== Running Test 4 - A* with with nullHeuristic (same as UCS) ==="
    ws = {"A": {"on": "TABLE", "under": None}, "B": {"on": "TABLE", "under": "C"}, "C": {"on": "B", "under": None}, "HOLDING": None}
    gs = {'A': {'on': 'B', 'under': None}, 'B': {'on': 'TABLE', 'under': "A"}, 'C': {'on': 'TABLE', 'under': None}, "HOLDING": None}
    s = BlocksWorldSolver()
    s.setStartState(ws)
    s.setGoalState(gs)
    
    s.solve("aStar", heuristic=nullHeuristic)

    ## Test 5 - a* Test with anotherHeuristic
    print "\n=== Running Test 5 - A* with anotherHeuristic ==="
    ws = {"A": {"on": "TABLE", "under": None}, "B": {"on": "TABLE", "under": "C"}, "C": {"on": "B", "under": None}, "HOLDING": None}
    gs = {'A': {'on': 'B', 'under': None}, 'B': {'on': 'TABLE', 'under': "A"}, 'C': {'on': 'TABLE', 'under': None}, "HOLDING": None}
    s = BlocksWorldSolver()
    s.setStartState(ws)
    s.setGoalState(gs)
    s.solve("aStar", heuristic=anotherHeuristic)
	
	## Test 6 - table size check1
    print "\n=== Running Test 6 - BFS with table size check1 ==="
    ws = {"A": {"on": "TABLE", "under": None}, "B": {"on": "TABLE", "under": "C"}, "C": {"on": "B", "under": None}, "HOLDING": None}
    gs = {'A': {'on': 'B', 'under': None}, 'B': {'on': 'TABLE', 'under': "A"}, 'C': {'on': 'TABLE', 'under': None}, "HOLDING": None}
    s = BlocksWorldSolver()
    s.setStartState(ws)
    s.setGoalState(gs)
    s.setTableSpace(2)
    
    s.solve("BFS")
##    ## Test 2
##    print "nn Running Test 2 n"
##    ws = "((on A B), (on C D), (ontable B), (ontable D), (clear A), (clear C), (armempty))"
##    gs = "((on C B), (on D A), (ontable B), (clear D))"
##    s = BlocksWorldSolver()
##    s.populateGoal(gs)
##    s.populateWorld(ws)
##    s.solve()
##
##    ## Test 3
##    print "nn Running Test 3 n"
##    ws = "((clear A), (armempty), (clear D), (ontable C),  (ontable D), (on B C), (on A B))"
##    gs = "((ontable C), (ontable D), (on B D), (clear A), (on A C),  (clear B))"
##    s = BlocksWorldSolver()
##    s.populateGoal(gs)
##    s.populateWorld(ws)
##    s.solve()
##
##    # Test 2 with extra goal state
##    print "nn Running Test 2 with extra Goal State n"
##    ws = "((on A B), (on C D), (ontable B), (ontable D), (clear A), (clear C), (armempty))"
##    gs = "((on C B), (on D A), (ontable B), (clear D),(ontable A))"
##    s = BlocksWorldSolver()
##    s.populateGoal(gs)
##    s.populateWorld(ws)
##    s.solve()
 
if __name__ == "__main__" :
    runMain()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
