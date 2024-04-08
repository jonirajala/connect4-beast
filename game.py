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
        moves = [self.is_allowed(col, board) for col in range(board.shape[1])]
        return [index for index, element in enumerate(moves) if element]

    def simulate(self, move, n, board, player):
        wins = 0
        for i in range(n):
            sim_board = board.copy()
            sim_player = player
            if move is not None:
                _, sim_board = self.play_move(move, sim_board, sim_player)
                sim_player *= -1
            
            state = "Continue"
            while state == "Continue":
                allowed_moves = self.allowed_moves(sim_board)
                random_move = np.random.choice(allowed_moves)
                state, sim_board = self.play_move(random_move, sim_board, sim_player)
                if state == "Win":
                    if sim_player == player:
                        wins += 1
                    break
                sim_player *= -1
        return wins
    