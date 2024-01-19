import sys
import math
import random
import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)


class Player:
    def __init__(self, x, y, width, height, color):

        self.x = x
        self.y = y
        self.speed_player = 20
        self.color = color

        self.width = width
        self.height = height


        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def up(self):
        if  self.rect.y <= 0:
            pass

        else:
            self.rect.y -= self.speed_player

    def down(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            pass

        else:
            self.rect.y += self.speed_player

    def collide(self, x, y, radius, raio):
        return self.rect.colliderect(x - radius, y - radius, radius * 2, radius * 2)


    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, self.color, self.rect)



class Ball:
    def __init__(self, x, y, radius, color):

        self.radius = radius
        self.x = x
        self.y = y
        self.color = color

        self.localization = [x, y]
        self.speed = [direction_ball() * 5, direction_ball() * 5]


    def change_x(self):
        self.speed[0] = - self.speed[0]

    def change_y(self):
        self.speed[1] = - self.speed[1]


    def new_ball(self):
        self.localization[0] = self.x


    def move(self):
        if self.localization[1] < self.radius or self.localization[1] > SCREEN_HEIGHT - self.radius:
            self.change_y()

        self.localization[0] += self.speed[0]
        self.localization[1] += self.speed[1]


    def draw(self, SCREEN):
        pygame.draw.circle(SCREEN, self.color, (self.localization[0], self.localization[1]), self.radius)
        #pygame.draw.rect(SCREEN, (255, 0, 0), (self.localization[0] - self.radius, self.localization[1] - self.radius,  self.radius * 2, self.radius * 2), 1)


def direction_ball():
    direction = random.randint(1, 2)

    if direction == 1:
        return 1

    else:
        return - 1


def main():
    COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    player_1 = [Player(50, 150, 10, 100, COLOR)]
    player_2 = [Player((SCREEN_WIDTH - 50), 150, 10, 100, COLOR)]

    ball = [Ball(600, random.randint(200, 500), 15, COLOR)]

    clock = pygame.time.Clock()

    run = True
    collision = True
    bater_1 = True
    bater_2 = True

    while run:
        SCREEN.fill(WHITE)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


        for play_1 in player_1:
            play_1.draw(SCREEN)


        for play_2 in player_2:
            play_2.draw(SCREEN)


        for bal in ball:
            bal.draw(SCREEN)
            bal.move()

        output_key = pygame.key.get_pressed()


        if output_key[K_w]:
            play_1.up()

        if output_key[K_s]:
            play_1.down()

        if output_key[K_UP]:
            play_2.up()

        if output_key[K_DOWN]:
            play_2.down()


        if bal.localization[0] < - bal.radius or bal.localization[0] > SCREEN_WIDTH + bal.radius:
            bal.localization[0] = bal.x
            bal.speed = [direction_ball() * 5, direction_ball() * 5]
            bater_1 = True
            bater_2 = True


        if play_1.collide(bal.localization[0], bal.localization[1], bal.radius, bal.radius) and bater_1 == True:
            bater_1 = False
            bater_2 = True
            bal.change_x()


        elif play_2.collide(bal.localization[0], bal.localization[1], bal.radius, bal.radius) and bater_2 == True:
            bater_1 = True
            bater_2 = False
            bal.change_x()


        pygame.display.update()


if __name__ == '__main__':
    main()
