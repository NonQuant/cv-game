from typing import Literal
import pygame
import pygame.image as pimg
import pygame.transform as transform

def load(filename: Literal[100], size: tuple[int, int] | None, convert=False):
    img = pimg.load(filename)
    if convert:
        img = img.convert_alpha()
    if size:
        img = transform.scale(img, size)
    return img