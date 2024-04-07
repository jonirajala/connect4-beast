import numpy as np

class Game:
    def init_env(self):
        # board, player
        return np.zeros((6, 7)), 1

    def play_move(self, col, board, player):
        col = int(col)
        for row in range(board.shape[0] - 1, -1 , -1):
            if board[row, col] == 0:
                board[row, col] = player
                break
        
        state = self.check_if_end(row, col, board, player)

        return state, board

    def is_allowed(self, col, board):
        return 0 <= col <= 6 and 0 in board[:, col] 

    def check_if_end(self, row, col, board, player):
        # Check for draw
        if not np.any(board == 0):
            return "Draw"

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal Right, Diagonal Left
        for dr, dc in directions:
            count = 1  # Count the last move
            # Check in the positive direction (right, down, down-right, down-left)
            r, c = row + dr, col + dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r, c] == player:
                count += 1
                r += dr
                c += dc
            # Check in the negative direction (left, up, up-left, up-right)
            r, c = row - dr, col - dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r, c] == player:
                count += 1
                r -= dr
                c -= dc
            # Check if there are four in a row
            if count >= 4:
                return "Win"

        # No win or draw
        return "Continue"

    def draw(self, board):
        output = ""
        for row in range(board.shape[0]):
            output += "|"
            for col in range(board.shape[1]):
                output += f"{int(board[row, col]) : ^{3}}|"
            output += "\n"
        print(output)

    def allowed_moves(self, board):
        return np.where([self.is_allowed(col, board) for col in range(board.shape[1])])[0]

    def simulate(self, col, n, board, player):
        wins = 0
        for i in range(n):
            sim_board = board.copy()
            sim_player = player
            if col is not None:
                _, sim_board = self.play_move(col, sim_board, sim_player)
                sim_player *= -1
            
            state = "Continue"
            while state == "Continue":
                allowed_moves = self.allowed_moves(sim_board)
                random_col = np.random.choice(allowed_moves)
                state, sim_board = self.play_move(random_col, sim_board, sim_player)
                if state == "Win":
                    if sim_player == player:
                        wins += 1
                    break
                sim_player *= -1
        return wins


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

    
    print([child.wins for child in root.children])
    return root.best_child().move

game = Game()
board, player = game.init_env()
state = "Continue"
while state == "Continue":
    game.draw(board)
    if player == 1:
        move = int(input(f"Player {player} move: "))
        while not game.is_allowed(move, board):
            print("Invalid Move")
            move = int(input(f"Player {player} move: "))
    else:
        move = mcts(game, board, player, 500)
    state, board = game.play_move(move, board, player)
    player *= -1

game.draw(board)
if state == "Win":
    print(f"Player {-player} wins")
else:
    print(state)
