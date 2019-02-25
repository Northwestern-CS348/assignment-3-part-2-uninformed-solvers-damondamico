
from solver import *
from queue import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.stack = []

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        self.visited[self.currentState] = True
        if self.currentState.state == self.victoryCondition:
            return True
        moves = self.gm.getMovables()
        if len(self.currentState.children) == 0:
            for move in moves:
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                if child not in self.visited.keys():
                    self.visited[child] = False
                child.parent = self.currentState
                self.currentState.children.append(child)
                self.gm.reverseMove(move)
        for i in self.currentState.children[::-1]:
            if self.visited[i] == False:
                self.stack.append(i)
        nextnode = self.stack.pop()
        move = nextnode.requiredMovable
        while self.currentState.nextChildToVisit == len(self.currentState.children):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState == self.currentState.parent
        nextnode.parent.nextChildToVisit += 1
        self.gm.makeMove(move)
        self.currentState = nextnode
        return False

            






class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.q = Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        movables = self.gm.getMovables()
        visited = self.visited
        if self.currentState.state == self.victoryCondition:
            if (self.q != self.q.empty()):
                while not self.q.empty():
                    self.q.get()
            return True
        if (movables):
            for move in movables:
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
                self.currentState.children.append(child)
                child.parent = self.currentState
                self.gm.reverseMove(move)
        for i in self.currentState.children:
            if i not in visited:
                self.q.put(i)
        while not self.q.empty():
            child = self.q.get()
            if child not in visited:
                currstate = self.currentState
                base = []
                branch = []
                while (currstate.requiredMovable):
                    base.append(currstate.requiredMovable)
                    currstate = currstate.parent
                currstate = child
                while currstate.requiredMovable:
                    branch.append(currstate.requiredMovable)
                    currstate = currstate.parent
                branch = reversed(branch)
                for k in base:
                    self.gm.reverseMove(k)
                for j in branch:
                    self.gm.makeMove(j)
                visited[child] = True
                self.currentState = child
                break
        return False