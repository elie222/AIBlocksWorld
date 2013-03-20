import util
import copy
from random import sample, randint, uniform, shuffle, choice
from math import exp
from prettytable import PrettyTable

'''
TODO: 
Heuristic functions for A*
Solve the problem in other ways?
Create more complicated tests
GUI - using PyQt4 to do this.
'''

MAX_NODES_TO_EXPLORE = 3000
NO_OF_TESTS = 20
MIN_BLOCKS_TO_TEST = 3
MAX_BLOCKS_TO_TEST = 5
INCREMENT = 1

class BlocksWorldSolver:
    ## Initialization code
    def __init__(self):
 	"""
	Initialize the gloal variables, and function dictionaries
	"""
	self.startState = {}
	self.goalState = {}
	self.nodesExpanded = 0
	self.tableSpace = "infinite"
	self.method = {"BFS": breadthFirstSearch, "DFS": depthFirstSearch, "UCS": uniformCostSearch, "aStar": aStarSearch, "SA":  simulateAnnealing}

    """
    Start and goal states have to be fully defined.
    """
    def getStartState(self):
        return self.startState

    def getNodesExpandedNum(self):
        return self.nodesExpanded

    def getGoalState(self):
        return self.goalState
    
    def setStartState(self, state):
        self.startState = state

    def setGoalState(self, state):
        self.goalState = state

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
        self.nodesExpanded +=1
        return successors
            
    def solve(self, methodName, heuristic=None):
		if heuristic == None:
			sol = self.method[methodName](self)
		else:
			sol = self.method[methodName](self,heuristic)
		return sol

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

def depthOrBreadthFirstSearch(problem, container):
    """
    preform the depthFirstSearch or the breadthFirstSearch
    according to the given container
    """
    firstNode = (problem.getStartState(), None, 0, None)#state, action to reach, incremental cost, parent node
    container.push(firstNode)
    visitedStates = []
    while (not container.isEmpty()):
        if problem.getNodesExpandedNum() > MAX_NODES_TO_EXPLORE:
            return None
        curNode = container.pop()
        if (problem.isGoalState(curNode[0])):
            return getStatePathFromNode(curNode, problem)
        for successor in problem.getSuccessors(curNode[0]):
            if not successor[0] in visitedStates:
                successorNode = (successor[0], successor[1], successor[2], curNode)
                visitedStates.append(successor[0])
                container.push(successorNode)
    return None

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
    if problem.getNodesExpandedNum() > MAX_NODES_TO_EXPLORE:
        return None
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
  return None

def blocksInPlacerHeuristic(state, problem):
    '''
    This heuristic calculates the no. of differences between the goal state and the current state.
    '''
    h = 0
    goalState = problem.getGoalState()
    for x in state:
        if not x == "HOLDING" and not state["HOLDING"] == x:
            if not state[x] == goalState[x] :
                h += 1
##    print 'blocksInPlacerHeuristic. h =', h 
    return h

def goalStateDiffrencesHeuristic(state, problem):
    '''
    This heuristic calculates the no. of differences between the goal state and the current state.
    '''
    h = 0
    goalState = problem.getGoalState()
    for x in state:
		if not x == "HOLDING" and not state["HOLDING"] == x:
			for y in state[x]:
				if not state[x][y] == goalState[x][y]:
					h += 1
		else:
			if not state[x] == goalState[x]:
				h += 1
##    print 'anotherHeuristic. h =', h 
    return h

    
def pickingNeeded(state, pickingSet, curBlock):
    retVal = 0
    while (not curBlock in pickingSet) and (not curBlock is None):
        pickingSet.add(curBlock)
        retVal +=1
        curBlock = state[curBlock]["under"]
    return retVal

def pickingNeededHeuristic(state, problem):
    '''
    This heuristic calculates the no. of differences between the goal state and the current state.
    '''
    h = 0
    pickingSet = set([])
    goalState = problem.getGoalState()
    for x in state:
        if not x == "HOLDING" and not state["HOLDING"] == x:
            if  not x in pickingSet:
                if not state[x]["on"] == goalState[x]["on"]:
                    h += pickingNeeded(state, pickingSet, x)

    h= 2*h
    if not state["HOLDING"] is None:
        h += 1 
    return h
    
    
