import pygame_tictactoe as game
import tictactoe_ai as ai
import pygame
import sys


clock = pygame.time.Clock()
player = 2
computer = 1
game_over = False
game.draw_window()
while True:
    clock.tick(game.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            clicked_row = int(mouse_y // game.SQUARE_SIZE)
            clicked_col = int(mouse_x // game.SQUARE_SIZE)
            if game.available_square(clicked_row, clicked_col):
                game.mark_square(clicked_row, clicked_col, player)
                game.draw_figures()
                if game.check_win(player):
                    game_over = True
                game.game_board = ai.comp_reaction(game.game_board, player, computer)
                if game.check_win(computer):
                    game_over = True
                game.draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = False
                game.restart()

    pygame.display.update()
