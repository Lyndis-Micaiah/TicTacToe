import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
MENU_HEIGHT = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (65, 105, 225)
LIGHT_BLUE = (100, 149, 237)
RED = (220, 20, 60)
GREEN = (34, 139, 34)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class TicTacToe:
    def __init__(self, size):
        self.size = size
        self.cell_size = min((WINDOW_SIZE - 100) // size, 150)
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.ai_mode = False
        self.thinking = False
        
        # Center the board
        self.board_offset_x = (WINDOW_SIZE - (self.cell_size * size)) // 2
        self.board_offset_y = (WINDOW_SIZE - (self.cell_size * size)) // 2

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            elif self.is_board_full():
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.ai_mode and self.current_player == 'O':
                    self.thinking = True
                    return True  # Return here to let the display update first
            return True
        return False

    def check_winner(self):
        win_length = 3 if self.size == 4 else (4 if self.size == 5 else self.size)
        
        # Check rows
        for i in range(self.size):
            for j in range(self.size - win_length + 1):
                if self.board[i][j] != ' ':
                    if all(self.board[i][j+k] == self.board[i][j] for k in range(win_length)):
                        return True

        # Check columns
        for i in range(self.size - win_length + 1):
            for j in range(self.size):
                if self.board[i][j] != ' ':
                    if all(self.board[i+k][j] == self.board[i][j] for k in range(win_length)):
                        return True

        # Check diagonals
        for i in range(self.size - win_length + 1):
            for j in range(self.size - win_length + 1):
                if self.board[i][j] != ' ':
                    # Check diagonal (top-left to bottom-right)
                    if all(self.board[i+k][j+k] == self.board[i][j] for k in range(win_length)):
                        return True
                    
                # Check diagonal (top-right to bottom-left)
                if self.board[i][j+win_length-1] != ' ':
                    if all(self.board[i+k][j+win_length-1-k] == self.board[i][j+win_length-1] for k in range(win_length)):
                        return True
        return False

    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def ai_move(self):
        
        # Try to win
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    if self.check_winner():
                        self.game_over = True
                        self.winner = 'O'
                        return
                    self.board[i][j] = ' '
        
        # Block player's winning move
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'X'
                    if self.check_winner():
                        self.board[i][j] = 'O'
                        self.current_player = 'X'
                        return
                    self.board[i][j] = ' '
        
        # Take center if available
        center = self.size // 2
        if self.board[center][center] == ' ':
            self.board[center][center] = 'O'
            if self.check_winner():
                self.game_over = True
                self.winner = 'O'
            else:
                self.current_player = 'X'
            return
        
        # Take random empty cell
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == ' ']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 'O'
            if self.check_winner():
                self.game_over = True
                self.winner = 'O'
            else:
                self.current_player = 'X'

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('TicTacToe')
        self.state = 'menu'
        self.game = None
        self.font = pygame.font.Font(None, 48)
        self.create_buttons()

    def create_buttons(self):
        # Main menu buttons
        center_x = WINDOW_SIZE // 2
        self.menu_buttons = [
            Button(center_x - 100, 200, 200, 50, "Play", BLUE, LIGHT_BLUE),
            Button(center_x - 100, 300, 200, 50, "How to Play", BLUE, LIGHT_BLUE),
            Button(center_x - 100, 400, 200, 50, "Exit", RED, (200, 0, 0))
        ]
        
        # Mode selection buttons
        self.mode_buttons = [
            Button(center_x - 100, 200, 200, 50, "2 Players", BLUE, LIGHT_BLUE),
            Button(center_x - 100, 300, 200, 50, "vs AI", BLUE, LIGHT_BLUE),
            Button(center_x - 100, 400, 200, 50, "Back", GRAY, (100, 100, 100))
        ]
        
        # Grid size selection buttons
        self.size_buttons = [
            Button(center_x - 100, 200, 200, 50, "3 x 3", BLUE, LIGHT_BLUE),
            Button(center_x - 100, 300, 200, 50, "4 x 4", BLUE, LIGHT_BLUE),
            Button(center_x - 100, 400, 200, 50, "5 x 5", BLUE, LIGHT_BLUE),
            Button(center_x - 100, 500, 200, 50, "Back", GRAY, (100, 100, 100))
        ]
        
        # Back to menu button for game screen
        self.menu_button = Button(WINDOW_SIZE - 110, WINDOW_SIZE - 60, 100, 40, "Menu", BLUE, LIGHT_BLUE)

    def draw_menu(self):
        self.screen.fill(WHITE)
        title = self.font.render('TicTacToe', True, BLACK)
        self.screen.blit(title, (WINDOW_SIZE//2 - title.get_width()//2, 100))
        
        for button in self.menu_buttons:
            button.draw(self.screen)

    def draw_mode_selection(self):
        self.screen.fill(WHITE)
        title = self.font.render('Select Mode', True, BLACK)
        self.screen.blit(title, (WINDOW_SIZE//2 - title.get_width()//2, 100))
        
        for button in self.mode_buttons:
            button.draw(self.screen)

    def draw_size_selection(self):
        self.screen.fill(WHITE)
        title = self.font.render('Select Grid Size', True, BLACK)
        self.screen.blit(title, (WINDOW_SIZE//2 - title.get_width()//2, 100))
        
        for button in self.size_buttons:
            button.draw(self.screen)

    def draw_how_to_play(self):
        self.screen.fill(WHITE)
        title = self.font.render('How to Play', True, BLACK)
        self.screen.blit(title, (WINDOW_SIZE//2 - title.get_width()//2, 50))
        
        instructions = [
            "1. Choose game mode: 2 Players or vs AI",
            "2. Select grid size: 3x3, 4x4, or 5x5",
            "3. Players take turns placing X and O",
            "4. Get your marks in a row to win!",
            "(horizontal, vertical, or diagonal)"
        ]
        
        small_font = pygame.font.Font(None, 36)
        for i, text in enumerate(instructions):
            line = small_font.render(text, True, BLACK)
            self.screen.blit(line, (50, 150 + i * 50))
        
        self.menu_button.draw(self.screen)

    def draw_game(self):
        self.screen.fill(WHITE)
        
        # Draw grid
        for i in range(self.game.size + 1):
            pygame.draw.line(self.screen, BLACK,
                           (self.game.board_offset_x + i * self.game.cell_size, self.game.board_offset_y),
                           (self.game.board_offset_x + i * self.game.cell_size, 
                            self.game.board_offset_y + self.game.size * self.game.cell_size), 2)
            pygame.draw.line(self.screen, BLACK,
                           (self.game.board_offset_x, self.game.board_offset_y + i * self.game.cell_size),
                           (self.game.board_offset_x + self.game.size * self.game.cell_size,
                            self.game.board_offset_y + i * self.game.cell_size), 2)

        # Draw X's and O's
        for i in range(self.game.size):
            for j in range(self.game.size):
                if self.game.board[i][j] == 'X':
                    x = self.game.board_offset_x + j * self.game.cell_size + 20
                    y = self.game.board_offset_y + i * self.game.cell_size + 20
                    pygame.draw.line(self.screen, BLUE,
                                   (x, y),
                                   (x + self.game.cell_size - 40, y + self.game.cell_size - 40), 3)
                    pygame.draw.line(self.screen, BLUE,
                                   (x + self.game.cell_size - 40, y),
                                   (x, y + self.game.cell_size - 40), 3)
                elif self.game.board[i][j] == 'O':
                    x = self.game.board_offset_x + j * self.game.cell_size + self.game.cell_size//2
                    y = self.game.board_offset_y + i * self.game.cell_size + self.game.cell_size//2
                    pygame.draw.circle(self.screen, RED,
                                    (x, y),
                                    self.game.cell_size//2 - 20, 3)

        # Draw status
        status_color = BLACK
        if self.game.game_over:
            if self.game.winner:
                status_text = f"Player {self.game.winner} wins!"
                status_color = GREEN if self.game.winner == 'X' else RED
            else:
                status_text = "It's a tie!"
        else:
            if self.game.ai_mode and self.game.current_player == 'O' and self.game.thinking:
                status_text = "AI is thinking..."
            else:
                status_text = f"Player {self.game.current_player}'s turn"

        status = self.font.render(status_text, True, status_color)
        self.screen.blit(status, (20, WINDOW_SIZE - 50))
        self.menu_button.draw(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                    if self.state == 'menu':
                        for i, button in enumerate(self.menu_buttons):
                            if button.handle_event(event):
                                if i == 0:  # Play
                                    self.state = 'mode_selection'
                                elif i == 1:  # How to Play
                                    self.state = 'how_to_play'
                                elif i == 2:  # Exit
                                    pygame.quit()
                                    sys.exit()
                    
                    elif self.state == 'mode_selection':
                        for i, button in enumerate(self.mode_buttons):
                            if button.handle_event(event):
                                if i < 2:  # 2 Players or vs AI
                                    self.ai_mode = (i == 1)
                                    self.state = 'size_selection'
                                else:  # Back
                                    self.state = 'menu'
                    
                    elif self.state == 'size_selection':
                        for i, button in enumerate(self.size_buttons):
                            if button.handle_event(event):
                                if i < 3:  # Grid size selection
                                    self.game = TicTacToe(i + 3)
                                    self.game.ai_mode = self.ai_mode
                                    self.state = 'game'
                                else:  # Back
                                    self.state = 'mode_selection'
                    
                    elif self.state == 'how_to_play':
                        if self.menu_button.handle_event(event):
                            self.state = 'menu'
                    
                    elif self.state == 'game':
                        if self.menu_button.handle_event(event):
                            self.state = 'menu'
                        elif event.type == pygame.MOUSEBUTTONDOWN and not self.game.game_over and not self.game.thinking:
                            x, y = event.pos
                            if (self.game.board_offset_x <= x <= self.game.board_offset_x + self.game.size * self.game.cell_size and
                                self.game.board_offset_y <= y <= self.game.board_offset_y + self.game.size * self.game.cell_size):
                                row = (y - self.game.board_offset_y) // self.game.cell_size
                                col = (x - self.game.board_offset_x) // self.game.cell_size
                                if 0 <= row < self.game.size and 0 <= col < self.game.size:
                                    if self.game.board[row][col] == ' ':
                                        self.game.board[row][col] = self.game.current_player
                                        if self.game.check_winner():
                                            self.game.game_over = True
                                            self.game.winner = self.game.current_player
                                        elif self.game.is_board_full():
                                            self.game.game_over = True
                                        else:
                                            if self.game.current_player == 'X':
                                                self.game.current_player = 'O'
                                            else:
                                                self.game.current_player = 'X'
                                            if self.game.ai_mode:
                                                self.game.thinking = True

            # Handle AI move after delay
            if (self.state == 'game' and self.game.ai_mode and 
                self.game.current_player == 'O' and self.game.thinking):
                current_time = pygame.time.get_ticks()
                if not hasattr(self, 'ai_start_time'):
                    self.ai_start_time = current_time
                elif current_time - self.ai_start_time >= 1500:  # 1.5 second delay
                    self.game.thinking = False
                    self.game.ai_move()
                    delattr(self, 'ai_start_time')

            # Draw current state
            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'mode_selection':
                self.draw_mode_selection()
            elif self.state == 'size_selection':
                self.draw_size_selection()
            elif self.state == 'how_to_play':
                self.draw_how_to_play()
            elif self.state == 'game':
                self.draw_game()
            
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
