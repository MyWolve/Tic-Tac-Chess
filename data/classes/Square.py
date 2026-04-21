import pygame

class Square:
    def __init__(self, x, y, width, height, offset_x=0, offset_y=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.abs_x = offset_x + x * width
        self.abs_y = offset_y + y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x,y)
        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        self.draw_color = (220, 208, 194) if self.color == 'light' else (53, 53, 53)
        self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 228, 10)
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False
        self.rect = pygame.Rect(
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )

        # get the formal notation of the tile
    def get_coord(self):
        columns = 'abcd'
        return columns[self.x] + str(self.y + 1)

    def draw(self, display):
        # configures if tile should be light or dark and draws it
        pygame.draw.rect(display, self.draw_color, self.rect)