def getStandingOn(state, block):
    retVal = set([])
    curBlock = state[block]["on"]
    #print curBlock
    while (not curBlock == "TABLE"):
        retVal.add(curBlock)
        curBlock = state[curBlock]["on"]
    return retVal
   
def pickingTwiceNeeded(problem, state, block):
    nowStandingOnState= getStandingOn(state, block)
    gsStandingOnState= getStandingOn(problem.getGoalState(), block)
    if len(nowStandingOnState.intersection(gsStandingOnState)) > 0:
        return True
    return False
    

def improvedPickingNeededHeuristic(state, problem):
    '''
    This heuristic calculates the no. of differences between the goal state and the current state.
    '''
    h = 0
    pickingSet = set([])
    goalState = problem.getGoalState()
    for x in state:
        if not x == "HOLDING" and not state["HOLDING"] == x:
            if  not x in pickingSet:
                if not state[x]["on"] == goalState[x]["on"]:
                    h += pickingNeeded(state, pickingSet, x)

    h= 2*h
    if not state["HOLDING"] is None:
        h += 1 
    
    pickTwiceSet = set([])
    for y in pickingSet:
        if pickingTwiceNeeded(problem, state, y):
            pickTwiceSet.add(y)
            h +=2
    return h
    
def blockHaveMutualPrevention (problem, curState, goalState, curCheckedForLockSet, block):
    curCheckedForLockSet = set([]) 
    while (True):
        curCheckedForLockSet.add(block)
        if goalState[block]["on"] == "TABLE":
            return False 

        block = goalState[goalState[block]["on"]]["under"]
        if block in curCheckedForLockSet:
            return True
        if goalState[goalState[block]["on"]]["under"] is None:
            return False            
    
def mutualPreventionPickingNeededHeuristic(state, problem):
    '''
    This heuristic calculates the no. of differences between the goal state and the current state.
    '''
    h = 0
    pickingSet = set([])
    goalState = problem.getGoalState()
    for x in state:
        if not x == "HOLDING" and not state["HOLDING"] == x:
            if  not x in pickingSet:
                if not state[x]["on"] == goalState[x]["on"]:
                    h += pickingNeeded(state, pickingSet, x)

    h= 2*h
    if not state["HOLDING"] is None:
        h += 1 
    
    checkedForLockSet = set([]) 
    curCheckedForLockSet = set([])
    #print state
    #print pickingSet
    for z in pickingSet:
        if z not in checkedForLockSet:
            if blockHaveMutualPrevention(problem, state, goalState, curCheckedForLockSet, z):
                #print curCheckedForLockSet
                checkedForLockSet= checkedForLockSet | curCheckedForLockSet
                #print checkedForLockSet
                h +=2
    return h

def mutualPreventionImprovedPickingNeededHeuristic(state, problem):
    '''
    This heuristic calculates the no. of differences between the goal state and the current state.
    '''
    h = 0
    pickingSet = set([])
    goalState = problem.getGoalState()
    for x in state:
        if not x == "HOLDING" and not state["HOLDING"] == x:
            if  not x in pickingSet:
                if not state[x]["on"] == goalState[x]["on"]:
                    h += pickingNeeded(state, pickingSet, x)

    h= 2*h
    if not state["HOLDING"] is None:
        h += 1 
    
    pickTwiceSet = set([])
    #print pickingSet
    #print state
    for y in pickingSet:
        if pickingTwiceNeeded(problem, state, y):
            pickTwiceSet.add(y)
            h +=2
    
    checkedForLockSet = set([]) 
    curCheckedForLockSet = set([])    
    for z in pickingSet:
        if z not in checkedForLockSet:
            if blockHaveMutualPrevention(problem, state, goalState, curCheckedForLockSet, z):
                checkedForLockSet= checkedForLockSet | curCheckedForLockSet
                if curCheckedForLockSet.isdisjoint(pickTwiceSet):
                    h +=2
    return h
    
