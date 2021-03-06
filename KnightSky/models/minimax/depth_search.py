from KnightSky.helpers.timeit import timeit
from chess_py import *
from .move_tree import Tree


class Ai(Player):
    def __init__(self, input_color):
        """
        Creates interface for human player.

        :type input_color: Color
        """
        super(Ai, self).__init__(input_color)
        self.piece_scheme = piece_const.Piece_values()
        self.my_moves = []
        self.tree = None

    def __str__(self):
        return "Minimax"

    @timeit
    def generate_move(self, position):
        """
        Returns valid and legal move given position

        :type position: Board
        :rtype Move
        """
        print(position)
        print("Running depth search")

        if self.tree is None:
            self.tree = Tree(position, self.color, 2)
        else:
            self.tree.update_from_position(position)

        print("Initial", self.tree.depth)

        node = self.tree_search(self.tree.head, piece_const.Piece_values())
        self.tree.update_from_node(node)
        return node.move

    @timeit
    def tree_search(self, node, val_scheme):
        if node is None:
            raise AttributeError("Node cannot be None")

        if node.is_tail:
            raise AttributeError("Cannot calculate from tail nodes")

        if len(node.children) == 1:
            return node.children[0]

        if node.children[0].is_tail:
            return self.tree.best_continuation(node, val_scheme)

        return max(*node.children,
                   key=lambda x: self.tree_search(x, val_scheme).position.material_advantage(node.color, val_scheme))
