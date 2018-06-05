from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.mouse import *


WINDOW_SIZE = 500
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
SHOT_HEIGHT = 14
SPACESHIP_WIDTH = 42
SHOT_WIDTH = 4
SPACESHIP_HEIGHT = 29
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40

BASE_SPEED = 100

ENEMY_START_X = 25
ENEMY_START_Y = 25
ENEMY_SPACING_X = 15
ENEMY_SPACING_Y = 15
BUTTON_BORDER = 30
BUTTON_SPACING = 20

ENEMY_LINES = 2
ENEMY_COLUMNS = 6

EASY = 1
MEDIUM = 2
HARD = 3
CURRENT_DIF = 2

total_time = 0
shot_time = CURRENT_DIF * 0.1
last_shot_time = 0
last_enemy_move = 0

LEFT = -1
RIGHT = 1
UP = -1
DOWN = 1

mouse = Mouse()
keyboard = Keyboard()

def menu():
    menu_window = Window(WINDOW_SIZE, WINDOW_SIZE)
    menu_window.set_title("Space Invaders!")
    bg = GameImage("img/bg.png")
    botao_jogar = Sprite("img/menu_jogar.png")
    botao_dificuldade = Sprite("img/menu_dificuldade.png")
    botao_ranking = Sprite("img/menu_ranking.png")
    botao_sair = Sprite("img/menu_sair.png")

    botao_jogar.set_position(150, 120)
    botao_dificuldade.set_position(150, 190)
    botao_ranking.set_position(150, 256)
    botao_sair.set_position(150, 328)

    CURRENT_DIF = 2
    
    while True:
        if mouse.is_over_object(botao_jogar) and mouse.is_button_pressed(1):
            game(CURRENT_DIF)

        elif mouse.is_over_object(botao_dificuldade) and mouse.is_button_pressed(1):
            CURRENT_DIF = dificuldade()
            print("DIFICULDADE: " + str(CURRENT_DIF))

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


def dificuldade():
    dif_window = Window(WINDOW_SIZE, WINDOW_SIZE)
    dif_window.set_title("Space Invaders!")
    background = GameImage("img/bg.png")

    while True:
        if keyboard.key_pressed("1"):
            return EASY

        if keyboard.key_pressed("2"):
            return MEDIUM

        if keyboard.key_pressed("3"):
            return HARD

        background.draw()
        dif_window.update()


def init_enemies(lines, columns):
    if lines > 5: lines = 5
    if columns > 8: columns = 8

    enemies = []

    for i in range(lines):
        line = []
        for j in range(columns):
            enemy = Sprite("img/enemy.png")

            enemy.set_position(ENEMY_START_X + j * (ENEMY_WIDTH + ENEMY_SPACING_X),
                               ENEMY_START_Y + i * (ENEMY_HEIGHT + ENEMY_SPACING_Y))
            line.append(enemy)
        enemies.append(line)

    return enemies

def draw_enemies(enemies):
     for line in enemies:
            for enemy in line:
                if enemy is not None:
                    enemy.draw()


def move_enemies(enemies, enemy_dir_x, enemy_dir_y):
    enemy_step_x = ENEMY_WIDTH + ENEMY_SPACING_X
    enemy_step_y = ENEMY_HEIGHT + ENEMY_SPACING_Y

    if (((enemies[0][len(enemies[0]) - 1].x + ENEMY_WIDTH) + (enemy_step_x * enemy_dir_x) >= WINDOW_SIZE - ENEMY_START_X)
        or (enemies[0][0].x + (enemy_step_x * enemy_dir_x) < ENEMY_START_X)):
        for line in enemies:
            for enemy in line:
                enemy.set_position(enemy.x, enemy.y + enemy_step_y * enemy_dir_y)
        enemy_dir_x = 0 - enemy_dir_x
    else:
        for line in enemies:
            for enemy in line:
                enemy.set_position(enemy.x + enemy_step_x * enemy_dir_x, enemy.y)

    return enemy_dir_x, enemy_dir_y

def game(CURRENT_DIF):
    game_window = Window(WINDOW_SIZE, WINDOW_SIZE)
    game_window.set_title("Space Invaders!")

    background = GameImage("img/bg.png")
    spaceship = Sprite("img/spaceship.png")

    spaceship.set_position(WINDOW_SIZE / 2 - SPACESHIP_WIDTH / 2, WINDOW_SIZE - SPACESHIP_HEIGHT)

    spaceship_speed = 2 * BASE_SPEED
    shots = []
    shot_speed = 4 * BASE_SPEED

    enemies = init_enemies(ENEMY_LINES, ENEMY_COLUMNS)

    enemy_speed = 1.5
    enemy_dir_x = RIGHT
    enemy_dir_y = DOWN

    total_time = 0
    last_shot_time = game_window.delta_time()
    last_enemy_move = game_window.delta_time()

    while True:
        # spaceship movements
        if keyboard.key_pressed("RIGHT"):
            if spaceship.x + SPACESHIP_WIDTH <= WINDOW_SIZE:
                spaceship.set_position(spaceship.x + spaceship_speed * delta_time, spaceship.y)

        elif keyboard.key_pressed("LEFT"):
            if spaceship.x >= 0:
                spaceship.set_position(spaceship.x - spaceship_speed * delta_time, spaceship.y)

        if keyboard.key_pressed("SPACE"):
            if total_time - last_shot_time >= shot_time:
                new_shot = Sprite("img/shot.png")
                new_shot.set_position(spaceship.x + SPACESHIP_WIDTH / 2, spaceship.y - SHOT_HEIGHT)
                shots.append(new_shot)
                last_shot_time = total_time

        elif keyboard.key_pressed("Q"):
            menu()

        elif keyboard.key_pressed("ESC"):
            game_window.close()
            return

        # update shot positions
        for shot in shots:
            shot.set_position(shot.x, shot.y - shot_speed * delta_time)

            if shot.y <= - SHOT_HEIGHT:
                shots.remove(shot)

        # update enemy positions
        if total_time - last_enemy_move > enemy_speed:
            enemy_dir_x, enemy_dir_y = move_enemies(enemies, enemy_dir_x, enemy_dir_y)
            last_enemy_move = total_time


        background.draw()
        spaceship.draw()

        for shot in shots:
            shot.draw()
 
        draw_enemies(enemies)
        game_window.update()

        delta_time = game_window.delta_time()
        total_time += delta_time


menu()
