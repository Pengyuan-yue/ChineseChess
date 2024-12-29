# game.py
from piece import ChessPiece

class Game:
    def __init__(self):
        self.board = [[None for _ in range(10)] for _ in range(9)]
        self.current_turn = 'red'
        self.selected_piece = None
        self.init_pieces()

    def init_pieces(self):
        # 红方
        self.board[0][0] = ChessPiece('车', 'red', (0,0))
        self.board[1][0] = ChessPiece('马', 'red', (1,0))
        self.board[2][0] = ChessPiece('相', 'red', (2,0))
        self.board[3][0] = ChessPiece('仕', 'red', (3,0))
        self.board[4][0] = ChessPiece('帅', 'red', (4,0))
        self.board[5][0] = ChessPiece('仕', 'red', (5,0))
        self.board[6][0] = ChessPiece('相', 'red', (6,0))
        self.board[7][0] = ChessPiece('马', 'red', (7,0))
        self.board[8][0] = ChessPiece('车', 'red', (8,0))
        self.board[1][2] = ChessPiece('炮', 'red', (1,2))
        self.board[7][2] = ChessPiece('炮', 'red', (7,2))
        for i in range(0,9,2):
            self.board[i][3] = ChessPiece('卒', 'red', (i,3))

        # 黑方
        self.board[0][9] = ChessPiece('车', 'black', (0,9))
        self.board[1][9] = ChessPiece('马', 'black', (1,9))
        self.board[2][9] = ChessPiece('象', 'black', (2,9))
        self.board[3][9] = ChessPiece('士', 'black', (3,9))
        self.board[4][9] = ChessPiece('将', 'black', (4,9))
        self.board[5][9] = ChessPiece('士', 'black', (5,9))
        self.board[6][9] = ChessPiece('象', 'black', (6,9))
        self.board[7][9] = ChessPiece('马', 'black', (7,9))
        self.board[8][9] = ChessPiece('车', 'black', (8,9))
        self.board[1][7] = ChessPiece('炮', 'black', (1,7))
        self.board[7][7] = ChessPiece('炮', 'black', (7,7))
        for i in range(0,9,2):
            self.board[i][6] = ChessPiece('兵', 'black', (i,6))

    def move_piece(self, from_pos, to_pos):
        try:
            piece = self.board[from_pos[0]][from_pos[1]]
            if piece is None:
                raise ValueError("选中的位置没有棋子。")
            if piece.color != self.current_turn:
                raise ValueError("不是该棋子的回合。")
            if not self.is_valid_move(piece, from_pos, to_pos):
                raise ValueError("非法的棋步。")
            target = self.board[to_pos[0]][to_pos[1]]
            if target is not None and target.color == piece.color:
                raise ValueError("不能吃掉同颜色的棋子。")
            self.board[to_pos[0]][to_pos[1]] = piece
            self.board[from_pos[0]][from_pos[1]] = None
            piece.position = to_pos
            self.current_turn = 'black' if self.current_turn == 'red' else 'red'
            return True
        except ValueError as ve:
            print(f"错误: {ve}")
            return False

    def is_valid_move(self, piece, from_pos, to_pos):
        # 实现各类棋子的走法规则
        if piece.name in ['车', '马', '炮', '帅', '将', '士', '象', '相', '兵', '卒']:
            if piece.name == '车':
                return self.valid_rook_move(from_pos, to_pos)
            elif piece.name == '马':
                return self.valid_knight_move(from_pos, to_pos)
            elif piece.name == '炮':
                return self.valid_cannon_move(from_pos, to_pos)
            elif piece.name in ['帅', '将']:
                return self.valid_general_move(piece, to_pos)
            elif piece.name in ['士', '仕']:
                return self.valid_advisor_move(piece, to_pos)
            elif piece.name in ['象', '相']:
                return self.valid_elephant_move(piece, to_pos)
            elif piece.name in ['兵', '卒']:
                return self.valid_soldier_move(piece, to_pos)
        return False

    def valid_rook_move(self, from_pos, to_pos):
        if from_pos[0] != to_pos[0] and from_pos[1] != to_pos[1]:
            return False
        # 检查路径是否被阻挡
        if from_pos[0] == to_pos[0]:
            step = 1 if to_pos[1] > from_pos[1] else -1
            for y in range(from_pos[1] + step, to_pos[1], step):
                if self.board[from_pos[0]][y] is not None:
                    return False
        else:
            step = 1 if to_pos[0] > from_pos[0] else -1
            for x in range(from_pos[0] + step, to_pos[0], step):
                if self.board[x][from_pos[1]] is not None:
                    return False
        return True

    def valid_knight_move(self, from_pos, to_pos):
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        if (abs(dx), abs(dy)) not in [(1,2), (2,1)]:
            return False
        # 检查马脚是否被堵
        if abs(dx) == 1:
            block = (from_pos[0], from_pos[1] + dy//2)
        else:
            block = (from_pos[0] + dx//2, from_pos[1])
        if self.board[block[0]][block[1]] is not None:
            return False
        return True

    def valid_cannon_move(self, from_pos, to_pos):
        if from_pos[0] != to_pos[0] and from_pos[1] != to_pos[1]:
            return False
        count = 0
        if from_pos[0] == to_pos[0]:
            step = 1 if to_pos[1] > from_pos[1] else -1
            for y in range(from_pos[1] + step, to_pos[1], step):
                if self.board[from_pos[0]][y] is not None:
                    count +=1
        else:
            step = 1 if to_pos[0] > from_pos[0] else -1
            for x in range(from_pos[0] + step, to_pos[0], step):
                if self.board[x][from_pos[1]] is not None:
                    count +=1
        target = self.board[to_pos[0]][to_pos[1]]
        if target is None:
            return count ==0
        else:
            return count ==1

    def valid_general_move(self, piece, to_pos):
        # 将帅只能在九宫内移动一格
        palace_x = range(3,6)
        palace_y = range(0,3) if piece.color == 'red' else range(7,10)
        if to_pos[0] not in palace_x or to_pos[1] not in palace_y:
            return False
        dx = abs(to_pos[0] - piece.position[0])
        dy = abs(to_pos[1] - piece.position[1])
        return max(dx, dy) ==1

    def valid_advisor_move(self, piece, to_pos):
        # 士只能在九宫内对角移动一格
        palace_x = range(3,6)
        palace_y = range(0,3) if piece.color == 'red' else range(7,10)
        if to_pos[0] not in palace_x or to_pos[1] not in palace_y:
            return False
        dx = to_pos[0] - piece.position[0]
        dy = to_pos[1] - piece.position[1]
        return abs(dx) ==1 and abs(dy) ==1

    def valid_elephant_move(self, piece, to_pos):
        # 象只能走田字，每次移动两格，对称
        dx = to_pos[0] - piece.position[0]
        dy = to_pos[1] - piece.position[1]
        if abs(dx) !=2 or abs(dy) !=2:
            return False
        # 不能过河
        if piece.color == 'red' and to_pos[1] >4:
            return False
        if piece.color == 'black' and to_pos[1] <5:
            return False
        # 检查象眼是否被堵
        eye = (piece.position[0] + dx//2, piece.position[1] + dy//2)
        if self.board[eye[0]][eye[1]] is not None:
            return False
        return True

    def valid_soldier_move(self, piece, to_pos):
        dx = to_pos[0] - piece.position[0]
        dy = to_pos[1] - piece.position[1]
        if piece.color == 'red':
            if piece.position[1] >=5:
                # 过河前，仅可前进
                return dx ==0 and dy ==1
            else:
                # 过河后，可前进或横移
                return (dx ==0 and dy ==1) or (abs(dx) ==1 and dy ==0)
        else:
            if piece.position[1] <=4:
                return dx ==0 and dy ==-1
            else:
                return (dx ==0 and dy ==-1) or (abs(dx) ==1 and dy ==0)

    def check_game_over(self):
        # 检查是否有一方的将帅被将军或被将死
        # 简单示例：检查帅或将是否被吃
        red_general = None
        black_general = None
        for row in self.board:
            for piece in row:
                if piece is not None:
                    if piece.name in ['帅', '将']:
                        if piece.color == 'red':
                            red_general = piece
                        else:
                            black_general = piece
        if red_general is None:
            return 'black'
        if black_general is None:
            return 'red'
        # 检查是否直线对峙
        red_pos = (red_general.position[0], red_general.position[1])
        black_pos = (black_general.position[0], black_general.position[1])
        if red_pos[0] == black_pos[0]:
            blocked = False
            y_start = red_pos[1] +1
            y_end = black_pos[1]
            for y in range(y_start, y_end):
                if self.board[red_pos[0]][y] is not None:
                    blocked = True
                    break
            if not blocked:
                return 'black'  # 黑胜
        return None
