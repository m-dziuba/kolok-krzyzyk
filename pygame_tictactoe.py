import pygame
import sys
import tictactoe_ai as ai


pygame.init()
# BOARD
BOARD_ROWS = 3
BOARD_COLS = 3

# WINDOW DIMENSIONS
WIDTH = 800
TOP_WINDOW_HEIGHT = WIDTH // 8
TOP_WINDOW_BORDER = TOP_WINDOW_HEIGHT // 10
HEIGHT = WIDTH + TOP_WINDOW_HEIGHT

# FONTS
MAIN_MENU_FONT_SIZE = WIDTH // 10
MAIN_MENU_FONT = pygame.font.Font('Assets\\ka1.ttf', MAIN_MENU_FONT_SIZE)
BUTTONS_FONT_SIZE = MAIN_MENU_FONT_SIZE * 3 // 4
BUTTONS_FONT = pygame.font.Font('Assets\\VCR_OSD_MONO.ttf', BUTTONS_FONT_SIZE)
SCOREBOARD_FONT_SIZE = TOP_WINDOW_HEIGHT // 2
SCOREBOARD_FONT = pygame.font.Font('Assets\\VCR_OSD_MONO.ttf', SCOREBOARD_FONT_SIZE)
SHORTCUTS_FONT_SIZE = TOP_WINDOW_HEIGHT // 3
SHORTCUTS_FONT = pygame.font.Font('Assets\\VCR_OSD_MONO.ttf', SHORTCUTS_FONT_SIZE)

# OPTIONS MENU DIMENSIONS
BUTTON_SPACING = TOP_WINDOW_HEIGHT
BORDER_WIDTH = TOP_WINDOW_BORDER // 2

BUTTON_WIDTH = int(BUTTONS_FONT_SIZE * 10.5)
BUTTON_HEIGHT = int(BUTTONS_FONT_SIZE * 1.2)

