# board.py
import pygame

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.width = 800
        self.height = 800
        self.margin = 40  # Margin for drawing
        self.grid_size = 80
        self.line_color = (74, 35, 16)  # #4A2310

    def draw_board(self):
        # Draw horizontal lines
        for i in range(10):
            start_pos = (self.margin, self.margin + i * self.grid_size)
            end_pos = (self.margin + 8 * self.grid_size, self.margin + i * self.grid_size)
            pygame.draw.line(self.screen, self.line_color, start_pos, end_pos, 2)

        # Draw vertical lines
        for i in range(9):
            start_pos = (self.margin + i * self.grid_size, self.margin)
            end_pos = (self.margin + i * self.grid_size, self.margin + 9 * self.grid_size)
            # Draw palace
            if i == 3 or i == 5:
                pygame.draw.line(self.screen, self.line_color, start_pos, (start_pos[0], start_pos[1] + 2 * self.grid_size), 2)
                pygame.draw.line(self.screen, self.line_color, (start_pos[0], end_pos[1] - 2 * self.grid_size), end_pos, 2)
            pygame.draw.line(self.screen, self.line_color, start_pos, end_pos, 2)

        # Draw the river
        river_y = self.margin + 4 * self.grid_size
        pygame.draw.line(self.screen, self.line_color,
                         (self.margin, river_y),
                         (self.margin + 8 * self.grid_size, river_y), 2)
        font = pygame.font.SysFont('SimHei', 20)
        text1 = font.render("楚河", True, self.line_color)
        text2 = font.render("汉界", True, self.line_color)
        self.screen.blit(text1, (self.margin + 2 * self.grid_size - text1.get_width()//2, river_y - 25))
        self.screen.blit(text2, (self.margin + 5 * self.grid_size - text2.get_width()//2, river_y - 25))
