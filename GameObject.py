import pygame
from GameFunctions import get_angle, project
warriorRight = [
    pygame.image.load('Sprites/APright0.png'),
    pygame.image.load('Sprites/APright1.png'),
    pygame.image.load('Sprites/APright2.png'),
    pygame.image.load('Sprites/APright3.png')]

warriorLeft = [
    pygame.image.load('Sprites/APleft0.png'),
    pygame.image.load('Sprites/APleft1.png'),
    pygame.image.load('Sprites/APleft2.png'),
    pygame.image.load('Sprites/APleft3.png')]

archerRight = [
    pygame.image.load('Sprites/IMright0.png'),
    pygame.image.load('Sprites/IMright1.png'),
    pygame.image.load('Sprites/IMright2.png'),
    pygame.image.load('Sprites/IMright3.png')]

archerLeft = [
    pygame.image.load('Sprites/IMleft0.png'),
    pygame.image.load('Sprites/IMleft1.png'),
    pygame.image.load('Sprites/IMleft2.png'),
    pygame.image.load('Sprites/IMleft3.png')]

archerhitleft = [pygame.image.load('Sprites/IMhitleft.png')]
archerhitright = [pygame.image.load('Sprites/IMhitright.png')]

arrowleft = pygame.image.load('Sprites/arrow_left.png')
arrowright = pygame.image.load('Sprites/arrow_right.png')
archerStand = pygame.image.load('Sprites/IMfront0.png')
warriorStand = pygame.image.load('Sprites/apstand.png')


bossmove = [pygame.image.load('Sprites/bossleft1.png'),
            pygame.image.load('Sprites/bossleft2.png')]
mongolmove = [pygame.image.load('Sprites/mongol1.png'),
              pygame.image.load('Sprites/mongol2.png')]
warriorhitleft = [pygame.image.load('Sprites/APhitleft0.png'),
                  pygame.image.load('Sprites/APhitleft1.png')]
warriorhitright = [pygame.image.load('Sprites/APhit0.png'),
                   pygame.image.load('Sprites/APhit1.png')]

red = (255, 20, 20)
white = (255, 255, 255)
green = (0, 128, 0)
gold = (249, 166, 2)


