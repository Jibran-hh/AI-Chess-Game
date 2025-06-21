from board.chessboard import board
from player.AI import AI
from board.move import move
import pygame

class ChessGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("AI Chess Game")
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.board = board()
        self.board.createboard()
        self.move_handler = move()
        self.ai = AI()
        
        # Game state
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.current_turn = "WHITE"  # WHITE or BLACK (AI)
        
        # GUI elements
        self.init_gui_elements()
        
        # Move input
        self.move_input = ""
        self.move_input_active = False
        self.input_rect = pygame.Rect(300, 750, 200, 30)
        
    def init_gui_elements(self):
        # Colors
        self.BACKGROUND_COLOR = (40, 40, 40)
        self.TITLE_COLOR = (255, 215, 0)
        self.BUTTON_COLOR = (101, 67, 33)
        self.BUTTON_HOVER_COLOR = (139, 69, 19)
        self.TEXT_COLOR = (255, 248, 220)
        self.BORDER_COLOR = (255, 215, 0)
        
        # Fonts
        self.title_font = pygame.font.Font('freesansbold.ttf', 64)
        self.button_font = pygame.font.Font('freesansbold.ttf', 32)
        self.input_font = pygame.font.Font('freesansbold.ttf', 20)
        
        # Text elements
        self.title_text = self.title_font.render('AI Chess Game', True, self.TITLE_COLOR)
        self.start_text = self.button_font.render('Start Game', True, self.TEXT_COLOR)
        self.checkmate_text = self.button_font.render('Checkmate!', True, self.TEXT_COLOR)
        self.stalemate_text = self.button_font.render('Stalemate!', True, self.TEXT_COLOR)
        self.thinking_text = self.button_font.render('AI is thinking...', True, self.TEXT_COLOR)
        
        # Text positions
        self.title_rect = self.title_text.get_rect(center=(400, 150))
        self.start_rect = self.start_text.get_rect(center=(400, 350))
        self.status_rect = self.thinking_text.get_rect(center=(400, 720))
        
        # Button
        self.start_button = pygame.Rect(300, 300, 200, 100)

    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                self.game_state = "PLAYING"
                return True
        return False

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.move_input_active:
                if event.key == pygame.K_RETURN:
                    self.process_move_input()
                elif event.key == pygame.K_BACKSPACE:
                    self.move_input = self.move_input[:-1]
                else:
                    self.move_input += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.move_input_active = True
            else:
                self.move_input_active = False

    def process_move_input(self):
        # Convert algebraic notation to board coordinates
        try:
            # Example: "e2e4" -> convert to board coordinates
            from_square = self.algebraic_to_coord(self.move_input[:2])
            to_square = self.algebraic_to_coord(self.move_input[2:])
            # Validate and make move
            # TODO: Implement move validation and execution
            self.move_input = ""
        except:
            print("Invalid move format")

    def algebraic_to_coord(self, alg):
        # Convert algebraic notation (e.g., "e4") to board coordinates
        file = ord(alg[0].lower()) - ord('a')
        rank = 8 - int(alg[1])
        return (rank, file)

    def draw_menu(self):
        self.display.fill(self.BACKGROUND_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw button with hover effect
        if self.start_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.display, self.BUTTON_HOVER_COLOR, self.start_button)
        else:
            pygame.draw.rect(self.display, self.BUTTON_COLOR, self.start_button)
        pygame.draw.rect(self.display, self.BORDER_COLOR, self.start_button, 2)
        
        # Draw text
        self.display.blit(self.title_text, self.title_rect)
        self.display.blit(self.start_text, self.start_rect)

    def draw_game(self):
        # Draw board and pieces
        self.board.draw(self.display)
        
        # Draw move input box
        pygame.draw.rect(self.display, self.TEXT_COLOR, self.input_rect, 2)
        text_surface = self.input_font.render(self.move_input, True, self.TEXT_COLOR)
        self.display.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        
        # Draw status text
        if self.current_turn == "BLACK":
            self.display.blit(self.thinking_text, self.status_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

                if self.game_state == "MENU":
                    if self.handle_menu_events(event):
                        self.board.reset()
                elif self.game_state == "PLAYING":
                    self.handle_game_events(event)

            if self.game_state == "MENU":
                self.draw_menu()
            elif self.game_state == "PLAYING":
                self.draw_game()

            pygame.display.update()
            self.clock.tick(60) 