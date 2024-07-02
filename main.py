import pygame
from pygame.locals import *
from sys import exit

pygame.init()

# Tamanho da Tela
SCREEN_WIDTH = 1200 # Largura da Tela
SCREEN_HEIGHT = 800 # Altura da Tela

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Limitações da Arena
start_line = 100 # Linha de Inicio da Arena (LIA)
finish_line = SCREEN_HEIGHT - start_line


'''if SCREEN_WIDTH - start_line >= SCREEN_HEIGHT:
    print(" Não é possivel gerar uma arena ")
    exit()'''


ball_speed = 5


# Cores
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
BLACK = (0, 0, 0)


class Player:
    def __init__(self, x, y, width, height):
        self.speed = ball_speed * 2

        # Box do Player
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Player
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def move_top(self):
        # Velocidade para Subir
        if self.rect.top <= start_line + self.speed:
            pass

        else:
            self.rect.y -= self.speed

    def move_down(self):
        # Velocidade para Descer
        if self.rect.bottom >= finish_line - self.speed:
            pass

        else:
            self.rect.y += self.speed


    def draw(self, SCREEN):
        # Desenhar na Tela
        pygame.draw.rect(SCREEN, BLACK, self.rect)
        pygame.draw.rect(SCREEN, WHITE, self.rect, 1, 20)


class Ball:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed = [ball_speed, ball_speed]


    def change_move_y(self):
        # Inverter diração da bola
        self.speed[1] = - self.speed[1]

    def change_move_x(self):
        # Inverter diração da bola
        self.speed[0] = - self.speed[0]

    def move(self):
        if start_line < 500: # Em 500 criasse um campo quadrado para arena, mas apenas 500!
            if self.rect.bottom >= SCREEN_HEIGHT - start_line or self.rect.top <= start_line:
                self.change_move_y()

        else:
            if self.rect.bottom <= SCREEN_HEIGHT - start_line + self.height or self.rect.top >= start_line - self.height:
                self.change_move_y()


        self.rect = self.rect.move(self.speed[0], self.speed[1])

    def collide(self, player):
        # Verifica se colidiu com o player
        return self.rect.colliderect(player)


    def draw(self, SCREEN):
        pygame.draw.circle(SCREEN, GREEN, self.rect.center, self.width // 2)


def map():
    color_line = WHITE

    #Vertical 1 e 2
    pygame.draw.line(SCREEN, color_line, (start_line, start_line), (SCREEN_WIDTH - start_line, start_line), 5)
    pygame.draw.line(SCREEN, color_line, (start_line, finish_line), (SCREEN_WIDTH - start_line, finish_line), 5)

    #Horizontal 1 e 2
    pygame.draw.line(SCREEN, color_line, (start_line, start_line), (start_line, SCREEN_HEIGHT - start_line), 5)
    pygame.draw.line(SCREEN, color_line, (SCREEN_WIDTH - start_line, SCREEN_HEIGHT - start_line), (SCREEN_WIDTH - start_line, start_line), 5)


def main():
    # Configurações do Jogo
    tick = 60
    color = GRAY


    # Configurações do Padrão dos Players
    width_player = 10
    height_player = 70
    y_player = SCREEN_HEIGHT // 2 - 35
    direcao_valida_1, direcao_valida_2 = True, True

    #Player 1 Localidade
    x_player_1 = start_line + 25

    # Player 2 Localidade
    x_player_2 = SCREEN_WIDTH - start_line - 25

    # Configurações da Bola
    x_ball = SCREEN_WIDTH // 2 + 35
    y_ball = SCREEN_HEIGHT // 2 - 35
    width_ball = 15
    height_ball = 15



    player_one = [Player(x_player_1, y_player, width_player, height_player)]
    player_two = [Player(x_player_2, y_player, width_player, height_player)]

    balls = [Ball(x_ball, y_ball, width_ball, height_ball)]

    clock = pygame.time.Clock()

    while True:
        clock.tick(tick)
        SCREEN.fill(color)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        # Desenhar todos os players na lista
        for p1 in player_one:
            p1.draw(SCREEN)

        for p2 in player_two:
            p2.draw(SCREEN)


        # Desenhar todas as bolas na lista
        for b in balls:
            b.draw(SCREEN)
            b.move()


        for ball in balls:
            # Faz a verificação da colisão Player Bola
            if ball.collide(player_one[balls.index(ball)]) or ball.collide(player_two[balls.index(ball)]):

                # JOGADOR 1
                if ball.collide(player_one[balls.index(ball)]) and direcao_valida_1:
                    direcao_valida_1 = False
                    direcao_valida_2 = True
                    ball.change_move_x()

                # JOGADOR 2
                elif ball.collide(player_two[balls.index(ball)]) and direcao_valida_2:
                    direcao_valida_1 = True
                    direcao_valida_2 = False
                    ball.change_move_x()

            elif ball.rect.left <= start_line or ball.rect.right >= SCREEN_WIDTH - start_line:
                # balls.pop(balls.index(ball))
                ball.change_move_x()


        # Teclas de Movimento
        output_key = pygame.key.get_pressed()

        if output_key[K_w]:
            p1.move_top()

        if output_key[K_s]:
            p1.move_down()

        if output_key[K_UP]:
            p2.move_top()

        if output_key[K_DOWN]:
            p2.move_down()


        map()
        pygame.display.update()


if __name__ == '__main__':
    main()
