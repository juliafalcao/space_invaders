from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.collision import *
import random


WINDOW_SIZE = 500
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
SHOT_HEIGHT = 14
SPACESHIP_WIDTH = 42
SHOT_WIDTH = 4
SPACESHIP_HEIGHT = 29
ENEMY_WIDTH = 35
ENEMY_HEIGHT = 28

BASE_SPEED = 100

ENEMY_START_X = 25
ENEMY_START_Y = 25
ENEMY_SPACING_X = 15
ENEMY_SPACING_Y = 15
BUTTON_BORDER = 30
BUTTON_SPACING = 20

global ENEMY_LINES
ENEMY_LINES = 3
global ENEMY_COLUMNS
ENEMY_COLUMNS = 6

EASY = 1
MEDIUM = 2
HARD = 3
global CURRENT_DIF
CURRENT_DIF = 2

global LIVES
LIVES = 3
CURRENT_SCORE = 0

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
            game(CURRENT_DIF, CURRENT_SCORE)

        elif mouse.is_over_object(botao_dificuldade) and mouse.is_button_pressed(1):
            CURRENT_DIF = dificuldade()
            print("DIFICULDADE: " + str(CURRENT_DIF))

        elif mouse.is_over_object(botao_ranking) and mouse.is_button_pressed(1):
            print("RANKING")

        elif (mouse.is_over_object(botao_sair) and mouse.is_button_pressed(1)) or keyboard.key_pressed("ESC"):
            menu_window.close()
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
            enemy = Sprite("img/enemy2.png")

            enemy.set_position(ENEMY_START_X + j * (ENEMY_WIDTH + ENEMY_SPACING_X),
                               ENEMY_START_Y + i * (ENEMY_HEIGHT + ENEMY_SPACING_Y))
            line.append(enemy)
        enemies.append(line)

    return enemies

def draw_enemies(enemies):
    dead = 0

    for line in enemies:
        for enemy in line:
            if enemy is None:
                dead += 1
            else:
                enemy.draw()

    return not dead == len(enemies) * len(enemies[0]) # return whether all enemies are dead

def move_enemies(enemies, enemy_dir_x, enemy_dir_y):
    enemy_step_x = ENEMY_WIDTH + ENEMY_SPACING_X
    enemy_step_y = ENEMY_HEIGHT + ENEMY_SPACING_Y

    if (enemies[0][len(enemies[0]) - 1] is not None and ((enemies[0][len(enemies[0]) - 1].x + ENEMY_WIDTH) + (enemy_step_x * enemy_dir_x) >= WINDOW_SIZE - ENEMY_START_X)
        or (enemies[0][0] is not None and enemies[0][0].x + (enemy_step_x * enemy_dir_x) < ENEMY_START_X)):
        for line in enemies: 
            for enemy in line:
                if enemy is not None:
                    enemy.set_position(enemy.x, enemy.y + enemy_step_y * enemy_dir_y)
        enemy_dir_x = 0 - enemy_dir_x
    else:
        for line in enemies:
            for enemy in line:
                if enemy is not None:
                    enemy.set_position(enemy.x + enemy_step_x * enemy_dir_x, enemy.y)

    return enemy_dir_x, enemy_dir_y

