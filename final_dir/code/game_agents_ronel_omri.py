import random

from action import *
from game_state import Game
import abc
import numpy as np
import copy
from agents import GreedyBFSTripleAgent
from main import test_board_heuristic, test_board_action_heuristic
from itertools import combinations_with_replacement
from heusristics_ilia import *

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
    :param blocks_list: 3 pieces to puts in the board
    :return:
    """
    successor = Game(None)
    successor.board = copy.deepcopy(node.board)
    successor.current_blocks = blocks_list
    return successor

def evaluation_function_by_score(current_game_state, list_of_act):
    """
    :param current_game_state: board
    :param list_of_act: List of actions to do on the board
    :return: score
    """
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
    multi-agent searchers.
    """

    def __init__(self, evaluation_function=evaluation_function_by_score, depth=0):
        self.evaluation_function = evaluation_function
        self.depth = depth
        self.actions = []
        self.helper = GreedyBFSTripleAgent(test_board_heuristic, test_board_action_heuristic)
        self._threes_lists = None
        self._node = None

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    @staticmethod
    def __helper_generate_successor(game_state: Game, act_list: list):
        """
        :param game_state: node to be created for it successor
        :param act_list: Actions we did on the board
        :return: List of [[board,act_list],...]
        """
        actions = []
        for block in game_state.current_blocks:
            actions += game_state.get_legal_actions(block)
        board = []
        for act in actions:
            board.append([game_state.generate_successor_2(act, len(game_state.current_blocks)), act_list + [act]])
        return board

    @staticmethod
    def generate_successor(game_state: Game):
        """
        :param game_state: node to be created for it successor
        :return: all successor of game_state
        """
        actions_1 = []
        # do the first act on board
        for block in game_state.current_blocks:
            actions_1 += game_state.get_legal_actions(block)
        board_whit_1_act = []
        for first_act in actions_1:
            board_whit_1_act.append(
                [game_state.generate_successor_2(first_act, len(game_state.current_blocks)), [first_act]])
        # do the second act on board
        board_whit_2_act = []
        for board_act in board_whit_1_act:
            board_whit_2_act += MultiAgentSearchAgent.__helper_generate_successor(board_act[0], board_act[1])
        # do the third act on board
        for board_act in board_whit_2_act:
            board_whit_3_act = MultiAgentSearchAgent.__helper_generate_successor(board_act[0], board_act[1])
            for board, act_on_board in board_whit_3_act:
                yield board, act_on_board


####################################################################################################################################

