import pygame
import sys
from GameObject import Archer, Warrior, Shoot, Mongol, Hit, Boss, SpeedBoost, Heal, Revive
from GameFunctions import detectCollision, distanceto
from TextFunctions import enemies_killed, showwave, boss
from random import randint
from Intro import game_intro, game_outro


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 128, 0)


pygame.init()
pygame.mixer.init(44100, 16, 2, 4096)
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
infoObject = pygame.display.Info()
winx, winy = infoObject.current_w, infoObject.current_h

picture = pygame.image.load('background1.jpg')
bg = pygame.transform.scale(picture, (winx, winy))

pygame.display.set_caption("Baty invasion")

pygame.mixer.music.load("Sounds/Songfinal.ogg")
pygame.mixer.music.set_volume(0.5)

#if winx == 1920 and winy == 1080:
#    bg = pygame.image.load('background1.jpg').convert_alpha()
#elif winx == 1440 and winy == 900:
#    bg = pygame.image.load('mac1.jpg').convert_alpha()
clock = pygame.time.Clock()
swordswing = pygame.mixer.Sound('Sounds/swing.ogg')
punch = pygame.mixer.Sound('Sounds/punch.ogg')
oof = pygame.mixer.Sound('Sounds/oof.ogg')
shoot = pygame.mixer.Sound('Sounds/shoot.ogg')
revive = pygame.mixer.Sound('Sounds/revive.ogg')

