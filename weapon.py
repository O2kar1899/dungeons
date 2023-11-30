import pygame
import math
import constants


class Weapon:
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = constants.SHOT_COOLDOWN
        arrow = None
        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)  # -ve because pygame y coordinates increase down the screen
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # get mouse_klick
        if (
            pygame.mouse.get_pressed()[0]
            and not self.fired
            and (pygame.time.get_ticks() - self.last_shot > shot_cooldown)
        ):  # 0: mouse-button
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

            return arrow

        #  resert mouse klick
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

            return arrow

        return None

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(
            self.image,
            (
                (self.rect.centerx - int(self.image.get_width() / 2)),
                self.rect.centery - int(self.image.get_height() / 2),
            ),
        )


class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.x = x
        self.angle = angle
        self.image = self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #  calculate the horizental and vertical speeds based on the angel
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED)  # y coordinats degrees

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy



    def draw(self, surface):
        surface.blit(
            self.image,
            (
                (self.rect.centerx - int(self.image.get_width() / 2)),
                self.rect.centery - int(self.image.get_height() / 2),
            ),
        )
