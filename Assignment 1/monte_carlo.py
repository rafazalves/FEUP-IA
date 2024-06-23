import random
import math
import game
import copy
import numpy as np

class Node:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = copy.deepcopy(game_state)
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.reward = 0

    def get_reward(self):
        winner = self.game_state.check_winner()
        if winner == 0:
            return 0.5
        elif winner == self.game_state.playing:
            return 1
        else:
            return 0

    def child(self, move):
        new_game_state = copy.deepcopy(self.game_state)
        new_game_state.update(move[0], move[1])
        child = Node(new_game_state, self, move)
        self.children.append(child)
        return child

    def update (self, result):
        self.visits += 1
        self.wins += result


    def unvisited_moves(self):
        moves = self.game_state.get_all_moves()
        return [(piece, move) for (piece, move) in moves if move not in self.children]

    def is_terminal(self):
        return self.game_state.check_winner() != 0

    def is_fully_expanded(self):
        return len(self.unvisited_moves()) == 0


    def child(self, move):
        new_game_state = copy.deepcopy(self.game_state)
        new_game_state.update(move[0], move[1])
        child = Node(new_game_state, self, move)
        self.children.append(child)
        return child

    def reward(self):
        winner = self.game_state.check_winner()
        if winner == 0:
            return 0.5
        elif winner == self.game_state.playing:
            return 1
        else:
            return 0

    def visits(self):
        if self.visits == 0:
            return 0.0001
        return self.visits


def monte_carlo_tree_search(root, n_iter):
    for _ in range(n_iter):
        print("Iteration: ", _)
        leaf = traverse(root)
        simulation_result = rollout(leaf)
        backpropagate(leaf, simulation_result)
    return best_child(root, 0)

# Node Traversal
def traverse(node):
    while not node.is_terminal():
        if not node.is_fully_expanded():
            return expand(node)
        else:
            node = best_uct(node)
    return node

# Node Expansion
def expand(node):
    unvisited_moves = node.unvisited_moves()
    move = unvisited_moves[np.random.choice(len(unvisited_moves))]
    return node.child(move)

# Node Simulation
def rollout(node):
    while not node.is_terminal():
        possible_moves = node.unvisited_moves()
        move = possible_moves[np.random.choice(len(possible_moves))]
        node = node.child(move)
    return node.get_reward()

# Node Backpropagation
def backpropagate(node, result):
    while node is not None:
        node.update(result)
        node = node.parent

# Node Selection
def best_child(node, exploration_weight):
    best_score = float('-inf')
    best_children = []
    for child in node.children:
        exploit = child.reward / child.visits
        explore = (2.0 * math.log(node.visits) / child.visits) ** 0.5
        score = exploit + exploration_weight * explore
        if score == best_score:
            best_children.append(child)
        if score > best_score:
            best_children = [child]
            best_score = score
    return random.choice(best_children)

# Upper Confidence Bound for Trees (UCT)
def uct(node):
    exploit = node.reward / node.visits
    explore = (2.0 * math.log(node.parent.visits) / node.visits) ** 0.5
    return exploit + explore

# Best UCT
def best_uct(node):
    return max(node.children, key=uct)