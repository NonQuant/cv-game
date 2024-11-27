import pygame
import image_loader
from constants import *


class Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = image_loader.load(HAND_OPEN_PATH, HAND_SIZE, True)
        self.rect = self.image.get_rect()
        self.closed = False
        self.need_reclosing = False
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, hand_coords, hand_closed):
        self.closed = bool(hand_closed) and not (self.need_reclosing)
        if hand_coords:
            self.rect.x, self.rect.y = (
                hand_coords[0] * SCREEN_WIDTH,
                hand_coords[1] * SCREEN_HEIGHT,
            )

        if hand_closed:
            self.image = image_loader.load(HAND_CLOSED_PATH, HAND_SIZE, True)
            self.need_reclosing = True
        else:
            self.image = image_loader.load(HAND_OPEN_PATH, HAND_SIZE, True)
            self.need_reclosing = False

    # Add this draw function so we can draw individual sprites
    def draw(self, screen):
        screen.blit(self.image, self.rect)
