import pygame.freetype
import pygame

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)


def text_objects(text, font, color):
    text = font.render(text, True, color)
    return text, text.get_rect()


def enemies_killed(count, window, winx):
    font = pygame.font.SysFont(None, 30)
    text = font.render("Score: " + str(count), True, white)
    window.blit(text, (0, 0))

def boss(window, winx, winy):
    font = pygame.font.SysFont(None, 40)
    text, textrect = text_objects("ШЫНГЫС has entered the battlefield", font, red)
    textrect.center = (winx / 2, winy - 20)
    window.blit(text, textrect)


def showwave(wave, window, winx):
    font = pygame.font.SysFont(None, 40)
    text = font.render("Wave: " + str(wave), True, white)
    window.blit(text, (winx / 4 * 3, 0))
