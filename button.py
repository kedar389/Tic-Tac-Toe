import pygame
from pygame.sprite import Sprite


class Button(Sprite):
    def __init__(self, normal_img, hover_img, center_position):
        super().__init__()

        default_image = normal_img
        hover_image = hover_img

        self.hover_state = False
        self.images = [default_image, hover_image]
        self.rects = [default_image.get_rect(center=center_position),
                      hover_image.get_rect(center=center_position)]

    @property
    def image(self):
        return self.images[1] if self.hover_state else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.hover_state else self.rects[0]


class HoverButton(Button):

    def __init__(self, normal_img, hover_img, center_position):
        super().__init__(normal_img, hover_img, center_position)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hover_state = True
        else:
            self.hover_state = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class PseudoButton(Button):
    def __init__(self, normal_img, hover_img, center_position, board, symbol):
        super().__init__(normal_img, hover_img, center_position)
        self.board = board
        self.symbol = symbol

    def update(self):

        if self.symbol == self.board.player_on_turn:
            self.hover_state = True
        else:
            self.hover_state = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