def simulateAnnealing(problem,valHeuristic=goalStateDiffrencesHeuristic):
    temp_start = 10000
    temp = temp_start
    temp_end = 10
    coolingFactor = 0.4
    curState = problem.getStartState()
    curNode = (problem.getStartState(), None, 0, None)#state, action to reach, incremental cost, parent node
    while temp > temp_end:
        successors = problem.getSuccessors(curNode[0])
        randSuccessor =  sample(successors, 1)[0]

        successorNode = (randSuccessor[0], randSuccessor[1], curNode[2]+randSuccessor[2], curNode)
        ##print "rand: " , randSuccessor[0], "\n"
        ##print "cur: " , curState[0], "\n"
        difference = valHeuristic(randSuccessor[0], problem) - valHeuristic(curNode[0], problem)
        if difference > 0:
            curState = randSuccessor
            curNode = successorNode
        else:
            prob = exp(-difference / temp)
            if prob > uniform(0,1):
                curState = randSuccessor
                curNode = successorNode
        temp = temp * coolingFactor
    return getStatePathFromNode(curNode, problem)
    
    

def test(name, ws, gs, method, heuristic=None):
    print name
    s = BlocksWorldSolver()
    s.setStartState(ws)
    s.setGoalState(gs)

    sol = s.solve(method, heuristic)

    if sol == None:
        print 'node expanded: ' , s.getNodesExpandedNum()
        print "there is no solution to this problem"
    else:
        print 'Solultion length: ', len(sol)
        print 'node expanded: ' , s.getNodesExpandedNum()
        print 'Solution:\n', sol
		
