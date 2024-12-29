# ai.py
import copy
import time

class AI:
    def __init__(self, color, game):
        self.color = color
        self.game = game
        self.max_depth = 4
        self.start_time = 0
        self.time_limit = 2.5  # 秒内完成决策

        # 棋子价值
        self.piece_values = {
            '帅': 10000, '将': 10000,
            '车': 90, '马': 30, '炮': 50,
            '兵': 10, '卒': 10,
            '士': 20, '仕':20, '象': 20, '相':20
        }

    def get_move(self):
        self.start_time = time.time()
        best_move = None
        best_score = -float('inf')
        for move in self.generate_all_moves(self.game, self.color):
            new_game = copy.deepcopy(self.game)
            new_game.move_piece(move[0], move[1])
            score = self.minimax(new_game, self.max_depth -1, -float('inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move
            if time.time() - self.start_time > self.time_limit:
                break
        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.check_game_over() is not None:
            return self.evaluate(game)
        if time.time() - self.start_time > self.time_limit:
            return self.evaluate(game)
        if maximizing_player:
            max_eval = -float('inf')
            for move in self.generate_all_moves(game, self.color):
                new_game = copy.deepcopy(game)
                new_game.move_piece(move[0], move[1])
                eval = self.minimax(new_game, depth -1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent = 'black' if self.color == 'red' else 'red'
            for move in self.generate_all_moves(game, opponent):
                new_game = copy.deepcopy(game)
                new_game.move_piece(move[0], move[1])
                eval = self.minimax(new_game, depth -1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, game):
        score = 0
        for row in game.board:
            for piece in row:
                if piece is not None:
                    value = self.piece_values.get(piece.name, 0)
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value
        return score

    def generate_all_moves(self, game, color):
        moves = []
        for x in range(9):
            for y in range(10):
                piece = game.board[x][y]
                if piece is not None and piece.color == color:
                    # 生成该棋子的所有合法走步
                    piece_moves = self.get_piece_moves(game, piece)
                    for move in piece_moves:
                        moves.append(((x, y), move))
        return moves

    def get_piece_moves(self, game, piece):
        # 根据棋子类型生成所有可能的移动位置
        moves = []
        if piece.name == '车':
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            for dx, dy in directions:
                nx, ny = piece.position[0] + dx, piece.position[1] + dy
                while 0 <= nx <9 and 0 <= ny <10:
                    target = game.board[nx][ny]
                    if target is None:
                        moves.append((nx, ny))
                    else:
                        if target.color != piece.color:
                            moves.append((nx, ny))
                        break
                    nx += dx
                    ny += dy
        elif piece.name == '马':
            potential_moves = [
                (piece.position[0] +1, piece.position[1] +2),
                (piece.position[0] +2, piece.position[1] +1),
                (piece.position[0] +1, piece.position[1] -2),
                (piece.position[0] +2, piece.position[1] -1),
                (piece.position[0] -1, piece.position[1] +2),
                (piece.position[0] -2, piece.position[1] +1),
                (piece.position[0] -1, piece.position[1] -2),
                (piece.position[0] -2, piece.position[1] -1),
            ]
            for move in potential_moves:
                if 0 <= move[0] <9 and 0 <= move[1] <10:
                    if game.is_valid_move(piece, piece.position, move):
                        moves.append(move)
        # 添加其他棋子的走法...
        return moves
