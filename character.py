import pygame
import math
import constants


class Character:
    def __init__(self, x, y, mob_animations, char_type):
        self.char_type = char_type
        self.mob_animations = mob_animations
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:run
        self.running = False
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx, dy):
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True

        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        self.rect.y += dy

    def update(self):

        # check what action the player is performing
        if self.running is True:
            self.update_action(1)
        else:
            self.update_action(0)


        animation_cooldown = constants.ANIMATION_COOLDOWN
        # handle animtion
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check th new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animations settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(
            self.image, flip_x=self.flip, flip_y=False
        )
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, (constants.RED), self.rect, 1)
