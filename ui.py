# ui.py
import pygame

class UI:
    def __init__(self, game, board, screen, ai):
        self.game = game
        self.board = board
        self.screen = screen
        self.ai = ai
        self.font = pygame.font.SysFont('SimHei', 20)
        self.status_font = pygame.font.SysFont('SimHei', 24)
        self.selected = None
        self.message = ""

    def draw(self):
        self.board.draw_board()
        # 绘制所有棋子
        for row in self.game.board:
            for piece in row:
                if piece is not None:
                    piece.draw(self.screen, self.font)
        # 绘制选中的棋子高亮
        if self.selected:
            x, y = self.selected
            grid_size = self.board.grid_size
            margin = self.board.margin
            rect = pygame.Rect(margin + x * grid_size -30, margin + y * grid_size -30, 60, 60)
            pygame.draw.rect(self.screen, (0,255,0), rect, 3)

        # 绘制游戏状态
        status_text = f"当前回合: {self.game.current_turn}"
        text_surface = self.status_font.render(status_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

        # 绘制消息
        if self.message:
            msg_surface = self.font.render(self.message, True, (255, 255, 0))
            self.screen.blit(msg_surface, (10, 40))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                grid_pos = self.get_grid_pos(pos)
                if grid_pos:
                    self.process_click(grid_pos)

    def get_grid_pos(self, pos):
        margin = self.board.margin
        grid_size = self.board.grid_size
        x, y = pos
        if margin <= x <= margin + 8 * grid_size and margin <= y <= margin + 9 * grid_size:
            grid_x = (x - margin + grid_size //2) // grid_size
            grid_y = (y - margin + grid_size //2) // grid_size
            return (grid_x, grid_y)
        return None

    def process_click(self, grid_pos):
        piece = self.game.board[grid_pos[0]][grid_pos[1]]
        if self.selected:
            from_pos = self.selected
            to_pos = grid_pos
            if self.game.move_piece(from_pos, to_pos):
                self.message = ""
                self.selected = None
                # 检查游戏是否结束
                winner = self.game.check_game_over()
                if winner:
                    self.message = f"{winner} 胜利！"
                else:
                    # 如果是AI模式且当前回合切换到AI
                    if self.ai and self.game.current_turn == self.ai.color:
                        ai_move = self.ai.get_move()
                        if ai_move:
                            self.game.move_piece(ai_move[0], ai_move[1])
                            self.message = f"AI移动: {self.get_move_str(ai_move)}"
                            # 检查游戏是否结束
                            winner = self.game.check_game_over()
                            if winner:
                                self.message = f"{winner} 胜利！"
            else:
                self.message = "非法的走步。"
                self.selected = None
        else:
            if piece is not None and piece.color == self.game.current_turn:
                self.selected = grid_pos
        # Redraw will occur in the main loop

    def get_move_str(self, move):
        from_pos, to_pos = move
        piece = self.game.board[to_pos[0]][to_pos[1]]
        return f"{piece.name} 从 {from_pos} 到 {to_pos}"
