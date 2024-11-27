import pygame
from mosquito import Mosquito
from constants import *
from hand_tracker import track_hand_closed
import state
import cv2
from hand import Hand
import mediapipe as mp


def offset(mask1, mask2):
    return int(mask2.x - mask1.x), int(mask2.y - mask1.y)


def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    # For webcam input:
    cap = cv2.VideoCapture(0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mosquito")
    clock = pygame.time.Clock()

    # Load mosquito sprite
    mosquito_group = pygame.sprite.Group()

    # Spawn a mosquito every 2 seconds
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, MOSQUITO_SPAWN_PERIOD)

    TRACK_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(TRACK_EVENT, HAND_TRACK_PERIOD)

    state.is_running = True
    hand_closed = False
    hand_coords = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    hand = Hand()
    while state.is_running:
        screen.fill((255, 255, 255))  # White background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.is_running = False
            elif event.type == SPAWN_EVENT:
                mosquito = Mosquito()
                mosquito_group.add(mosquito)
            elif event.type == TRACK_EVENT:
                res = track_hand_closed(mp_drawing, mp_drawing_styles, mp_hands, cap)
                if res:
                    hand_coords, hand_closed = res

        # Update and draw mosquitoes
        mosquito_group.update()
        mosquito_group.draw(screen)

        hand.update(hand_coords, hand_closed)
        hand.draw(screen)

        for mosquito in mosquito_group:
            if (
                mosquito.mask.overlap(hand.mask, offset(mosquito.rect, hand.rect))
                and hand.closed
            ):
                mosquito.kill()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