class Player:
    def __init__(self, x, y):
        self.lastmove = 'right'
        self.facing = 1
        self.animcount = 0
        self.left = False
        self.right = False
        self.y = y
        self.x = x
        self.speed = 10
        self.width = 43
        self.maxhealth = self.health
        self.height = 71
        self.pos = (self.x + self.width // 2, self.y + self.height // 2)
        self.cooldown = 500
        self.bonusdict = {'speedboost': pygame.time.get_ticks()}
        self.walkleft = None
        self.walkright = None
        self.Stand = None
        self.in_attack = False
        self.attacklistright = None
        self.attacklistleft = None
        self.animhit = 0
        self.hitcount = None
        self.name = None
        self.hppos = None

    def render(self, window):
        if self.animcount + 1 >= 16:
            self.animcount = 0
        if not self.in_attack:
            if self.left:
                window.blit(
                    self.walkleft[self.animcount // 4], (self.x, self.y))
                self.animcount += 1
            elif self.right:
                window.blit(
                    self.walkright[self.animcount // 4], (self.x, self.y))
                self.animcount += 1
            else:
                window.blit(self.Stand, (self.x, self.y))
        else:
            if self.animhit + 1 >= self.hitcount:
                self.animhit = 0
            if self.lastmove == 'left':
                window.blit(
                    self.attacklistleft[self.animhit // 4], (self.x, self.y))
                self.animhit += 1
            elif self.lastmove == 'right':
                window.blit(
                    self.attacklistright[self.animhit // 4], (self.x, self.y))
                self.animhit += 1

    def hprender(self, window, winx, winy):
        pygame.draw.rect(
            window,
            (211, 211, 211),
            (winx // self.hppos - 5, 0, winx // 8 + 10, 40))
        pygame.draw.rect(
            window,
            green,
            (winx // self.hppos, 5, winx // 8 * self.health // self.maxhealth, 30))
        font = pygame.font.SysFont(None, 30)
        text = font.render(self.name, True, white)
        window.blit(text, (winx // self.hppos + 5, 10))


class Archer(Player):
    def __init__(self, x, y):
        self.lastshot = pygame.time.get_ticks()
        self.attack = 5
        self.health = 5
        Player.__init__(self, x, y)
        self.walkleft = archerLeft
        self.walkright = archerRight
        self.Stand = archerStand
        self.hitcount = 4
        self.attacklistleft = archerhitleft
        self.attacklistright = archerhitright
        self.bullets = []
        self.name = "Archer"
        self.hppos = 2


class Warrior(Player):
    def __init__(self, x, y):
        self.lasthit = pygame.time.get_ticks()
        self.attack = 10
        self.health = 10
        Player.__init__(self, x, y)
        self.hitcount = 8
        self.attacklistright = warriorhitright
        self.attacklistleft = warriorhitleft
        self.walkleft = warriorLeft
        self.walkright = warriorRight
        self.Stand = warriorStand
        self.hits = []
        self.name = "Warrior"
        self.hppos = 4


class Shoot():
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 20 * facing
        self.width = 9
        self.height = 21

    def draw(self, window):
        if self.facing == 1:
            window.blit(arrowright, (self.x, self.y))
        else:
            window.blit(arrowleft, (self.x, self.y))


class Enemy:
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.lasthit = pygame.time.get_ticks()
        self.cooldown = 1000
        self.img = None
        self.maxhealth = self.health
        self.animcount = 0
        self.pos = (self.x + self.width // 2, self.y + self.height // 2)
        self.movelist = None

    def render(self, window):
        if self.animcount + 1 >= 10:
            self.animcount = 0
        window.blit(self.movelist[self.animcount // 5], (self.x, self.y))
        self.animcount += 1

    def update(self, player):
        angle = get_angle(
            (self.x + self.width // 2,
             self.y + self.height // 2),
            (player.x + player.width // 2,
             player.y + player.height // 2))
        self.pos = project(self.pos, angle, self.speed)
        self.x = self.pos[0] - self.width // 2
        self.y = self.pos[1] - self.height // 2

    def health_render(self, window):
        pygame.draw.rect(
            window,
            red,
            (self.x, self.y - 10, self.width * self.health / self.maxhealth,
             5))


class Mongol(Enemy):
    def __init__(self, x, y):
        self.attack = 1
        self.health = 10
        self.speed = 4
        self.width = 50
        self.height = 50
        Enemy.__init__(self, x, y)
        self.img = pygame.image.load('Sprites/mongol.png')
        self.movelist = mongolmove


class Boss(Enemy):
    def __init__(self, x, y):
        self.attack = 3
        self.health = 100
        self.speed = 3
        self.width = 100
        self.height = 130
        Enemy.__init__(self, x, y)
        self.img = pygame.image.load('Sprites/boss.png')
        self.movelist = bossmove

    def boss(self, window):
        if self.animcount + 1 >= 10:
            self.animcount = 0
        window.blit(self.movelist[self.animcount // 5], (self.x, self.y))
        self.animcount += 1


class Hit:
    def __init__(self, player):
        self.facing = player.facing
        self.x = player.x + self.facing * 43
        self.y = player.y
        self.hitlength = 300

    def hitrender(self, window, player):
        if self.facing == 1:
            pygame.draw.rect(
                window,
                (255,
                 255,
                 255,
                 100),
                (player.x +
                 self.facing *
                 player.width,
                 player.y,
                 player.width,
                 player.height))
        else:
            pygame.draw.rect(
                window,
                (255,
                 255,
                 255,
                 128),
                (player.x +
                 self.facing *
                 player.width,
                 player.y,
                 player.width,
                 player.height))

    def hitupdate(self, player):
        self.x = player.x + self.facing * 43
        self.y = player.y


class Bonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 40
        self.width = 40

    def render(self, window):
        window.blit(self.img, (self.x, self.y))


class SpeedBoost(Bonus):
    def __init__(self, x, y):
        self.speed = 20
        Bonus.__init__(self, x, y)
        self.img = pygame.image.load('Sprites/bonusspeed.png')

    def boost(self, player):
        player.speed = self.speed
        player.speedboosted = True


class Heal(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.img = pygame.image.load('Sprites/bonusheal.png')

    def apply(self, player):
        player.health = player.maxhealth


class Revive(Bonus):
    def __init__(self, x, y):
        Bonus.__init__(self, x, y)
        self.width = 29
        self.height = 44
        self.img = pygame.image.load('Sprites/cross.png')

    def apply(self, players):
        for player in players:
            if player.health <= 0:
                player.health = player.maxhealth
