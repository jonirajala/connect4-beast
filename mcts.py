import numpy as np

class Node:
    def __init__(self, board, game, move=None, parent=None, player=None):
        self.board = board
        self.game = game
        self.move = move  
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.player = player  

    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.visits += 1
        self.wins += result

    def is_fully_expanded(self):
        return len(self.children) == len(self.game.allowed_moves(self.board))

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.wins / child.visits) + c_param * np.sqrt((2 * np.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]

def selection(node):
    while node.is_fully_expanded():
        node = node.best_child()
    return node
    

def expansion(leaf_node, game):    
    allowed_moves = game.allowed_moves(leaf_node.board)
    for move in allowed_moves:
        if not any(child.move == move for child in leaf_node.children):
            new_state, new_board = game.play_move(move, leaf_node.board.copy(), leaf_node.player)
            if new_state != "Continue":
                continue
            new_node = Node(board=new_board, game=game, move=move, parent=leaf_node, player=-leaf_node.player)
            leaf_node.add_child(new_node)
            return new_node
    return None

def backpropagate(node, result):
    while node is not None:
        node.update(result)
        node = node.parent

def mcts(game, board, player, iterations=500):
    root = Node(board=board.copy(), game=game, player=player)
    for _ in range(iterations):
        leaf_node = selection(root)
        expanded_node = expansion(leaf_node, game) if not leaf_node.is_fully_expanded() else leaf_node
        simulation_node = expanded_node if expanded_node is not None else leaf_node
        result = game.simulate(simulation_node.move, 300, simulation_node.board, simulation_node.player)
        backpropagate(simulation_node, result)

    
    print("Mcts", [child.wins for child in root.children])
    return root.best_child(c_param=0).move

def simple_mcts(game, board, player, iterations=500):
    allowed_moves = game.allowed_moves(board)
    wins = np.zeros_like(allowed_moves)
    n = int(iterations * 300 / 6)
    for i in range(len(allowed_moves)):
        wins[i] = game.simulate(allowed_moves[i], n, board, player)

    print("simple mcts", wins)
    return allowed_moves[np.argmax(wins)]

