import pygame
from constants import COLORS, MARGIN_TOP, MARGIN_SIDE, get_width

class Text:
    """A Text represents a piece of text displayed in the game."""

    def __init__(self, screen, board, font_type=None, font_size=50):
        """Initializes the Text.

        Arguments:
            screen(Surface): A pygame Surface representing the screen display.
            board(Board): The Board containing the squares and fleas.
            font_type(Font): The pygame font type to use.
            font_size(int): The font size to use.
        """
        self.screen = screen
        self.board = board
        self.font_type = font_type
        self.font_size = font_size

        self.screen_width = self.board.num_cols * get_width() + MARGIN_SIDE
        self.font = pygame.font.Font(self.font_type, self.font_size)

        self.top_area = pygame.Surface((self.screen_width, MARGIN_TOP))
        self.top_area.fill(COLORS['black'])

    def clear(self):
        """Clears the previous text by overlaying it with black."""

        self.screen.blit(self.top_area, self.top_area.get_rect())
        pygame.display.flip()

    def update(self, message):
        """Replaces the old text with new text and displays the new text.

        Arguments:
            message(str): The text to be displayed.
        """

        self.clear()
        text = self.font.render(message, True, COLORS['white'], COLORS['black'])
        text_rect = text.get_rect(center=(self.screen_width // 2, MARGIN_TOP // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
