from typing import Literal, Union
import pygame
import random
import image_loader
from constants import *


class Mosquito(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        size = self._get_randomized_size()

        self.image = image_loader.load(MOSQUITO_IMAGE_PATH, size, True)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.Mask(size, True)

        self.moving_direction, start_pos, self.velocity = self._define_spawn_pose(size)
        self._flip_if_necessary(self.moving_direction)

        self.rect.x, self.rect.y = start_pos[0], start_pos[1]

    def update(self):
        self.rect.x += self.velocity

        if self.moving_direction == "left" and self.rect.right < 0:
            self.kill()
        elif self.moving_direction == "right" and self.rect.left > SCREEN_WIDTH:
            self.kill()

    def _get_randomized_size(self):
        scale_factor = random.uniform(
            MOSQUITO_HITBOX_SCALER[0], MOSQUITO_HITBOX_SCALER[1]
        )
        size = int(MOSQUITO_SIZE[0] * scale_factor), int(
            MOSQUITO_SIZE[1] * scale_factor
        )
        return size

    def _flip_if_necessary(self, moving_direction):
        if moving_direction == "right":
            self.image = pygame.transform.flip(self.image, True, False)

    def _define_spawn_pose(
        self, size
    ) -> tuple[Literal["left", "right"], tuple[int, int], float]:
        direction = random.choice(("left", "right"))
        velocity = random.uniform(
            MOSQUITO_MOVE_SPEED["min"], MOSQUITO_MOVE_SPEED["max"]
        )
        if direction == "left":
            start_pos = (
                SCREEN_WIDTH + size[0],
                random.randint(0, SCREEN_HEIGHT - size[1] - MOSQUITO_SPAWN_MARGIN),
            )
            velocity *= -1
        else:
            start_pos = (
                -size[1],
                random.randint(0, SCREEN_HEIGHT - size[1] - MOSQUITO_SPAWN_MARGIN),
            )
        return direction, start_pos, velocity
