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
            
    def solve(self, methodName):
        self.method[methodName]()            

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

    def depthOrBreadthFirstSearch (problem, container):
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
      print "the algorithm didn't find a solution"

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

    
    def nullHeuristic():
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
      print "Error: no path from start state to goal state"
            
    def getSuccessors(state):
        if state[ARMHOLDING] == "NONE":
            return 0                         
        else:
            return 0
                    
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

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
