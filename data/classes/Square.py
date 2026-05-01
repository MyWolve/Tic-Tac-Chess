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

        self.pos = self.get_coord()
        self.center = (self.abs_x + width // 2, self.abs_y + height // 2)

        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        self.draw_color = (220, 208, 194) if self.color == 'light' else (53, 53, 53)
        self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 228, 10)
        
        self.occupying_piece = None
        self.highlight = False

        self.rect = pygame.Rect(
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )

    def get_coord(self):
        columns = 'ABCD'
        return columns[self.x] + str(self.y + 1)

    def draw(self, display):
        # configures if tile should be light or dark and draws it
        pygame.draw.rect(display, self.draw_color, self.rect)
    
                