def game(dif = CURRENT_DIF, enemy_lines = ENEMY_LINES, enemy_columns = ENEMY_COLUMNS, score = CURRENT_SCORE):
    game_window = Window(WINDOW_SIZE, WINDOW_SIZE)
    game_window.set_title("Space Invaders!")

    background = GameImage("img/bg.png")
    spaceship = Sprite("img/spaceship.png")

    spaceship.set_position(WINDOW_SIZE / 2 - SPACESHIP_WIDTH / 2, WINDOW_SIZE - SPACESHIP_HEIGHT)

    spaceship_speed = 2 * BASE_SPEED
    shots = []
    enemy_shots = []
    shot_speed = 4 * BASE_SPEED

    super_shot_time = 1
    shot_charging = False
    current_charging_time = 0
    charging_time = 1.5

    lives = 3

    enemies = init_enemies(ENEMY_LINES, ENEMY_COLUMNS)

    if enemies is None:
        return
        
    enemy_speed = 1.5
    enemy_dir_x = RIGHT
    enemy_dir_y = DOWN

    total_time = 0
    last_shot_time = 0
    last_enemy_move = 0
    last_enemy_shot = 0
    enemy_shot_cooldown = 1

    while True:
        # spaceship movements
        if keyboard.key_pressed("RIGHT"):
            if spaceship.x + SPACESHIP_WIDTH <= WINDOW_SIZE:
                spaceship.set_position(spaceship.x + spaceship_speed * delta_time, spaceship.y)

        elif keyboard.key_pressed("LEFT"):
            if spaceship.x >= 0:
                spaceship.set_position(spaceship.x - spaceship_speed * delta_time, spaceship.y)

        if keyboard.key_pressed("SPACE"):
            shot_charging = True
            current_charging_time += delta_time

        elif shot_charging:
            if total_time - last_shot_time >= super_shot_time and current_charging_time > charging_time:
                new_shot = Shot(spaceship.x, spaceship.y, True)
                shots.append(new_shot)
                last_shot_time = total_time
            elif total_time - last_shot_time >= shot_time:
                new_shot = Shot(spaceship.x, spaceship.y, False)
                shots.append(new_shot)
                last_shot_time = total_time
            shot_charging = False
            current_charging_time = 0

        elif keyboard.key_pressed("Q"):
            menu()

        elif keyboard.key_pressed("ESC"):
            game_window.close()
            return

        # update enemy positions
        if total_time - last_enemy_move > enemy_speed:
            enemy_dir_x, enemy_dir_y = move_enemies(enemies, enemy_dir_x, enemy_dir_y)
            last_enemy_move = total_time

        # update shot positions
        for shot in shots:
            shot.set_position(shot.x, shot.y - shot_speed * delta_time)

            if shot.y <= - SHOT_HEIGHT:
                shots.remove(shot)

        # enemy shots
        if total_time - last_enemy_shot > enemy_shot_cooldown:
            total = 0 # alive enemies

            for i in range(len(enemies)):
                for j in range(len(enemies[0])):
                    if enemies[i][j] is not None:
                        total += 1

            chosen = random.randint(0, total)
            it = 0

            for i in range(len(enemies)):
                for j in range(len(enemies[0])):
                    if enemies[i][j] is not None:
                        if it == chosen:
                            new_shot = Sprite("img/shot.png")
                            new_shot.set_position(enemies[i][j].x + ENEMY_WIDTH / 2, enemies[i][j].y)
                            enemy_shots.append(new_shot)
                        it += 1

            last_enemy_shot = total_time

        # updates monsters shots positions
        for shot in enemy_shots:
            shot.set_position(shot.x, shot.y + shot_speed * delta_time)

            if shot.y <= 0 - SHOT_HEIGHT:
                shots.remove(shot)

        # check for enemy and spaceship shot collisions
        for shot in shots:
            for i in range(len(enemies)):
                for j in range(len(enemies[0])):
                    if enemies[i][j] is not None: # enemy still alive

                        if Collision.collided(shot.sprite, enemies[i][j]):
                            enemies[i][j] = None # now it's dead
                            global CURRENT_SCORE
                            CURRENT_SCORE += 10

                            if (not shot.loaded):
                                shots.remove(shot) # stop shooting


        # check for spaceship and enemy shot collisions
        for shot in enemy_shots:
            if Collision.collided(shot, spaceship):
                lives -= 1
                enemy_shots.remove(shot)


        # check if game over
        all_enemies_dead = True

        for line in enemies:
            for enemy in line:
                if enemy is not None:
                    all_enemies_dead = False


        if all_enemies_dead:
            print("VITÓRIA!")
            print("Agora a dificuldade é: ", end = "")
            global CURRENT_DIF

            if CURRENT_DIF == 1:
                print("EASY")

            if CURRENT_DIF == 2:
                print("MEDIUM")

            for i in range(3, CURRENT_DIF):
                print("MUITO", end = " ")

            if CURRENT_DIF >= 3:
                print("HARD")

            game(CURRENT_DIF + 1, CURRENT_SCORE)
            return

        if lives == 0:
            print("GAME OVER")
            return

        background.draw()
        spaceship.draw()

        for shot in shots:
            shot.draw()
 
        r = draw_enemies(enemies)

        if not r:

            CURRENT_DIF += 1
            game(CURRENT_DIF)

        game_window.draw_text(str(CURRENT_SCORE), WINDOW_SIZE - 30, 10, size = 25, color = (255, 255, 255), font_name="Consolas", bold=True)
        game_window.update()

        delta_time = game_window.delta_time()
        total_time += delta_time

class Shot:
    def __init__(self, s_pos_x, s_pos_y, loaded):
        self.x = s_pos_x + SPACESHIP_WIDTH / 2
        self.y = s_pos_y - SHOT_HEIGHT

        self.loaded = loaded
        if loaded:
            self.sprite = Sprite("img/sshot.png")
            self.x = s_pos_x + SPACESHIP_WIDTH / 2 - 5
            self.y = s_pos_y - SHOT_WIDTH
        else:
            self.sprite = Sprite("img/shot.png")
            self.x = s_pos_x + SPACESHIP_WIDTH / 2
            self.y = s_pos_y - SHOT_HEIGHT
        self.sprite.set_position(self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.sprite.set_position(x, y)

    def draw(self):
        self.sprite.draw()

menu()
