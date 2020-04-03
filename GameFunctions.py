from math import pi, cos, sin, atan2, hypot


def detectCollision(x1, y1, w1, h1, x2, y2, w2, h2):

    if (x2 + w2 >= x1 >= x2 and y2 + h2 >= y1 >= y2):
        return True
    elif (x2 + w2 >= x1 + w1 >= x2 and y2 + h2 >= y1 >= y2):
        return True
    elif (x2 + w2 >= x1 >= x2 and y2 + h2 >= y1 + h1 >= y2):
        return True
    elif (x2 + w2 >= x1 + w1 >= x2 and y2 + h2 >= y1 + h1 >= y2):
        return True
    else:
        return False


def get_angle(origin, destination):
    # Возвращает угол к объекту в радианах
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)


def project(pos, angle, distance):
    # Плавно двигает к объекту
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))


def distanceto(origin, players):
    dist = 5000
    disttarget = None
    for player in players:
        temp = hypot(origin[0] - player.pos[0], origin[1] - player.pos[1])
        if temp < dist and player.health > 0:
            dist = temp
            disttarget = player
    return disttarget