class AlphaBetaAgentV3(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning 
    the alpha agent ran for the maximum 30 boys according to heuristics
    the betat agent ran on 10 random threes
    """

    def get_type(self):
        return "AlphaBetaAgentV3"

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
        self._node = game_state
        actions = []
        func = lambda x: 2.5 * surface_heuristic(game_state, x) + 0.5 * row_col_completeness_heuristic(game_state, x)
        for block in game_state.current_blocks:
            ac = game_state.get_legal_actions(block)
            ac.sort(key=func)
            actions += ac if len(ac) < 10 else ac[:10]

        # Initializes with the maximum values for alpha, beta
        alpha, beta = -float('inf'), float('inf')
        best = actions[0]
        possible_move = game_state.generate_successor(best, True)
        # Completes the last 2 moves by the helper agent
        complet_best = self.helper.greedy_search(possible_move)

        for action in actions:
            possible_move = game_state.generate_successor(action, True)
            moves = self.helper.greedy_search(possible_move)
            for act in moves:
                possible_move = possible_move.generate_successor(act, True)
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
            return self.evaluation_function(self._node, list_of_act)
        if maxPlayer:
            # get oll legal action for the agent
            actions = []

            func = lambda x: 2.5 * surface_heuristic(game_state, x) + 0.5 * row_col_completeness_heuristic(game_state, x)
            for block in node.current_blocks:
                ac = node.get_legal_actions(block)
                ac.sort(key=func)
                actions += ac if len(ac) < 10 else ac[:10]

            for action in actions:
                possible_move = node.generate_successor(action, True)
                new_s = self.helper.greedy_search(possible_move)
                for act in new_s:
                    possible_move = possible_move.generate_successor(act, True)
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
                good_act = self.helper.greedy_search(successor) if depth + 1 == self.depth else []
                for act in good_act:
                    successor = successor.generate_successor(act, True)
                temp_list = list_of_act + good_act
                temp = self.AlphaBetaPruning(successor, depth + 1, alpha, beta, True, temp_list)
                beta = min(beta, temp)
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
            b = BLOCKS()
            comb_lst = []
            while len(comb_lst) != NUM_OF_BETA_AGENT:
                block_3 = np.random.choice(blocks, size=3, p=b.probabilities)
                block_3 = list(block_3)
                if block_3 not in comb_lst: comb_lst.append(block_3)
            self._threes_lists = comb_lst
            return self._threes_lists


########################################################################################################################


class AlphaBetaAgentV2(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning
    """

    def get_type(self):
        return "AlphaBetaAgentV2"

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
        self._node = game_state
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
        complet_best = self.helper.greedy_search(possible_move)
        for act in complet_best:
            possible_move = possible_move.generate_successor(act, True)
        for action in actions:
            possible_move = game_state.generate_successor(action, True)
            moves = self.helper.greedy_search(possible_move)
            action_list = [action] + moves
            for act in moves:
                possible_move = possible_move.generate_successor(act, True)
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
            return self.evaluation_function(self._node, list_of_act)
        if maxPlayer:
            # get oll legal action for the agent
            actions = []
            for block in node.current_blocks:
                actions += node.get_legal_actions(block)
            actions.sort(key=lambda x: surface_heuristic(node, x))
            for action in actions:
                possible_move = node.generate_successor(action, True)
                new_s = self.helper.greedy_search(possible_move)
                for act in new_s:
                    possible_move = possible_move.generate_successor(act, True)
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
                good_act = self.helper.greedy_search(successor) if depth + 1 == self.depth else []
                for act in good_act:
                    successor = successor.generate_successor(act, True)
                temp_list = list_of_act + good_act
                temp = self.AlphaBetaPruning(successor, depth + 1, alpha, beta, True, temp_list)
                beta = min(beta, temp)
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
                block_3 = list(block_3)
                if block_3 not in comb_lst: comb_lst.append(block_3)
            return self._threes_lists


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
        self._node = game_state
        actions = []
        for block in game_state.current_blocks:
            actions += game_state.get_legal_actions(block)

        # sort the action by heuristic

        actions.sort(key=lambda x: surface_heuristic(game_state, x) + row_col_completeness_heuristic(game_state, x))
        # Initializes with the maximum values for alpha, beta
        alpha, beta = -float('inf'), float('inf')
        best = None
        for board, act_on_board in MultiAgentSearchAgent.generate_successor(game_state):
            n_alpha = self.AlphaBetaPruning(board, 0, alpha, beta, False, act_on_board) - board.points
            if n_alpha > alpha:
                best = act_on_board
                alpha = n_alpha
            if alpha >= beta:
                break
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
            return self.evaluation_function(self._node, list_of_act)
        if maxPlayer:
            # get oll legal action for the agent
            for board, act_on_board in MultiAgentSearchAgent.generate_successor(node):
                act_list = list_of_act + act_on_board
                alpha = max(alpha, self.AlphaBetaPruning(
                    board, depth,
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
                # Completes the moves by the helper agent if depth +1 == self.depth else the alpha agent will complete
                # the god act
                good_act = self.helper.greedy_search(successor) if depth + 1 == self.depth else []
                for act in good_act:
                    successor = successor.generate_successor(act, True)
                temp_list = list_of_act + good_act
                temp = self.AlphaBetaPruning(successor, depth + 1, alpha, beta, True, temp_list)
                beta = min(beta, temp)
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
            self._threes_lists = make_sub_group(blocks, 3)
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
