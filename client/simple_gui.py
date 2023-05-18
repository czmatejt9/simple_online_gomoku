import pygame

RGB = tuple[int, int, int]
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "purple": (255, 0, 255),
    "cyan": (0, 255, 255),
    "yellow": (255, 255, 0),
    "light_grey": (211, 211, 211),
    "dark_grey": (50, 50, 50),
    "dark_yellow": (246, 190, 0)
}
MAX_NAME_LENGTH = 16

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, bg_color: RGB, hover_color: RGB, outline_thickness: int,
                 outline_color: RGB, text: str = "", fontsize: int = 0, font_color: RGB = (255, 255, 255),
                 font_hover_color: RGB = (0, 0, 0), font: str = "arial", active_color: RGB = (244, 132, 14)):
        self.bg_color = bg_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.hover_color = hover_color
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.text = text
        self.font = font
        self.fontsize = fontsize
        self.font_color = font_color
        self.font_hover_color = font_hover_color
        self.active = False
        self.active_color = active_color

    def draw(self, window: pygame.Surface, hover: bool = False):
        pygame.draw.rect(window, self.outline_color, (self.x - self.outline_thickness, self.y - self.outline_thickness,
                                                      self.width + self.outline_thickness * 2,
                                                      self.height + self.outline_thickness * 2), 6, 6)
        pygame.draw.rect(window, self.active_color if self.active else self.hover_color if hover else self.bg_color,
                         (self.x, self.y, self.width, self.height))

        if self.text:
            self.draw_text(window, hover)

    def draw_text(self, window: pygame.Surface, hover: bool):
        font = pygame.font.SysFont(self.font, self.fontsize)
        text = font.render(self.text, True, self.font_hover_color if hover else self.font_color)
        window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                           self.y + (self.height / 2 - text.get_height() / 2)))

    # checks if mouse is on button and if is it also draws the hover state, returns TRUE/FALSE
    def is_over(self, window: pygame.Surface, pos: tuple[int, int]):
        if self.x - self.outline_thickness < pos[0] < self.x + self.width + self.outline_thickness \
                and self.y - self.outline_thickness < pos[1] < self.y + self.height + self.outline_thickness:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            enlargement = self.outline_thickness - 3
            self.height += enlargement * 2
            self.width += enlargement * 2
            self.x -= enlargement
            self.y -= enlargement
            self.draw(window, True)
            self.height -= enlargement * 2
            self.width -= enlargement * 2
            self.x += enlargement
            self.y += enlargement

            return True
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.active and self.rect.collidepoint(event.pos):
                return self.text
            else:
                self.active = not self.active if self.rect.collidepoint(event.pos) else False
        return ""


class InputBox(Button):
    def __init__(self, x: int, y: int, width: int, height: int, bg_color: RGB, hover_color: RGB, outline_thickness: int,
                 outline_color: RGB, text: str, fontsize: int, only_number: bool = False):
        super().__init__(x, y, width, height, bg_color, hover_color, outline_thickness, outline_color, text, fontsize,
                         active_color=COLORS["black"])
        self.only_number = only_number

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]
            elif len(self.text) < MAX_NAME_LENGTH:
                if self.only_number:
                    if event.unicode.isnumeric() or (not self.text and event.unicode == "-"):
                        self.text += event.unicode
                else:
                    self.text += event.unicode