count = 0
enemies = []
enemyspawn = [(-5, winy // 4), (-5, winy // 4 * 3),
              (winx + 5, winy // 4), (winx + 5, winy // 4 * 3)]
spawntime = [
    pygame.time.get_ticks(),
    pygame.time.get_ticks(),
    pygame.time.get_ticks(),
    pygame.time.get_ticks()]
lastwave = pygame.time.get_ticks()
bonuses = []
wave = 1
boss_spawned = False
players = [Archer(400, 400), Warrior(600, 600)]


def drawWindow():
    window.blit(bg, (0, 0))
    for bonus in bonuses:
        bonus.render(window)
    for player in players:
        if player.health > 0:
            player.render(window)
            player.hprender(window, winx,winy)
    enemies_killed(count, window, winx)
    if boss_spawned:
        boss(window, winx, winy)
    for enemy in enemies:
        enemy.render(window)
        enemy.health_render(window)
    for bullet in players[0].bullets:
        bullet.draw(window)
    showwave(wave, window, winx)
#    for hit in players[1].hits:
#        hit.hitrender(window, players[1])
    pygame.display.update()


wavedone = True
enemywavecount = wave * 4


game_intro(winx, winy, window)  # Цикл Интро

pygame.mixer.music.play(-1)  # Музыка после интро
run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for el in enemyspawn:
        now = pygame.time.get_ticks()
        if now - lastwave >= 5000 and wavedone:  # 5 секунд между волнами и пройдена ли волна предыдущая
            if (now - spawntime[enemyspawn.index(el)] >=
                    2000) and (len(enemies) < enemywavecount):
                # 2 секунды между появлением врагов из одного спауна
                enemies.append(Mongol(el[0], el[1]))
                spawntime[enemyspawn.index(el)] = now
            if len(enemies) == enemywavecount:
                wavedone = False
    if wave % 5 == 0 and wavedone and not boss_spawned:
        enemies.append(Boss(winx // 2, -100))
        enemywavecount -= 10
        boss_time = pygame.time.get_ticks()
        boss_spawned = True

    if len(enemies) == 0 and not wavedone:
        wave += 1  # добавление волны
        boss_spawned = False
        wavedone = True  # счетчик, пройдена ли волна
        enemywavecount = wave * 4
        lastwave = now  # Время последней волны
    if players[0].health <= 0 and players[1].health <= 0:  # Надпись при смерти и выход из игры
        break
    for bullet in players[0].bullets:  # удаление стрел, которые улетели за экран
        if bullet.x < winx and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            players[0].bullets.pop(players[0].bullets.index(bullet))
    for hit in players[1].hits:  # Чтоб удар двигался вместе с игроком
        hit.hitupdate(players[1])

    for bonus in bonuses:
        for player in players:
            if player.health > 0:
                collisions = detectCollision(
                    bonus.x,
                    bonus.y,
                    40,
                    40,
                    player.x,
                    player.y,
                    player.width,
                    player.height)
                if collisions:
                    if isinstance(bonus, SpeedBoost):
                        bonus.boost(player)
                        player.bonusdict['speedboost'] = pygame.time.get_ticks()
                    elif isinstance(bonus, Heal):
                        bonus.apply(player)
                    elif isinstance(bonus, Revive):
                        revive.play()
                        bonus.apply(players)  # Принимает список игроков
                    bonuses.pop(bonuses.index(bonus))
    now = pygame.time.get_ticks()

    for player in players:
        for key in player.bonusdict:
            if now - player.bonusdict['speedboost'] >= 10000:  # отмена бонусов
                player.speed = 10

    for enemy in enemies:
        now = pygame.time.get_ticks()
        if enemy.health <= 0:
            count += 1  # счетчик убитых врагов
            if randint(1, 100) <= 10:  # Вероятность бонуса с моба //////
                probability = randint(1, 3)
                if probability == 1:
                    bonuses.append(SpeedBoost(enemy.x, enemy.y))
                elif probability == 2:
                    bonuses.append(Heal(enemy.x, enemy.y))
                elif probability == 3:
                    bonuses.append(Revive(enemy.x, enemy.y))
            enemies.pop(enemies.index(enemy))
            enemywavecount -= 1  # счетчик убитых в текущей волне игроков, чтобы не спавнились вечно

        targetdist = distanceto(enemy.pos, players)
        if isinstance(targetdist, Archer):
            if not detectCollision(
                    enemy.x,
                    enemy.y,
                    enemy.width,
                    enemy.height,
                    players[0].x,
                    players[0].y,
                    players[0].width,
                    players[0].height):
                # Если не касается, то преследовать игрока
                enemy.update(players[0])
            else:
                if now - enemy.lasthit >= enemy.cooldown:
                    enemy.lasthit = now
                    oof.play()  # Проигрыш звука получения урона
                    players[0].health -= enemy.attack
            if detectCollision(
                    enemy.x,
                    enemy.y,
                    enemy.width,
                    enemy.height,
                    players[1].x,
                    players[1].y,
                    players[1].width,
                    players[1].height) and players[1].health:
                if now - enemy.lasthit >= enemy.cooldown:
                    enemy.lasthit = now
                    oof.play()  # Проигрыш звука получения урона
                    players[1].health -= enemy.attack
        elif isinstance(targetdist, Warrior):
            if not detectCollision(
                    enemy.x,
                    enemy.y,
                    enemy.width,
                    enemy.height,
                    players[1].x,
                    players[1].y,
                    players[1].width,
                    players[1].height):
                # Если не касается, то преследовать игрока
                enemy.update(players[1])
            else:
                if now - enemy.lasthit >= enemy.cooldown:
                    enemy.lasthit = now
                    oof.play()  # Проигрыш звука получения урона
                    players[1].health -= enemy.attack
            if detectCollision(
                    enemy.x,
                    enemy.y,
                    enemy.width,
                    enemy.height,
                    players[0].x,
                    players[0].y,
                    players[0].width,
                    players[0].height) and players[0].health:
                # Если коснется другого игрока, будучи заагренным на другого,
                # то ударить его
                if now - enemy.lasthit >= enemy.cooldown:
                    enemy.lasthit = now
                    oof.play()  # Проигрыш звука получения урона
                    players[0].health -= enemy.attack

        for bullet in players[0].bullets:  # Обработка выстрелов
            collisions = detectCollision(
                bullet.x,
                bullet.y,
                bullet.width,
                bullet.height,
                enemy.x,
                enemy.y,
                enemy.width,
                enemy.height)
            if collisions:
                # Если касание стрелы и врага - бьет врага, удаляет стрелу
                players[0].bullets.pop(players[0].bullets.index(bullet))
                punch.play()
                enemy.health -= players[0].attack

        if players[1].hits:  # Обработка ударов
            for hit in players[1].hits:
                now = pygame.time.get_ticks()
                collisions = detectCollision(
                    enemy.x,
                    enemy.y,
                    enemy.width,
                    enemy.height,
                    hit.x,
                    hit.y,
                    players[0].width,
                    players[0].height)
                if collisions:
                    punch.play()
                    # Если касание, то бьет врага
                    players[1].in_attack = False
                    enemy.health -= players[1].attack
                    players[1].hits.pop(players[1].hits.index(hit))
                # Удаление удара через кд времени
                elif now - players[1].lasthit >= hit.hitlength:
                    players[1].in_attack = False
                    players[1].hits.pop(players[1].hits.index(hit))

    if not enemies:
        for hit in players[1].hits:
            now = pygame.time.get_ticks()   # УДАЛЕНИЕ УДАРОВ, КОГДА ВРАГОВ НЕТ
            if now - players[1].lasthit >= hit.hitlength:
                players[1].in_attack = False
                players[1].hits.pop(players[1].hits.index(hit))
    for bullet in players[0].bullets:
        if now - players[0].lastshot >= 300:
            players[0].in_attack = False
    keys = pygame.key.get_pressed()
    # Обработка нажатия клавиш
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    if players[0].health > 0:
        if keys[pygame.K_SPACE]:
            if players[0].lastmove == 'right':
                players[0].facing = 1
            else:
                players[0].facing = -1
            if len(players[0].bullets) < 10:
                now = pygame.time.get_ticks()
                if now - players[0].lastshot >= players[0].cooldown:
                    players[0].lastshot = now
                    shoot.play()
                    players[0].in_attack = True
                    players[0].bullets.append(
                        Shoot(
                            round(
                                players[0].x +
                                players[0].width //
                                2),
                            round(
                                players[0].y +
                                players[0].height //
                                2),
                            players[0].facing))

        # Первый игрок, лучник

        if keys[pygame.K_LEFT] and players[0].x > 5:
            players[0].x -= players[0].speed
            players[0].left = True
            players[0].right = False
            players[0].facing = -1
            players[0].lastmove = 'left'
        elif keys[pygame.K_RIGHT] and players[0].x < (winx - players[0].width - 5):
            players[0].x += players[0].speed
            players[0].left = False
            players[0].right = True
            players[0].facing = 1
            players[0].lastmove = 'right'
        else:
            players[0].left = False
            players[0].right = False
            players[0].animcount = 0

        if keys[pygame.K_UP] and players[0].y > 5:
            players[0].y -= players[0].speed

        if keys[pygame.K_DOWN] and players[0].y < (
                winy - players[0].height - 5):
            players[0].y += players[0].speed

        # Второй игрок, воин
    if players[1].health > 0:
        if keys[pygame.K_a] and players[0].x > 5:
            players[1].x -= players[1].speed
            players[1].left = True
            players[1].right = False
            players[1].facing = -1
            players[1].lastmove = 'left'
        elif keys[pygame.K_d] and players[1].x < (winx - players[1].width - 5):
            players[1].x += players[1].speed
            players[1].left = False
            players[1].right = True
            players[1].facing = 1
            players[1].lastmove = 'right'
        else:
            players[1].left = False
            players[1].right = False
            players[1].animcount = 0

        if keys[pygame.K_w] and players[1].y > 5:
            players[1].y -= players[1].speed

        if keys[pygame.K_s] and players[1].y < (winy - players[1].height - 5):
            players[1].y += players[1].speed
        if keys[pygame.K_f]:
            if players[1].lastmove == 'right':
                players[1].facing = 1
            else:
                players[1].facing = -1
            now = pygame.time.get_ticks()
            if now - players[1].lasthit >= players[0].cooldown:
                players[1].in_attack = True
                players[1].lasthit = now
                swordswing.play()
                players[1].hits.append(Hit(players[1]))
    drawWindow()
game_outro(winx, winy, window, count)
pygame.quit()
sys.exit()
