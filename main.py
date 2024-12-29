# main.py
import pygame
from board import Board
from game import Game
from ai import AI
from ui import UI

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("中国象棋")
    clock = pygame.time.Clock()

    board = Board(screen)
    game = Game()
    ai = AI('black', game)  # AI为黑方
    ui = UI(game, board, screen, ai)

    running = True
    while running:
        screen.fill((0, 128, 0))  # 背景色绿色
        ui.draw()
        ui.handle_events()
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()
