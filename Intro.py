from TextFunctions import text_objects
import pygame
import sys

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 128, 0)


def choosedef(winx, winy, window):
    if winx == 1440 and winy == 900:
        intro_bg = pygame.image.load('mac-bg.jpg')
    elif winx == 1920 and winy == 1080:
        intro_bg = pygame.image.load('fullhd-bg.jpg')
    elif winx == 1336 and winy == 768:
        intro_bg = pygame.image.load('1336x768.jpg')
    return intro_bg


def game_intro(winx, winy, window):
    intro_bg = choosedef(winx, winy, window)
    clock = pygame.time.Clock()
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        window.blit(intro_bg, (0, 0))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects(
            "Press SPACE to start or ESC to quit", largeText, red)
        TextRect.center = ((winx / 2), (winy / 4 * 3))
        window.blit(TextSurf, TextRect)
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE]:
            intro = False
        pygame.display.update()
        clock.tick(15)


def game_outro(winx, winy, window, score):
    outro_bg = choosedef(winx, winy, window)
    clock = pygame.time.Clock()
    outro = True
    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        window.blit(outro_bg, (0, 0))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects(
            "Press Space to quit", largeText, red)
        TextRect.center = ((winx / 2), (winy / 4 * 3))
        TextSurf1, TextRect1 = text_objects(
            "Your score: " + str(score), largeText, red)
        TextRect1.center = ((winx / 2), (winy / 4 * 3 + 50))
        window.blit(TextSurf, TextRect)
        window.blit(TextSurf1, TextRect1)
        if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        pygame.display.update()
        clock.tick(15)
