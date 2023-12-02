import pygame
import constants
from character import Character
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDHT, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeons Crawler")

# create clock for maintaining frame rate
clock = pygame.time.Clock()

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", size=20)


# helper function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))


#  load heart images
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)


# load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)


# load character images
mob_animations: list = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]

animations_types = ["idle", "run"]
for mob in mob_types:
    # load images
    animation_list = []
    for animation in animations_types:
        #  reset tempory list of images
        tempp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            tempp_list.append(img)
        animation_list.append(tempp_list)
    mob_animations.append(animation_list)


# function for display game info
def draw_info():
    # draw lives
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))


#  damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #  move damage text up
        self.rect.y -= 1
        #  delete the counter after a few time
        self.counter += 1
        if self.counter > 30:  # noqa: PLR2004
            self.kill()


# create player
player = Character(x=100, y=100, health=100, mob_animations=mob_animations, char_type=0)

#  create enemy
enemy = Character(200, 300, 100, mob_animations, 1)

# create player's weapon
bow = Weapon(bow_image, arrow_image)

# create empty enemy list
enemy_list = []
enemy_list.append(enemy)

# create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()


# game loop
run = True
while run:
    # control frame rate
    clock.tick(constants.FPS)
    screen.fill(constants.BG)

    # calculate player movement
    dx = 0  # delta x
    dy = 0  # delta y
    if moving_right is True:
        dx = constants.SPEED
    if moving_left is True:
        dx = -constants.SPEED
    if moving_down is True:
        dy = constants.SPEED
    if moving_up is True:
        dy = -constants.SPEED

    # move player
    player.move(dx, dy)

    # update player
    for enemy in enemy_list:
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), (constants.RED))
            damage_text_group.add(damage_text)
    damage_text_group.update()

    # draw player on screens
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    draw_info()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key is pygame.K_a:
                moving_left = True
            if event.key is pygame.K_d:
                moving_right = True
            if event.key is pygame.K_w:
                moving_up = True
            if event.key is pygame.K_x:
                moving_down = True

        # keyboard button release
        if event.type == pygame.KEYUP:
            if event.key is pygame.K_a:
                moving_left = False
            if event.key is pygame.K_d:
                moving_right = False
            if event.key is pygame.K_w:
                moving_up = False
            if event.key is pygame.K_x:
                moving_down = False

    pygame.display.update()


pygame.quit()
