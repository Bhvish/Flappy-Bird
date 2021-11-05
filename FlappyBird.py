import time
import os
import pygame
import random
import sys

light_blue = (207, 242, 252)
#blue = (0, 0, 250)
black = pygame.Color(0, 0, 0)
#green = (106, 196, 2)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = (34, 139, 34)
blue = (64, 224, 208)
pygame.init()

# resolution - width,height
width = 900
height = 720
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

img = pygame.image.load('flapbrd.png')
img_width = img.get_size()[0]
img_height = img.get_size()[1]


def show_score(score, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (width / 10, 15)
    else:
        score_rect.midtop = (width / 2, height / 1.25)
    surface.blit(score_surface, score_rect)


def blocks(x_block, y_block, block_width, block_height, gap):
    pygame.draw.rect(surface, green, [x_block, y_block, block_width, block_height])
    pygame.draw.rect(surface, green, [x_block, y_block + block_height + gap, block_width, height])


def makeTextObjs(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key
    return None


def msg_surface(text):
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    largeText = pygame.font.Font('freesansbold.ttf', 130)

    titletextSurf, titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = width / 2, height / 2
    surface.blit(titletextSurf, titleTextRect)

    typtextSurf, typTextRect = makeTextObjs('Press any key to continue', smallText)
    typTextRect.center = width / 2, ((height / 2) + 100)
    surface.blit(typtextSurf, typTextRect)

    pygame.display.update()
    time.sleep(1)

    while replay_or_quit() is None:
        clock.tick()

    main()


pygame.mixer.init()
s = 'sound'
crash = pygame.mixer.Sound(os.path.join(s, 'crash.mp3'))
pop = pygame.mixer.Sound(os.path.join(s, 'pop.ogg'))


def gameOver(score):
    font = pygame.font.Font('freesansbold.ttf', 90)
    game_over_surface = font.render('YOU DIED!', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width / 2, height / 4)
    surface.fill(black)
    surface.blit(game_over_surface, game_over_rect)
    show_score(score, 0, red, 'times', 30)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()



def bird(x, y, image):
    surface.blit(image, (x, y))


def main():
    x = 150
    y = 200
    y_move = 0

    x_block = width
    y_block = 0

    block_width = 50
    block_height = random.randint(0, height / 2)
    gap = img_height * 5

    # speed of blocks
    block_move = 5

    score = 0
    game_over = False

    # Game Loop/ Game State
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # keydown - when button is pressed keyup - when it's released
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 5

        y = y + y_move

        surface.fill(blue)
        bird(x, y, img)
        show_score(score, 1, white, 'consolas', 20)

        # Adding difficulty relative to score
        # Increasing the speed and decreasing the gap of blocks

        if 3 <= score < 5:
            block_move = 6
            gap = img_height * 3.3

        if 5 <= score < 8:
            block_move = 7
            gap = img_height * 3.1

        if 8 <= score < 14:
            block_move = 8
            gap = img_height * 3

        if score >= 14:
            block_move = 8
            gap = img_height * 2.5

        blocks(x_block, y_block, block_width, block_height, gap)
        x_block -= block_move

        # boundaries
        if y > height - img_height or y < 0:
            pygame.mixer.Sound.play(crash)
            gameOver(score)

        # blocks on surface or not
        if x_block < (-1 * block_width):
            x_block = width
            block_height = random.randint(0, height / 2)

        # Collision Detection

        # detecting whether we are past the block or not in X
        if x + img_width > x_block and x < x_block + block_width:
            if y < block_height or y + img_height > block_height + gap:
                pygame.mixer.Sound.play(crash)
                gameOver(score)

        if x > x_block + block_width and x < x_block + block_width + img_width / 5:
            pygame.mixer.Sound.play(pop)
            score += 1

        pygame.display.update()
        clock.tick(80)


main()
pygame.quit()
quit()