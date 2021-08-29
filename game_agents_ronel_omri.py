# from agents import Agent
import random

from action import *
from game_state import Game
import abc
import numpy as np
import copy

# On some subgroups the beta agent tester
NUM_OF_BETA_AGENT = 10


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


from agents import AStarAgent
from main import test_board_heuristic, test_board_action_heuristic, test_block_heuristic


def evaluation_function_by_score(current_game_state, list_of_act):
    n2 = 0
    for act in list_of_act:
        n2 += 2.5 * surface_heuristic(current_game_state, act)
        n2 += 0.5 * row_col_completeness_heuristic(current_game_state, act)
        current_game_state = current_game_state.generate_successor(act, True)

    n1 = free_space_heuristic(
        current_game_state) + 50 * one_square_hole(
        current_game_state) + empty_large_square_heuristic(
        current_game_state)
    return n1 + n2


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
        self.actions = []
        self.helper = AStarAgent(test_board_heuristic, test_board_action_heuristic)
        # self.helper =  LocalSearchAgent(test_board_heuristic, test_board_action_heuristic, test_block_heuristic)
        self._threes_lists = None

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):

    def get_action(self, game_state: Game):
        actions = []
        for block in game_state.current_blocks:
            actions += game_state.get_legal_actions(block)
        successors = np.array(
            [self.Minimax(game_state.generate_successor(action, True), 0, False) for action in actions])
        # return the max
        return actions[np.argmax(successors)]

    def get_type(self):
        return "MinimaxAgent"

    def Minimax(self, node: Game, depth: int, isMaxNode: bool, act_list: list):
        """
        :param node: game state
        :param depth: How deep to look in tree
        :param isMaxNode: true if the agent is max else false
        :return: the best move for maxPlayer
        """

        # if we got to depth that we chose in constrctor
        if depth == self.depth and len(node.current_blocks) == 0:
            return self.evaluation_function(node, act_list)
        elif isMaxNode:
            actions = []
            for block in node.current_blocks:
                actions += node.get_legal_actions(block)

            max = np.max(
                np.array([self.Minimax(node.generate_successor_2(s, len(node.current_blocks)), depth,
                                       len(node.current_blocks) != 0, act_list + s) for s in actions])) if len(
                actions) else 0
            # return the best move that maximiz the point
            return max
        else:
            blocks = node.blocks.block_list
            list_of_combinations = make_sub_group(blocks, 3)
            # return the best move that mimaiz
            return np.min(np.array(
                [self.Minimax(generate_successor_for_minAgent(node, list(blocks_3)), depth + 1, True) for blocks_3 in
                 list_of_combinations]))


# class AlphaBetaAgent(MultiAgentSearchAgent):
#     """
#     Your minimax agent with alpha-beta pruning (question 3)
#     """
#
#     def get_type(self):
#         return "AlphaBetaAgent"
#
#     def get_action(self, game_state):
#         """
#         Returns the minimax action using self.depth and self.evaluationFunction
#         """
#
#         actions = []
#         for block in game_state.current_blocks:
#             actions += game_state.get_legal_actions(block)
#         # Initializes with the maximum values for alpha, beta
#         alpha, beta = -float('inf'), float('inf')
#         # print(11111111111111111111,len(actions),len(game_state.current_blocks))
#         best = actions[0]
#         for action in actions:
#             possible_move = game_state.generate_successor(action, True)
#             n_alpha = self.AlphaBetaPruning(possible_move, depth=0, alpha=alpha, beta=beta, maxPlayer=False)
#             if n_alpha > alpha:
#                 best = action
#                 alpha = n_alpha
#             if alpha >= beta:
#                 break
#         return best
#
#     def AlphaBetaPruning(self, node: Game, depth: int, alpha, beta, maxPlayer):
#         """
#         :param node: the game state
#         :param depth: How deep to look in tree
#         :param alpha: the value of alpha plyer
#         :param beta: the value of beta plyer
#         :param maxPlayer: true if plyer is maxPlayer
#         :return: alpha if case of maxPlayer is true and beta other
#         """
#
#         if depth == self.depth:
#             return self.evaluation_function(node)
#         if len(node.current_blocks) != 0:
#             # get oll legal action for the agent
#             actions = []
#             for block in node.current_blocks:
#                 # print(node.current_blocks)
#                 actions += node.get_legal_actions(block)
#             for action in actions:
#                 alpha = max(alpha,
#                             self.AlphaBetaPruning(node.generate_successor_2(action, len(node.current_blocks)), depth,
#                                                   alpha, beta, False))
#                 if alpha >= beta:
#                     break
#             return alpha
#         else:
#             # get oll legal action for the coputer
#             blocks = node.blocks.block_list
#             list_of_combinations = make_sub_group(blocks, 3)
#             for combination in list_of_combinations:
#                 # get the beat move that mzimiz the score of maxPlyer
#                 v = [Block(node.blocks.block_list.index(s), node.blocks, None, False) for s in combination]
#                 beta = min(beta,
#                            self.AlphaBetaPruning(generate_successor_for_minAgent(node, v), depth + 1, alpha, beta,
#                                                  True))
#                 if alpha >= beta:
#                     break
#             return beta