def runMain():

    ## Test picHeuristic
    name = "\n=== Running Test 8 - A* with pickingNeededHeuristic ==="
    ws = {"A": {"on": "TABLE", "under": "B"}, "B": {"on": "A", "under": "C"}, "C": {"on": "B", "under": "D"}, "D": {"on": "C", "under": "E"}, "E": {"on": "D", "under": None},"HOLDING": None}
    gs = {"A": {"on": "B", "under": None}, "B": {"on": "C", "under": "A"}, "C": {"on": "D", "under": "B"}, "D": {"on": "E", "under": "C"}, "E": {"on": "TABLE", "under": "D"},"HOLDING": None}
    test(name, ws, gs, "aStar", heuristic=pickingNeededHeuristic)
    
    ## Test picHeuristic
    name = "\n=== Running Test 9 - A* with goalStateDiffrencesHeuristic ==="
    ws = {"A": {"on": "TABLE", "under": "B"}, "B": {"on": "A", "under": "C"}, "C": {"on": "B", "under": "D"}, "D": {"on": "C", "under": "E"}, "E": {"on": "D", "under": None},"HOLDING": None}
    gs = {"A": {"on": "B", "under": None}, "B": {"on": "C", "under": "A"}, "C": {"on": "D", "under": "B"}, "D": {"on": "E", "under": "C"}, "E": {"on": "TABLE", "under": "D"},"HOLDING": None}
    test(name, ws, gs, "aStar", heuristic=goalStateDiffrencesHeuristic)
    
    
    ## Test improvedPickingNeededHeuristic
    name = "\n=== Running Test 10 - A* with improvedPickingNeededHeuristic ==="
    ws = {"A": {"on": "TABLE", "under": "B"}, "B": {"on": "A", "under": "C"}, "C": {"on": "B", "under": "D"}, "D": {"on": "C", "under": "E"}, "E": {"on": "D", "under": None},"HOLDING": None}
    gs = {"A": {"on": "B", "under": None}, "B": {"on": "C", "under": "A"}, "C": {"on": "D", "under": "B"}, "D": {"on": "E", "under": "C"}, "E": {"on": "TABLE", "under": "D"},"HOLDING": None}
    test(name, ws, gs, "aStar", heuristic=improvedPickingNeededHeuristic)
    
    
    ## Test simulateAnnealing
    name = "\n=== Running Test 10 - A* with simulateAnnealing ==="
    ws = {"A": {"on": "TABLE", "under": "B"}, "B": {"on": "A", "under": "C"}, "C": {"on": "B", "under": "D"}, "D": {"on": "C", "under": "E"}, "E": {"on": "D", "under": None},"HOLDING": None}
    gs = {"A": {"on": "B", "under": None}, "B": {"on": "C", "under": "A"}, "C": {"on": "D", "under": "B"}, "D": {"on": "E", "under": "C"}, "E": {"on": "TABLE", "under": "D"},"HOLDING": None}
    test(name, ws, gs, "SA")
    
    ## Test mutualPreventionImprovedPickingNeededHeuristic
    name = "\n=== Running Test 10 - A* with mutualPreventionImprovedPickingNeededHeuristic ==="
    ws = {"A": {"on": "TABLE", "under": "B"}, "B": {"on": "A", "under": "C"}, "C": {"on": "B", "under": "D"}, "D": {"on": "C", "under": "E"}, "E": {"on": "D", "under": None},"HOLDING": None}
    gs = {"A": {"on": "B", "under": None}, "B": {"on": "C", "under": "A"}, "C": {"on": "D", "under": "B"}, "D": {"on": "E", "under": "C"}, "E": {"on": "TABLE", "under": "D"},"HOLDING": None}
    test(name, ws, gs, "aStar", heuristic=mutualPreventionImprovedPickingNeededHeuristic)

    ## Test mutualPreventionImprovedPickingNeededHeuristic
    name = "\n=== Running Test 11 - A* with mutualPreventionImprovedPickingNeededHeuristic ==="
    ws = {"A": {"on": "C", "under": None}, "B": {"on": "D", "under": None}, "C": {"on": "TABLE", "under": "A"}, "D": {"on": "TABLE", "under": "B"},"HOLDING": None}
    gs = {"A": {"on": "D", "under": None}, "B": {"on": "C", "under": None}, "C": {"on": "TABLE", "under": "B"}, "D": {"on": "TABLE", "under": "A"},"HOLDING": None}
    test(name, ws, gs, "aStar", heuristic=mutualPreventionImprovedPickingNeededHeuristic)
    
    ## Test mutualPreventionPickingNeededHeuristic
    name = "\n=== Running Test 12 - A* with mutualPreventionPickingNeededHeuristic ==="
    ws = {"A": {"on": "C", "under": None}, "B": {"on": "D", "under": None}, "C": {"on": "TABLE", "under": "A"}, "D": {"on": "TABLE", "under": "B"},"HOLDING": None}
    gs = {"A": {"on": "D", "under": None}, "B": {"on": "C", "under": None}, "C": {"on": "TABLE", "under": "B"}, "D": {"on": "TABLE", "under": "A"},"HOLDING": None}
    test(name, ws, gs, "aStar", heuristic=mutualPreventionPickingNeededHeuristic)

