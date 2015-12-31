# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        #['West', 'Stop', 'East', 'North', 'South']
        #print legalMoves
        #print legalMoves[chosenIndex]
        "Add more of your code here if you want to"
        # TODO: handle if repetitive walk forward and back 
        
        return legalMoves[chosenIndex]

    def calculateScoreBasedOnGhosts(self, ghostStates, pacmanPos):
        score = 0
        for ghost in ghostStates:
            ghostScaredTime = ghost.scaredTimer
            #print "ghostScaredTime", ghostScaredTime
            distanceToGhost = util.manhattanDistance(pacmanPos, ghost.getPosition())
            #print "distanceToGhost", distanceToGhost
            if ghostScaredTime <= 0:
                score -= pow(max(6 - distanceToGhost, 0), 2)
                #score -= pow(7 - distanceToGhost, 2)
            else:
                #print "!!"
                score += pow(max(7 - distanceToGhost, 0), 2)
            #print "score", score
        return score

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #Note: As features, try the reciprocal of important values (such as distance to food) rather than just the values themselves.
        newFood = successorGameState.getFood()
        distanceToFood = map(lambda x: 1.0 / manhattanDistance(x, newPos), newFood.asList())
        #print "dist to food", distanceToFood   
        scoreBasedOnFood = max(distanceToFood + [0])
        #print "dist to food + [0]", (distanceToFood + [0])
        #print "score on food ", scoreBasedOnFood
        
        scoreBasedOnGhosts = self.calculateScoreBasedOnGhosts(newGhostStates, newPos)
        return scoreBasedOnFood + scoreBasedOnGhosts + successorGameState.getScore()


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
            
          Directions.STOP:
            The stop direction, which is always legal
          
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        total_agents = gameState.getNumAgents()

        def evaluateMax(gamestate, current_depth):
            actions_for_pacman = gamestate.getLegalActions(0)

            if current_depth > self.depth or gamestate.isWin() or not actions_for_pacman:
                return self.evaluationFunction(gamestate), None

            successor_cost = []
            for action in actions_for_pacman:
                successor = gamestate.generateSuccessor(0, action)
                successor_cost.append((evaluateMin(successor, 1, current_depth), action))
            #print "============"
            #print successor_cost
            #print max(successor_cost)
            return max(successor_cost)

        def evaluateMin(gamestate, agent_index, current_depth):
            actions_for_ghost = gamestate.getLegalActions(agent_index)
            #print "agent index 2 test: " , gamestate.getLegalActions(2)
            if not actions_for_ghost or gamestate.isLose():
                return self.evaluationFunction(gamestate), None

            successors = [gamestate.generateSuccessor(agent_index, action) for action in actions_for_ghost]
            
            #print "----------------------"
            #print agent_index
            #print successors
            
            if agent_index == total_agents - 1:
                successor_cost = []
                for successor in successors:
                    successor_cost.append(evaluateMax(successor, current_depth + 1))
            else:
                successor_cost = []
                for successor in successors:
                    successor_cost.append(evaluateMin(successor, agent_index + 1, current_depth))

            return min(successor_cost)


        return evaluateMax(gameState, 1)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        total_agents = gameState.getNumAgents()
        
        #similar to minimax
        def evaluateMax(gamestate, current_depth, alpha, beta):
            actions_for_pacman = gamestate.getLegalActions(0)

            if current_depth > self.depth or gamestate.isWin() or not actions_for_pacman:
                return self.evaluationFunction(gamestate), Directions.STOP

            #initial value
            value = float('-inf')
            bestAction = Directions.STOP
            for action in actions_for_pacman:
                successor = gamestate.generateSuccessor(0, action)
                cost = evaluateMin(successor, 1, current_depth, alpha, beta)[0]
                
                #print "============="
                #print calculateMin(successor, 1, current_depth, alpha, beta)
                #print cost
                
                if cost > value:
                    value = cost
                    bestAction = action
                if value > beta:
                    return value, bestAction
                alpha = max(alpha, value)

            return value, bestAction

        def evaluateMin(gamestate, agent_index, current_depth, alpha, beta):
            actions_for_ghost = gamestate.getLegalActions(agent_index)
            if not actions_for_ghost or gamestate.isLose():
                return self.evaluationFunction(gamestate), Directions.STOP

            #initial value
            value = float('inf')
            bestAction = Directions.STOP
            isPacman = agent_index == total_agents - 1
            for action in actions_for_ghost:
                successor = gamestate.generateSuccessor(agent_index, action)
                if isPacman:
                    cost = evaluateMax(successor, current_depth + 1, alpha, beta)[0]
                else:
                    cost = evaluateMin(successor, agent_index + 1, current_depth, alpha, beta)[0]

                if cost < value:
                    value = cost
                    bestAction = action
                if value < alpha:
                    return value, bestAction
                beta = min(beta, value)

            return value, bestAction


        initAlpha = float('-inf')
        initBeta = float('inf')
        #a = calculateMax(gameState, 1, initAlpha, initBeta)[1]
        #print "!!!!!!!!!!!"
        #print a
        return evaluateMax(gameState, 1, initAlpha, initBeta)[1]


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
        total_agents = gameState.getNumAgents()

        def evaluateMax(gamestate, current_depth):
            actions_for_pacman = gamestate.getLegalActions(0)

            if current_depth > self.depth or gamestate.isWin() or not actions_for_pacman:
                return self.evaluationFunction(gamestate), None

            successors_score = []
            for action in actions_for_pacman:
                successor = gamestate.generateSuccessor(0, action)
                successors_score.append((evaluateMin(successor, 1, current_depth)[0], action))

            return max(successors_score)

        def evaluateMin(gamestate, agent_index, current_depth):
            actions_for_ghost = gamestate.getLegalActions(agent_index)
            if not actions_for_ghost or gamestate.isLose():
                return self.evaluationFunction(gamestate), None

            successors = [gamestate.generateSuccessor(agent_index, action) for action in actions_for_ghost]

            successors_score = []
            isPacman = agent_index == total_agents - 1
            for successor in successors:
                if isPacman:
                    successors_score.append(evaluateMax(successor, current_depth + 1))
                else:
                    successors_score.append(evaluateMin(successor, agent_index + 1, current_depth))

            averageScore = sum(map(lambda x: float(x[0]) / len(successors_score), successors_score))
            return averageScore, None

        return evaluateMax(gameState, 1)[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    position = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    foodStates = currentGameState.getFood()
    capsuleStates = currentGameState.getCapsules()
    #print capsuleStates
    
    distanceToCapsule = map(lambda x: 1.0 / manhattanDistance(x, position), capsuleStates)
    distanceToFood = map(lambda x: 1.0 / manhattanDistance(x, position), foodStates.asList())
    scoreBasedOnFood = max(distanceToFood + [0])
    scoreBasedOnCapsule = max(distanceToCapsule + [0])
    #print scoreBasedOnCapsule
    scoreBasedOnGhosts = evaluateScoreBasedOnGhostsStates(ghostStates, position)
    #print "scoreBasedOnCapsule", scoreBasedOnCapsule
    #print "scoreBasedOnFood", scoreBasedOnFood
    #print "scoreBasedOnGhosts", scoreBasedOnGhosts
    #print "score", score
    return scoreBasedOnCapsule + 10 * scoreBasedOnFood + 1 * scoreBasedOnGhosts + score
def evaluateScoreBasedOnGhostsStates(ghostStates, pacmanPos):
    score = 0
    for ghost in ghostStates:
        ghostScaredTime = ghost.scaredTimer
        distanceToGhost = util.manhattanDistance(pacmanPos, ghost.getPosition())
        
        if ghostScaredTime <= 0:
            score -= pow(max(6 - distanceToGhost, 0), 2)
        else:
            score += pow(max(7 - distanceToGhost, 0), 2)
    return score


# Abbreviation
better = betterEvaluationFunction


