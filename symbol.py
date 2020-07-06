from pygame.sprite import Sprite
import pygame


class Symbol(Sprite):
    def __init__(self, image, coords, size):
        super().__init__()
        self.symbol_image = image
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        self.surface.blit(self.symbol_image, (0, 0))
        self.coords = coords

    def draw(self, surface):
        surface.blit(self.surface, self.coords)
