from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.mouse import *


WINDOW_SIZE = 500
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
SHOT_WIDTH = 4
SHOT_HEIGHT = 14
SPACESHIP_WIDTH = 42
SPACESHIP_HEIGHT = 29
ENEMY_WIDTH = 25
ENEMY_HEIGHT = 25

BASE_SPEED = 100

ENEMY_START_X = 50
ENEMY_START_Y = 25
ENEMY_SPACING_X = 40
ENEMY_SPACING_Y = 40
BUTTON_BORDER = 30
BUTTON_SPACING = 20

mouse = Mouse()
keyboard = Keyboard()

def menu():
    menu_window = Window(WINDOW_SIZE, WINDOW_SIZE)
    bg = GameImage("img/bg.png")
    botao_jogar = Sprite("img/menu_jogar.png")
    botao_dificuldade = Sprite("img/menu_dificuldade.png")
    botao_ranking = Sprite("img/menu_ranking.png")
    botao_sair = Sprite("img/menu_sair.png")

    botao_jogar.set_position(150, 120)
    botao_dificuldade.set_position(150, 190)
    botao_ranking.set_position(150, 256)
    botao_sair.set_position(150, 328)
    
    while True:
        if mouse.is_over_object(botao_jogar) and mouse.is_button_pressed(1):
            game()

        elif mouse.is_over_object(botao_dificuldade) and mouse.is_button_pressed(1):
            print("DIFICULDADE")

        elif mouse.is_over_object(botao_ranking) and mouse.is_button_pressed(1):
            print("RANKING")

        elif (mouse.is_over_object(botao_sair) and mouse.is_button_pressed(1)) or keyboard.key_pressed("ESC"):
            janela.close()
            return

        bg.draw()
        botao_jogar.draw()
        botao_dificuldade.draw()
        botao_ranking.draw()
        botao_sair.draw()
        menu_window.update()


def game():
    game_window = Window(WINDOW_SIZE, WINDOW_SIZE)
    game_window.set_title("Space Invaders!")

    background = GameImage("img/bg.png")
    spaceship = Sprite("img/spaceship.png")

    spaceship.set_position(WINDOW_SIZE / 2 - SPACESHIP_WIDTH / 2, WINDOW_SIZE - SPACESHIP_HEIGHT)

    spaceship_speed = 2 * BASE_SPEED
    shot_speed = 3 * BASE_SPEED

    shots = []

    enemies = []
    for i in range(2):
        line = []
        for j in range(5):
            enemy = Sprite("img/enemy.png")
            enemy.set_position(ENEMY_START_X + j * (ENEMY_WIDTH + ENEMY_SPACING_X),
                               ENEMY_START_Y + i * (ENEMY_HEIGHT + ENEMY_SPACING_Y))
            line.append(enemy)
        enemies.append(line)

    enemy_speed = 0.3 * BASE_SPEED
    enemy_move_x = 1
    enemy_move_y = 0
    enemy_n_of_moves_x = 0
    enemy_n_of_moves_y = 0

    total_time = 0
    last_shot_time = game_window.delta_time()
    last_enemy_move = game_window.delta_time()

    while True:
        delta_time = game_window.delta_time()
        total_time += delta_time

        # spaceship movements
        if keyboard.key_pressed("RIGHT"):
            if spaceship.x + SPACESHIP_WIDTH <= WINDOW_SIZE:
                spaceship.set_position(spaceship.x + spaceship_speed * delta_time, spaceship.y)
        elif keyboard.key_pressed("LEFT"):
            if spaceship.x >= 0:
                spaceship.set_position(spaceship.x - spaceship_speed * delta_time, spaceship.y)
        if keyboard.key_pressed("SPACE"):
            if total_time - last_shot_time >= 0.1:
                new_shot = Sprite("img/shot.png")
                new_shot.set_position(spaceship.x + SPACESHIP_WIDTH / 2, spaceship.y - SHOT_HEIGHT)
                shots.append(new_shot)
                last_shot_time = total_time

        elif keyboard.key_pressed("Q"):
            menu()

        elif keyboard.key_pressed("ESC"):
            return

        # update shot positions
        for shot in shots:
            shot.set_position(shot.x, shot.y - shot_speed * delta_time)
            if shot.y <= 0 - SHOT_HEIGHT:
                shots.remove(shot)

        # update enemy positions
        if total_time - last_enemy_move > 1:
            if enemy_n_of_moves_x > 5:
                enemy_n_of_moves_x = 0
                enemy_move_x = 0
                enemy_move_y = 1

            if enemy_n_of_moves_y > 0:
                enemy_speed = 0 - enemy_speed
                enemy_n_of_moves_y = 0
                enemy_move_x = 1
                enemy_move_y = 0

            if enemy_move_x == 1:
                enemy_n_of_moves_x += 1

            if enemy_move_y == 1:
                enemy_n_of_moves_y += 1

            for line in enemies:
                for enemy in line:
                    enemy.set_position(enemy.x + (enemy_speed * enemy_move_x), enemy.y + (enemy_speed * enemy_move_y))
            
            last_enemy_move = total_time

        background.draw()
        spaceship.draw()

        for shot in shots:
            shot.draw()

        """
        for line in enemies:
            for enemy in line:
                if enemy is not None:
                    enemy.draw()
        """
        
        game_window.update()


menu()