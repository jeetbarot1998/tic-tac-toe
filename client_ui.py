import json
import pygame
from network import Network

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Display
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
FONT = pygame.font.Font(None, 36)

# Initialize network
n = Network()
player = int(n.getP())
print("You are player", player)

def draw_board(board):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(WINDOW, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(WINDOW, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            cell_value = board[row * BOARD_COLS + col]
            if cell_value == 'X':
                pygame.draw.line(WINDOW, RED, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(WINDOW, RED, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE),
                                 (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
            elif cell_value == 'O':
                pygame.draw.circle(WINDOW, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3, LINE_WIDTH)

def display_message(text, color, y_offset=0):
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    WINDOW.blit(text_surface, text_rect)

def main():
    run = True
    clock = pygame.time.Clock()
    game_over = False

    while run:
        clock.tick(60)

        try:
            data = n.send("get")
        except Exception as e:
            run = False
            print("Error:", e)
            break

        if data is not None:  # Check if data is not None before processing
            board_data = json.loads(data.decode())
            board = board_data['board']
            player_to_play = board_data['player_to_play']
            player_won = board_data['player_won']
            ready = board_data['ready']

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONUP and player_to_play == player and player_won is None:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    cell_index = clicked_row * BOARD_COLS + clicked_col
                    n.send(str(cell_index))

            WINDOW.fill(WHITE)
            draw_board(board)

            # Display player indicator and waiting message
            if ready:
                if player_to_play == player and player_won is None:
                    display_message("Your Turn (Player " + str(player) + ")", GREEN)
                elif player_to_play != player:
                    display_message("Waiting for Opponent...", GRAY)
            else:
                display_message("Waiting for Opponent to Join...", GRAY)

            pygame.display.update()

            if player_won is not None and not game_over:
                if player_won == player:
                    display_message("You Won!", RED)
                else:
                    display_message("You Lost.", RED)
                pygame.display.update()
                pygame.time.delay(3000)  # Pause for 3 seconds before closing
                n.send("close")  # Inform the server to close the game
                run = False  # Exit the game loop

    pygame.quit()

if __name__ == "__main__":
    main()
