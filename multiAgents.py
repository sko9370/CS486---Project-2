# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # tuple (x,y)
        newPos = successorGameState.getPacmanPosition()
        # list of list with true/false, true where food exists
        newFood = successorGameState.getFood()
        # list of each ghost states, use .getPosition
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodCount = successorGameState.getNumFood()

        #for ghostPos in successorGameState.getGhostPositions():
        #    print("ghostPosition: " + str(ghostPos))

        foodDis = 0
        foodMinList = []
        for food in newFood.asList():
            foodDis += manhattanDistance(food, newPos)
            foodMinList.append(manhattanDistance(food, newPos))
        if len(foodMinList) == 0:
            foodMin = 1
        else:
            foodMin = min(foodMinList)

        ghostDis = 0
        ghostMinList = []
        for ghost in successorGameState.getGhostPositions():
            ghostDis += manhattanDistance(ghost, newPos)
            ghostMinList.append(manhattanDistance(ghost, newPos))
        if len(foodMinList) == 0:
            ghostMin = 1
        else:
            ghostMin = min(ghostMinList)

        if foodDis == 0:
            foodDis = 1
        if newFoodCount == 0:
            newFoodCount = -1
        if ghostDis == 0:
            ghostDis = 1
        if foodMin == 0:
            foodMin = 1
        if ghostMin == 0:
            ghostMin = 1

        if sum(newScaredTimes) > 3:
            score = 1/foodMin - newFoodCount + 1/ghostMin
        else:
            score = 1/foodMin - newFoodCount - 2/ghostMin - 1/ghostDis
        #print(score)
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        import sys

        maxDepth = self.depth
        numAgents = gameState.getNumAgents()

        def maxValue(gameState, agent, depth):
            #print("from max with agent: " + str(agent))
            v = -sys.maxsize
            legalActions = gameState.getLegalActions(agent)
            scores = []
            for action in legalActions:
                # terminal state, calculate gameState score
                if gameState.isWin() or gameState.isLose():
                    scores.append(self.evaluationFunction(gameState))
                # non-terminal
                else:
                    scores.append(minValue(gameState.generateSuccessor(agent, action), agent + 1, depth))

            if not scores:
                return self.evaluationFunction(gameState)
            else:
                bestScore = max(scores)
                return bestScore

        def minValue(gameState, agent, depth):
            #print("from min with agent: " + str(agent))
            v = sys.maxsize
            legalActions = gameState.getLegalActions(agent)
            scores = []
            for action in legalActions:
                # terminal state, calculate gameState score
                if gameState.isWin() or gameState.isLose():
                    #print("terminal")
                    scores.append(self.evaluationFunction(gameState))
                # non-terminal
                elif agent < numAgents - 1:
                    #print("not last agent")
                    scores.append(minValue(gameState.generateSuccessor(agent, action), agent + 1, depth))
                else:
                    if depth == maxDepth:
                        #print("last agent at max depth")
                        scores.append(self.evaluationFunction(gameState))
                    else:
                        #print("last agent but not at max depth")
                        scores.append(maxValue(gameState.generateSuccessor(agent, action), 0, depth + 1))

            if not scores:
                return self.evaluationFunction(gameState)
            else:
                worstScore = min(scores)
                return worstScore

        #print("\nnumber of agents: " + str(numAgents))
        #print("\nmax depth: " + str(maxDepth))
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions
        scores = [minValue(gameState.generateSuccessor(0, action), 1, 1) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
