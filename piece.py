# piece.py
import pygame

class ChessPiece:
    def __init__(self, name, color, position):
        self.name = name  # '车', '马', etc.
        self.color = color  # 'red' or 'black'
        self.position = position  # (x, y) grid position
        self.radius = 30  # Diameter 60 pixels

    def draw(self, screen, font):
        # Calculate pixel position
        grid_size = 80
        margin = 40
        x = margin + self.position[0] * grid_size
        y = margin + self.position[1] * grid_size

        # Draw circle
        if self.color == 'red':
            color = (255, 0, 0)
        else:
            color = (0, 0, 0)
        pygame.draw.circle(screen, color, (x, y), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), self.radius, 2)  # White border

        # Render text
        text_surface = font.render(self.name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
