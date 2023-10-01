""" MIGHT REMOVE!!!
from abc import ABC, abstractmethod
from collections import defaultdict
import math


class MCTS:
    # Monte Carlo Tree Searcher. Rolls out the tree, then makes a move

    def __init__(self, explore_weight = 1):
        self.Q = defaultdict(int) # Total node reward
        self.N = defaultdict(int) # Node visit count
        self.children = dict() # children of nodes
        self.explore_weight = explore_weight

    # Choose the best move (Choose best successor node)
    def choose(self, node):
        if node.is_terminal():
            raise RuntimeError("Choose called on a terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf") # Stops unseen moves
            return self.Q[n] / self.N[n] # Average reward

        return max(self.children[node], key=score)

    # +1 iteration of the tree
    def rollout(self, node):
        path = self.select(node)
        leaf = path[-1]
        self.expand(leaf)
        reward = self.simulate(leaf)
        self.back_prop(path, reward)

    # Find unexplored child
    def select(self, node):
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # Node unexplored/terminal
                return path

            unexplored = self.children[node] - self.children.keys()

            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self.uct_select(node) # go a layer deeper

    # Update the children dict with the children of "node"
    def expand(self, node):
        if node in self.children:
            return # already expanded
        self.children[node] = node.find_children()

    # Return the reward for a random simulation (to completion) of the selected node
    def simulate(self, node):
        invert = True
        while True:
            if node.is_terminal():
                reward = node.reward()
                if invert:
                    return 1 - reward
                else:
                    return reward
            node = node.find_random_child()
            invert = not invert

    # Send the reward back up the tree
    def back_prop(self, path, reward):
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward # 1 for me, 0 for enemy, and vice versa

    # Select a child node, balancing exploration and exploitation
    def uct_select(self, node):
        assert all(n in self.children for n in self.children[node])

        logNvertex = math.log(self.N[node])

        # Upper confidence bound for trees
        def uct(n):
            return self.Q[n] / self.N[n] + self.explore_weight * math.sqrt(logNvertex / self.N[n])

        return max(self.children[node], key=uct)


class Node(ABC):
    @abstractmethod
    # All possible successors of this board state
    def find_children(self):
        return set()

    @abstractmethod
    # Random successor of this board state
    def find_random_child(self):
        return None

    @abstractmethod
    # if node has no children, return True
    def is_terminal(self):
        return True

    @abstractmethod
    # Assume self is terminal. 1=win, 0=loss, .5 = tie
    def reward(self):
        return 0

    @abstractmethod
    # Nodes must be hashable
    def __hash__(self):
        return 123456789

    @abstractmethod
    # Are nodes comparable?
    def __eq__(node1, node2):
        return True
"""
