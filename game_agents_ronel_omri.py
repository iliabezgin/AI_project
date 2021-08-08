# from agents import Agent
from action import *
from game_state import Game
import abc
import numpy as np
import copy


class Agent(object):

    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state: Game):
        '''
        Returns action for the current game state
        :param game_state:
        '''
        return

    def stop_running(self):
        pass

    @abc.abstractmethod
    def get_type(self):
        return


def evaluation_function_by_score(current_game_state: Game):
    return current_game_state.get_points()


def get_agent_legal_action():
    pass


def get_opponent_legal_action():
    pass


# def get_legal_actions(agent_ind):
#     if agent_ind == 0:
#         return get_agent_legal_action()
#     elif agent_ind == 1:
#         return get_enmy_legal_action()
#     else:
#         raise Exception('illegal agent')
class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function=evaluation_function_by_score, depth=1):
        self.evaluation_function = evaluation_function
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):

    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """

        player = 0
        actions = []
        for block in game_state.current_blocks:
            print("aaaa" + str(len(game_state.get_legal_actions(block))), end=" ")
            actions += game_state.get_legal_actions(block)
        # if len(actions) == 0:
        #     return
        # get oll succurors. That is, all the moves the computer can make
        # print(len(actions), end=" ")
        # print(len(game_state.current_blocks))
        successors = np.array(
            [self.Minimax(game_state.generate_successor(action, True), 0, False) for action in actions])
        # return the max
        return actions[np.argmax(successors)]

    def get_type(self):
        return "MinimaxAgent"

    def Minimax(self, node: Game, depth, isMaxNode):
        """
        :param node: game state
        :param depth: How deep to look in tree
        :param isMaxNode: true if the agent is max else false
        :return: the best move for maxPlayer
        """

        # if we got to depth that we chose in constrctor
        if depth == self.depth:
            return self.evaluation_function(node)
        elif len(node.current_blocks) != 0:
            actions = []
            for block in node.current_blocks:
                actions += node.get_legal_actions(block)

            max = np.max(
                np.array([self.Minimax(node.generate_successor_2(s,len(node.current_blocks)), depth, False) for s in actions])) if len(
                actions) else 0
            # return the best move that maximiz the point
            return max
        else:
            blocks = node.blocks.block_list
            list_of_combinations = make_sub_group(blocks, 3)
            print(f"comb = {len(list_of_combinations)}")
            # return the best move that mimaiz
            return np.min(np.array(
                [self.Minimax(generate_successor_for_minAgent(node, list(blocks_3)), depth + 1, True) for blocks_3 in
                 list_of_combinations]))


def make_sub_group(_list, size):
    from itertools import combinations_with_replacement, combinations
    return list(combinations(_list, size))
    # return list(combinations_with_replacement(s, n))


def generate_successor_for_minAgent(node: Game, blockss: list):
    successor = Game(None)
    successor.board = copy.deepcopy(node.board)
    successor.current_blocks = blockss
    return successor


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_type(self):
        return "AlphaBetaAgent"

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        actions = []
        for block in game_state.current_blocks:
            actions += game_state.get_legal_actions(block)
        # Initializes with the maximum values for alpha, beta
        alpha, beta = -float('inf'), float('inf')
        # print(11111111111111111111,len(actions),len(game_state.current_blocks))
        best = actions[0]
        for action in actions:
            possible_move = game_state.generate_successor(action, True)
            n_alpha = self.AlphaBetaPruning(possible_move, depth=0, alpha=alpha, beta=beta, maxPlayer=False)
            if n_alpha > alpha:
                best = action
                alpha = n_alpha
            if alpha >= beta:
                break
        print(1111111111111)
        return best

    def AlphaBetaPruning(self, node:Game, depth:int, alpha, beta, maxPlayer):
        """
        :param node: the game state
        :param depth: How deep to look in tree
        :param alpha: the value of alpha plyer
        :param beta: the value of beta plyer
        :param maxPlayer: true if plyer is maxPlayer
        :return: alpha if case of maxPlayer is true and beta other
        """

        if depth == self.depth:
            return self.evaluation_function(node)
        if len(node.current_blocks) != 0:
            # get oll legal action for the agent
            actions = []
            # if depthe ==1:
            #     print(len(node.current_blocks),11222)
            for block in node.current_blocks:
                # print(node.current_blocks)
                actions += node.get_legal_actions(block)
            for action in actions:
                alpha = max(alpha, self.AlphaBetaPruning(node.generate_successor_2(action, len(node.current_blocks)), depth, alpha, beta, False))
                if alpha >= beta:
                    break
            return alpha
        else:
            # get oll legal action for the coputer
            blocks = node.blocks.block_list
            list_of_combinations = make_sub_group(blocks, 3)
            for combination in list_of_combinations:
                # get the beat move that mzimiz the score of maxPlyer
                v = [Block(node.blocks.block_list.index(s), node.blocks, None, False) for s in combination]
                beta = min(beta,
                           self.AlphaBetaPruning(generate_successor_for_minAgent(node, v), depth + 1, alpha, beta, True))
                if alpha >= beta:
                    break
            return beta

class LocalSearchAgent(MultiAgentSearchAgent):

    def get_type(self):
        return "LocalSearchAgent"

    def local_search(self):
        actions = []
        if (len( game_state.current_blocks) == 3):
            for block in game_state.current_blocks:
                actions += game_state.get_legal_actions(block)
            action = random.choise(actions)
            apply_action(action)
        while(len( game_state.current_blocks) != 0 ):
            actions = []
            for block in game_state.current_blocks:
                actions += game_state.get_legal_actions(block)
            max_act, max_val = 0
            for action in actions:
                success = generate_successor_2(action, len(game_state.current_blocks))
                if success.get_points() > max_val:
                    max_act = action
                    max_val = success.get_points()
            apply_action(max_act)