def multipleTests():
    h1 = blocksInPlacerHeuristic
    h2 = goalStateDiffrencesHeuristic
    h3 = pickingNeededHeuristic
    h4 = improvedPickingNeededHeuristic
    h5 = mutualPreventionPickingNeededHeuristic
    h6 = mutualPreventionImprovedPickingNeededHeuristic

    table = PrettyTable(['Heuristic','No. of blocks','Table Size','Average Nodes Expanded','Average Time Taken'], sortby='Heuristic')
    table.align['Heuristic'] = '1'

    data = {}
    data['1'] = {}
    data['2'] = {}
    data['3'] = {}
    data['4'] = {}
    data['5'] = {}
    data['6'] = {}

    i = MIN_BLOCKS_TO_TEST
    while i<=MAX_BLOCKS_TO_TEST:
        h1Nodes, h1Time = 0, 0
        h2Nodes, h2Time = 0, 0
        h3Nodes, h3Time = 0, 0
        h4Nodes, h4Time = 0, 0
        h5Nodes, h5Time = 0, 0
        h6Nodes, h6Time = 0, 0

        for j in range(NO_OF_TESTS):
            n = i #no of blocks
            ts = i #table size
            ws, gs = createRandomProblem(n,ts)
            # print 'ws:', ws
            # print 'gs:', gs
            # print ''
            # print 'No of blocks:', n
            # print 'Table size:', ts
            # print ''

            sol, nodesExpanded, timeTaken = singleTest(ws,gs,'aStar',heuristic=h1,tableSpace=ts)
            h1Nodes += nodesExpanded
            h1Time += timeTaken

            sol, nodesExpanded, timeTaken = singleTest(ws,gs,'aStar',heuristic=h2,tableSpace=ts)
            h2Nodes += nodesExpanded
            h2Time += timeTaken

            sol, nodesExpanded, timeTaken = singleTest(ws,gs,'aStar',heuristic=h3,tableSpace=ts)
            h3Nodes += nodesExpanded
            h3Time += timeTaken

            sol, nodesExpanded, timeTaken = singleTest(ws,gs,'aStar',heuristic=h4,tableSpace=ts)
            h4Nodes += nodesExpanded
            h4Time += timeTaken

            sol, nodesExpanded, timeTaken = singleTest(ws,gs,'aStar',heuristic=h5,tableSpace=ts)
            h5Nodes += nodesExpanded
            h5Time += timeTaken

            sol, nodesExpanded, timeTaken = singleTest(ws,gs,'aStar',heuristic=h6,tableSpace=ts)
            h6Nodes += nodesExpanded
            h6Time += timeTaken

        table.add_row(['1', i, ts, h1Nodes/NO_OF_TESTS, h1Time/NO_OF_TESTS])
        table.add_row(['2', i, ts, h2Nodes/NO_OF_TESTS, h2Time/NO_OF_TESTS])
        table.add_row(['3', i, ts, h3Nodes/NO_OF_TESTS, h3Time/NO_OF_TESTS])
        table.add_row(['4', i, ts, h4Nodes/NO_OF_TESTS, h4Time/NO_OF_TESTS])
        table.add_row(['5', i, ts, h5Nodes/NO_OF_TESTS, h5Time/NO_OF_TESTS])
        table.add_row(['6', i, ts, h6Nodes/NO_OF_TESTS, h6Time/NO_OF_TESTS])

        i += INCREMENT

    print table


    # print 'h5. average nodes expanded:', h5NodesAverage, '. time average:', h5TimeAverage
    # print 'h6. average nodes expanded:', h6NodesAverage, '. time average:', h6TimeAverage

def createRandomProblem(noOfBlocks, tableSize):
    ws = createRandomState(noOfBlocks,tableSize)
    gs = createRandomState(noOfBlocks,tableSize)
    return ws, gs

def createRandomState(noOfBlocks, tableSize):
    blockNames = [str(i+1) for i in range(noOfBlocks)]

    shuffle(blockNames)

    blocks = {}

    noOfBlocksOnTable = 0

    uncoveredBlocks = []
    uncoveredBlocks.append('TABLE')

    for i in blockNames:
        placeOn = choice(uncoveredBlocks)
        newBlock = {}
        newBlock['on'] = placeOn
        newBlock['under'] = None
        blocks[i] = newBlock
        uncoveredBlocks.append(i)

        if placeOn == 'TABLE':
            noOfBlocksOnTable += 1
            if noOfBlocksOnTable == tableSize:
                uncoveredBlocks.remove('TABLE')
        else:
            blocks[placeOn]['under'] = i
            uncoveredBlocks.remove(placeOn)
    blocks['HOLDING'] = None
    return blocks

def singleTest(ws, gs, method, heuristic=None, tableSpace='infinite'):
    s = BlocksWorldSolver()
    s.setStartState(ws)
    s.setGoalState(gs)
    s.setTableSpace(tableSpace)

    from time import time
    startTime = time()
    sol = s.solve(method, heuristic)
    endTime = time()

    timeTaken = endTime - startTime

    return sol, s.getNodesExpandedNum(), timeTaken


if __name__ == "__main__" :
    # runMain()
    multipleTests()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