# GAME DIMENSIONS
LINE_WIDTH = WIDTH // 30
SQUARE_SIZE = WIDTH // BOARD_ROWS
CIRCLE_RADIUS = (SQUARE_SIZE // 2) - WIDTH // LINE_WIDTH
CIRCLE_WIDTH = int(LINE_WIDTH // 1.5)
CROSS_WIDTH = int(LINE_WIDTH * 1.2)
CROSS_SPACE = WIDTH // LINE_WIDTH
WINNING_LINE_SPACING = 15
WINNING_LINE_THICKNESS = 2 * LINE_WIDTH // 3

# SCOREBOARD DIMENSIONS
CROSS_SIZE = SCOREBOARD_FONT_SIZE
CIRCLE_SIZE = int((CROSS_SIZE // 2) * 1.2)

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CROSS_COLOUR = (14, 10, 66)
CIRCLE_COLOUR = (128, 128, 128)

# WINDOW
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("TIC TAC TOE")


def mark_square(game_board, row, col, player):
    game_board[row][col] = player


def available_square(game_board, row, col):
    return game_board[row][col] == 0


def is_board_full(game_board):
    if any(game_board[row][col] == 0 for row in range(BOARD_ROWS)
           for col in range(BOARD_COLS)):
        return False


def check_win(game_board, player):
    # vertical
    for col in range(BOARD_COLS):
        if all(game_board[i][col] == player for i in range(3)):
            draw_vertical_winning_line(col, player)
            return True
    # horizontal
    for row in range(BOARD_ROWS):
        if all(game_board[row][i] == player for i in range(3)):
            draw_horizontal_winning_line(row, player)
            return True
    if game_board[2][0] == player and game_board[1][1] == player and game_board[0][2] == player:
        draw_asc_diagonal_winning_line(player)
        return True
    if game_board[0][0] == player and game_board[1][1] == player and game_board[2][2] == player:
        draw_desc_diagonal_winning_line(player)
        return True
    return False


def check_draw(game_board):
    if all(game_board[i][j] != 0 for i in range(3) for j in range(3)):
        return True
    return False


def restart(game_board):
    draw_window()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            game_board[row][col] = 0


def draw_window():
    WIN.fill(WHITE)
    for i in (SQUARE_SIZE, 2 * SQUARE_SIZE):
        pygame.draw.line(WIN, BLACK, (i, TOP_WINDOW_HEIGHT), (i, HEIGHT + TOP_WINDOW_HEIGHT), LINE_WIDTH)
    for i in (SQUARE_SIZE, 2 * SQUARE_SIZE):
        pygame.draw.line(WIN, BLACK, (0, i + TOP_WINDOW_HEIGHT), (WIDTH, i + TOP_WINDOW_HEIGHT), LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (0, TOP_WINDOW_HEIGHT), (WIDTH, TOP_WINDOW_HEIGHT), TOP_WINDOW_BORDER)
    pygame.draw.line(WIN, BLACK, (0, 0), (WIDTH, 0), TOP_WINDOW_BORDER)


def draw_scoreboard(cross_wins, circle_wins):
    draw_text(f'{cross_wins}', SCOREBOARD_FONT, BLACK, WIN, WIDTH // 2 - SCOREBOARD_FONT_SIZE, SCOREBOARD_FONT_SIZE)
    pygame.draw.line(WIN, CROSS_COLOUR, (WIDTH // 2 - SCOREBOARD_FONT_SIZE * 2, int(CROSS_SIZE * 0.5)),
                     (WIDTH // 2 - TOP_WINDOW_HEIGHT - CROSS_SIZE, int(CROSS_SIZE * 1.5)), CROSS_WIDTH // 2)
    pygame.draw.line(WIN, CROSS_COLOUR, (WIDTH // 2 - SCOREBOARD_FONT_SIZE * 2, int(CROSS_SIZE * 1.5)),
                     (WIDTH // 2 - TOP_WINDOW_HEIGHT - CROSS_SIZE, int(CROSS_SIZE * 0.5)), CROSS_WIDTH // 2)
    draw_text(':', SCOREBOARD_FONT, BLACK, WIN, WIDTH // 2, SCOREBOARD_FONT_SIZE)
    draw_text(f'{circle_wins}', SCOREBOARD_FONT, BLACK, WIN, WIDTH // 2 + SCOREBOARD_FONT_SIZE, SCOREBOARD_FONT_SIZE)
    pygame.draw.circle(WIN, CIRCLE_COLOUR, (WIDTH // 2 + TOP_WINDOW_HEIGHT + CIRCLE_SIZE, SCOREBOARD_FONT_SIZE),
                       CIRCLE_SIZE, CIRCLE_WIDTH // 2)
    draw_text("r:reset", SHORTCUTS_FONT, BLACK, WIN,
              len("r:reset") * TOP_WINDOW_HEIGHT // 10, TOP_WINDOW_HEIGHT // 3)
    draw_text("esc:back", SHORTCUTS_FONT, BLACK, WIN,
              len("esc:back") * TOP_WINDOW_HEIGHT // 10,  2 * TOP_WINDOW_HEIGHT // 3)


def draw_winning_player(player):
    pygame.draw.rect(WIN, WHITE, (WIDTH // 4, TOP_WINDOW_BORDER, WIDTH // 2, TOP_WINDOW_HEIGHT - 2 * TOP_WINDOW_BORDER))

    if player == 1:
        x_or_o = "CROSS"
    elif player == 2:
        x_or_o = "CIRCLE"
    else:
        x_or_o = "NO ONE"
    draw_text(f'{x_or_o} WINS', SCOREBOARD_FONT, BLACK, WIN, WIDTH // 2, SCOREBOARD_FONT_SIZE)


def draw_figures(game_board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if game_board[row][col] == 1:
                pygame.draw.line(WIN, CROSS_COLOUR,
                                 (col * SQUARE_SIZE + CROSS_SPACE,
                                  row * SQUARE_SIZE + SQUARE_SIZE - CROSS_SPACE + TOP_WINDOW_HEIGHT),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - CROSS_SPACE,
                                  row * SQUARE_SIZE + CROSS_SPACE + TOP_WINDOW_HEIGHT), CROSS_WIDTH)
                pygame.draw.line(WIN, CROSS_COLOUR,
                                 (col * SQUARE_SIZE + CROSS_SPACE,
                                  row * SQUARE_SIZE + CROSS_SPACE + TOP_WINDOW_HEIGHT),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - CROSS_SPACE,
                                  row * SQUARE_SIZE + SQUARE_SIZE - CROSS_SPACE + TOP_WINDOW_HEIGHT), CROSS_WIDTH)
            elif game_board[row][col] == 2:
                pygame.draw.circle(WIN, CIRCLE_COLOUR, (
                    int(SQUARE_SIZE * (col + 0.5)), int(SQUARE_SIZE * (row + 0.5) + TOP_WINDOW_HEIGHT)
                ), CIRCLE_RADIUS, CIRCLE_WIDTH)


def draw_vertical_winning_line(col, player):
    colour = None
    pos_x = SQUARE_SIZE * (col + 0.5)
    if player == 1:
        colour = CROSS_COLOUR
    elif player == 2:
        colour = CIRCLE_COLOUR

    pygame.draw.line(WIN, colour, (pos_x, WINNING_LINE_SPACING + TOP_WINDOW_HEIGHT),
                     (pos_x, HEIGHT - WINNING_LINE_SPACING), WINNING_LINE_THICKNESS)


def draw_horizontal_winning_line(row, player):
    colour = None
    pos_y = SQUARE_SIZE * (row + 0.5)
    if player == 1:
        colour = CROSS_COLOUR
    elif player == 2:
        colour = CIRCLE_COLOUR
    pygame.draw.line(WIN, colour, (WINNING_LINE_SPACING, pos_y + TOP_WINDOW_HEIGHT),
                     (WIDTH - WINNING_LINE_SPACING, pos_y + TOP_WINDOW_HEIGHT), WINNING_LINE_THICKNESS)


def draw_asc_diagonal_winning_line(player):
    colour = None
    if player == 1:
        colour = CROSS_COLOUR
    elif player == 2:
        colour = CIRCLE_COLOUR
    pygame.draw.line(WIN, colour, (WINNING_LINE_SPACING, HEIGHT - WINNING_LINE_SPACING),
                     (WIDTH - WINNING_LINE_SPACING, WINNING_LINE_SPACING + TOP_WINDOW_HEIGHT), WINNING_LINE_THICKNESS)


def draw_desc_diagonal_winning_line(player):
    colour = None
    if player == 1:
        colour = CROSS_COLOUR
    elif player == 2:
        colour = CIRCLE_COLOUR
    pygame.draw.line(WIN, colour, (WINNING_LINE_SPACING, WINNING_LINE_SPACING + TOP_WINDOW_HEIGHT),
                     (WIDTH - WINNING_LINE_SPACING, HEIGHT - WINNING_LINE_SPACING), WINNING_LINE_THICKNESS)


def player_vs_player(game_board):
    clock = pygame.time.Clock()
    player = 1
    player_1_wins = 0
    player_2_wins = 0
    game_over = False
    draw_window()
    running = True
    while running:
        if game_over is False:
            draw_scoreboard(player_1_wins, player_2_wins)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = pygame.mouse.get_pos()
                if my >= TOP_WINDOW_HEIGHT:
                    clicked_row = int((my - TOP_WINDOW_HEIGHT) // SQUARE_SIZE)
                    clicked_col = int(mx // SQUARE_SIZE)
                    if available_square(game_board, clicked_row, clicked_col):
                        mark_square(game_board, clicked_row, clicked_col, player)
                        if check_win(game_board, player):
                            if player == 1:
                                player_1_wins += 1
                            else:
                                player_2_wins += 1
                            draw_winning_player(player)
                            game_over = True
                        elif check_draw(game_board):
                            draw_winning_player(3)
                            game_over = True
                        player = player % 2 + 1
                        draw_figures(game_board)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    player = 1
                    restart(game_board)

        pygame.display.update()


def player_vs_ai(game_board):
    clock = pygame.time.Clock()
    player = 1
    computer = 2
    player_wins = 0
    computer_wins = 0
    game_over = False
    draw_window()
    running = True
    while running:
        if game_over is False:
            draw_scoreboard(player_wins, computer_wins)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = pygame.mouse.get_pos()
                if my >= TOP_WINDOW_HEIGHT:
                    clicked_row = int((my - TOP_WINDOW_HEIGHT) // SQUARE_SIZE)
                    clicked_col = int(mx // SQUARE_SIZE)
                    if available_square(game_board, clicked_row, clicked_col):
                        mark_square(game_board, clicked_row, clicked_col, player)
                        draw_figures(game_board)
                        if check_win(game_board, player):
                            player_wins += 1
                            game_over = True
                        elif check_draw(game_board):
                            draw_winning_player(3)
                            game_over = True
                        game_board = ai.comp_reaction(game_board, player, computer)
                        if check_win(game_board, computer):
                            computer_wins += 1
                            game_over = True
                        draw_figures(game_board)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    restart(game_board)

        pygame.display.update()


def draw_text(text, font, colour, surface, x, y):
    text_obj = font.render(text, True, colour)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def create_button(text, font, colour, button_number):
    button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, button_number * BUTTON_SPACING,
                         BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(WIN, colour, button, BORDER_WIDTH, BORDER_WIDTH)
    draw_text(text, font, colour, WIN, WIDTH // 2,
              button_number * BUTTON_SPACING + BUTTON_HEIGHT // 2)
    return button


def main_menu():
    board = [[0 for i in range(BOARD_COLS)] for j in range(BOARD_ROWS)]

    click = False
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        WIN.fill(WHITE)
        draw_text("Main menu", MAIN_MENU_FONT, BLACK, WIN, WIDTH // 2, MAIN_MENU_FONT_SIZE)

        mx, my = pygame.mouse.get_pos()

        pvp_button = create_button("Player vs. Player", BUTTONS_FONT, BLACK, 2)
        pve_button = create_button("Player vs. AI", BUTTONS_FONT, BLACK, 3)
        settings_button = create_button("Settings", BUTTONS_FONT, BLACK, 4)
        if pvp_button.collidepoint(mx, my):
            if click:
                restart(board)
                player_vs_player(board)
        if pve_button.collidepoint(mx, my):
            if click:
                restart(board)
                player_vs_ai(board)
        if settings_button.collidepoint(mx, my):
            if click:
                pass

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


if __name__ == '__main__':
    main_menu()


# TODO change who goes 1st
# TODO pick cross or circle
# TODO load different shapes?
# TODO what colour
# TODO difficulty levels
