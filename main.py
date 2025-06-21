# gobang_with_menu.py
# Enhanced Gobang (Five-in-a-Row) with Strategy AI and Full Menu (Improved with Handcrafted Evaluation)
import pygame
import sys
import random

BOARD_SIZE = 15
CELL_SIZE = 40
MARGIN = 20
SCREEN_SIZE = BOARD_SIZE * CELL_SIZE + MARGIN * 2
EMPTY, BLACK, WHITE = 0, 1, 2

DIFFICULTY_MAP = {"Easy": 1, "Medium": 2, "Hard": 3}
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_turn = BLACK
player_color = BLACK
MAX_DEPTH = 2

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Gobang - Human vs AI")
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)

dx = [1, 1, 0, -1, -1, -1, 0, 1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

def draw_board():
    screen.fill((249, 214, 91))
    for i in range(BOARD_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (MARGIN, MARGIN + i * CELL_SIZE), (SCREEN_SIZE - MARGIN, MARGIN + i * CELL_SIZE))
        pygame.draw.line(screen, (0, 0, 0), (MARGIN + i * CELL_SIZE, MARGIN), (MARGIN + i * CELL_SIZE, SCREEN_SIZE - MARGIN))
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == BLACK:
                pygame.draw.circle(screen, (0, 0, 0), (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE), 16)
            elif board[y][x] == WHITE:
                pygame.draw.circle(screen, (255, 255, 255), (MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE), 16)

def draw_buttons(buttons):
    for label, rect in buttons.items():
        pygame.draw.rect(screen, (180, 180, 180), rect)
        text = small_font.render(label, True, (0, 0, 0))
        screen.blit(text, (rect.x + 10, rect.y + 10))

def menu():
    global MAX_DEPTH, player_color
    selecting = True
    difficulty_buttons = {"Easy": pygame.Rect(200, 100, 120, 40), "Medium": pygame.Rect(200, 160, 120, 40), "Hard": pygame.Rect(200, 220, 120, 40)}
    side_buttons = {"Play as Black": pygame.Rect(400, 100, 160, 40), "Play as White": pygame.Rect(400, 160, 160, 40)}
    exit_button = pygame.Rect(300, 300, 160, 40)
    selected_difficulty = "Medium"
    while selecting:
        screen.fill((240, 240, 240))
        text = font.render("Select Difficulty and Side", True, (0, 0, 0))
        screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, 40))
        draw_buttons(difficulty_buttons)
        draw_buttons(side_buttons)
        pygame.draw.rect(screen, (200, 100, 100), exit_button)
        screen.blit(small_font.render("Exit", True, (0, 0, 0)), (exit_button.x + 50, exit_button.y + 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for label, rect in difficulty_buttons.items():
                    if rect.collidepoint(pos):
                        selected_difficulty = label
                for label, rect in side_buttons.items():
                    if rect.collidepoint(pos):
                        player_color = BLACK if label == "Play as Black" else WHITE
                        MAX_DEPTH = DIFFICULTY_MAP[selected_difficulty]
                        selecting = False
                if exit_button.collidepoint(pos):
                    pygame.quit(); sys.exit()

def is_valid_move(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x] == EMPTY

def check_win(x, y, color):
    def count(dx_, dy_):
        cnt = 1
        for d in [1, -1]:
            i = 1
            while True:
                nx, ny = x + dx_ * i * d, y + dy_ * i * d
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == color:
                    cnt += 1
                    i += 1
                else:
                    break
        return cnt
    for dx_, dy_ in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        if count(dx_, dy_) >= 5:
            return True
    return False

def show_winner(text):
    draw_board()
    pygame.display.flip()
    pygame.time.wait(500)
    screen.fill((255, 255, 255))
    win_text = font.render(text, True, (255, 0, 0))
    screen.blit(win_text, (SCREEN_SIZE // 2 - 100, SCREEN_SIZE // 2 - 60))
    restart_rect = pygame.Rect(SCREEN_SIZE // 2 - 80, SCREEN_SIZE // 2, 160, 40)
    menu_rect = pygame.Rect(SCREEN_SIZE // 2 - 80, SCREEN_SIZE // 2 + 60, 160, 40)
    pygame.draw.rect(screen, (200, 200, 200), restart_rect)
    pygame.draw.rect(screen, (180, 180, 180), menu_rect)
    screen.blit(small_font.render("Restart", True, (0, 0, 0)), (restart_rect.x + 40, restart_rect.y + 10))
    screen.blit(small_font.render("Main Menu", True, (0, 0, 0)), (menu_rect.x + 25, menu_rect.y + 10))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    reset_game()
                    return
                elif menu_rect.collidepoint(event.pos):
                    menu()
                    reset_game()
                    return

def point(x, y, color):
    def count(u):
        cnt = 1
        for d in [1, -1]:
            i = 1
            while True:
                nx, ny = x + dx[u] * i * d, y + dy[u] * i * d
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == color:
                    cnt += 1
                    i += 1
                else:
                    break
        return cnt
    score = 0
    for u in range(4):
        c = count(u)
        if c >= 5:
            score += 10000
        elif c == 4:
            score += 1000
        elif c == 3:
            score += 100
        elif c == 2:
            score += 10
    return score

def best_move():
    max_score = -1
    move = None
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == EMPTY:
                score = point(x, y, WHITE) + point(x, y, BLACK) * 0.8
                if score > max_score:
                    max_score = score
                    move = (x, y)
    return move

def reset_game():
    global board, current_turn
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_turn = BLACK
    main_game()

def main_game():
    global current_turn
    if player_color == WHITE:
        move = best_move()
        if move:
            board[move[1]][move[0]] = WHITE
            current_turn = BLACK
    while True:
        draw_board()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_turn == player_color:
                mx, my = pygame.mouse.get_pos()
                x = (mx - MARGIN + CELL_SIZE // 2) // CELL_SIZE
                y = (my - MARGIN + CELL_SIZE // 2) // CELL_SIZE
                if is_valid_move(x, y):
                    board[y][x] = player_color
                    if check_win(x, y, player_color):
                        show_winner("You Win!")
                    current_turn = WHITE if player_color == BLACK else BLACK
                    move = best_move()
                    if move:
                        board[move[1]][move[0]] = WHITE if player_color == BLACK else BLACK
                        if check_win(move[0], move[1], WHITE if player_color == BLACK else BLACK):
                            show_winner("AI Wins!")
                        current_turn = player_color

menu()
main_game()