########################################################################################################################

from itertools import combinations_with_replacement, combinations

from heusristics_ilia import *


def make_sub_group(_list, size: int):
    """
    :param _list: list to creat sub group
    :param size: size of the sub group
    :return: list of sub group
    """
    return list(combinations_with_replacement(_list, size))


def generate_successor_for_minAgent(node: Game, blocks_list: list):
    """
    Gets a board of the game and puts into it the 3 pieces
    :param node:
    :param blocks_list:
    :return:
    """
    successor = Game(None)
    successor.board = copy.deepcopy(node.board)
    successor.current_blocks = blocks_list
    return successor


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_type(self):
        return "AlphaBetaAgent"

    def get_action(self, game_state: Game):
        if len(self.actions) == 0:
            self.actions = self.get_action_of_alphaBeta(game_state)
        action = self.actions.pop(0)
        for block in game_state.current_blocks:
            if block.block_list_index == action.block.block_list_index:
                action.block = block
                break
        return action

    def get_action_of_alphaBeta(self, game_state: Game):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        actions = []
        for block in game_state.current_blocks:
            actions += game_state.get_legal_actions(block)

        # sort the action by heuristic
        actions.sort(key=lambda x: surface_heuristic(game_state, x))
        # Initializes with the maximum values for alpha, beta
        alpha, beta = -float('inf'), float('inf')
        best = actions[0]
        possible_move = game_state.generate_successor(best, True)
        # Completes the last 2 moves by the helper agent
        complet_best = self.helper.a_star_search(possible_move)

        for action in actions:
            possible_move = game_state.generate_successor(action, True)
            moves = self.helper.a_star_search(possible_move)
            action_list = [action] + moves
            n_alpha = self.AlphaBetaPruning(possible_move, 0, alpha, beta, False, action_list) - possible_move.points
            if n_alpha > alpha:
                best = action
                complet_best = moves
                alpha = n_alpha
            if alpha >= beta:
                break
        best = [best] + complet_best
        self._threes_lists = None
        return best

    def AlphaBetaPruning(self, node: Game, depth: int, alpha: float, beta: float, maxPlayer: bool, list_of_act: list):
        """
        :param node: the game state
        :param depth: How deep to look in tree
        :param alpha: the value of alpha plyer
        :param beta: the value of beta plyer
        :param maxPlayer: true if plyer is maxPlayer
        :return: alpha if case of maxPlayer is true and beta other
        """

        if depth == self.depth:
            return self.evaluation_function(node, list_of_act)
        if maxPlayer:
            # get oll legal action for the agent
            actions = []
            for block in node.current_blocks:
                actions += node.get_legal_actions(block)
            actions.sort(key=lambda x: surface_heuristic(node, x))
            for action in actions:
                possible_move = node.generate_successor(action, True)
                new_s = self.helper.a_star_search(possible_move)
                act_list = [action] + new_s
                alpha = max(alpha, self.AlphaBetaPruning(
                    possible_move, depth,
                    alpha, beta, False, list_of_act + act_list))
                if alpha >= beta:
                    break
            return alpha
        else:
            # get oll legal action for the computer
            list_of_combinations = self._get_threes_list(node)
            for combination in list_of_combinations:
                # creat the list of block for beat agent
                block_lst = [Block(node.blocks.block_list.index(comb), node.blocks, None,
                                   False) for comb in combination]
                successor = generate_successor_for_minAgent(node, block_lst)
                # Completes the moves by the helper agent
                good_act = self.helper.a_star_search(successor)
                temp_list = list_of_act + good_act
                temp = self.AlphaBetaPruning(successor, depth + 1, alpha, beta, True, temp_list)
                prob = get_prob(block_lst)
                beta = min(beta, temp)
                # beta = min(beta, temp*prob)
                if alpha >= beta:
                    break
            return beta

    def _get_threes_list(self, node: Game):
        """
        :param node:
        :return: 10 threes of block
        """
        if self._threes_lists:
            return self._threes_lists
        else:
            blocks = node.blocks.block_list
            list_of_combinations = make_sub_group(blocks, 3)
            self._threes_lists = random.choices(list_of_combinations, k=10)
            b = BLOCKS()
            comb_lst = []
            while len(comb_lst) != NUM_OF_BETA_AGENT:
                block_3 = np.random.choice(blocks, size=3, p=b.probabilities)
                if block_3 not in comb_lst: comb_lst.append(block_3)
            # for i in range(NUM_OF_BETA_AGENT):
            #     comb_lst.append(np.random.choice(blocks, size=3, p=b.probabilities))
            return self._threes_lists


def get_prob(block_list):
    """
    :param block_list: list of block
    :return: the Probability that these parts came out together
    """
    prob = 1
    b = BLOCKS()
    for block in block_list:
        prob *= b.probabilities[block.block_list_index]
    return prob
