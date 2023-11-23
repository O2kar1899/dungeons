import pygame
import constants
from character import Character

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

player_image = pygame.image.load("assets/images/characters/elf/idle/0.png").convert_alpha()

# create player
player = Character(100, 100, player_image)

# game loop
run = True
while run:
    # create frame rate

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

    # draw player
    player.draw(screen)

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
