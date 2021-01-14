import pygame
import os
import sys
import random
from doctor import Doctor
from Covid_class import Covid
from Vaccine import Vaccine
from Tile_class import Tile

pygame.init()
size = 700, 500
screen = pygame.display.set_mode(size)
color = pygame.Color((0, 0, 100))
running = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = pygame.sprite.Group()
clock = pygame.time.Clock()
covid_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
FPS = 70
pause = False
fullname = os.path.join('data', 'canon.mp3')
pygame.mixer.music.load(fullname)
pygame.mixer.music.play(-1)
#sound1 = pg.mixer.Sound('boom.wav')


def terminate():  # Выход из игры
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):  # Загружаем изображение
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_button():  # Прорисовка кнопки паузы
    color1 = pygame.Color('white')
    color2 = pygame.Color('black')
    pygame.draw.rect(screen, color1, (3, 3, 35, 35), 0)
    pygame.draw.rect(screen, color2, (13, 10, 4, 25), 0)
    pygame.draw.rect(screen, color2, (23, 10, 4, 25), 0)


def draw_new_game():   #Прорисовка кнопки новой игры
    color1 = pygame.Color('white')
    color2 = pygame.Color('black')
    pygame.draw.rect(screen, color1, (660, 3, 35, 35), 0)
    pygame.draw.circle(screen, color2, (677, 20), 18, 4)
    font = pygame.font.Font(None, 20)
    string_rendered = font.render('New', 1, pygame.Color('Black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 15
    intro_rect.x = 665
    screen.blit(string_rendered, intro_rect)


def start_screen():   # Заставка

    fon = pygame.transform.scale(load_image('covid1.jpg'), size)
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    pygame.time.delay(1000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

level_map = None


def load_level(filename):   # Загрузка уровня
    global level_map
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    level_map = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return level_map


tile_images = {
    'wall': load_image('box.png'),
    'ladder': pygame.transform.scale(load_image('ladder.png'), (20, 50)),
    'vaccine_box': pygame.transform.rotate(pygame.transform.scale(load_image('vaccine.png'), (10, 40)), 0)}

can_find_box = []


def generate_level(level):   # Генерация уровня
    global can_find_box
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                if y != 0 and x != 0 and x != len(level[y]):
                    can_find_box.append((x * 50, y * 50 - 20))
                Tile('wall', x, y, tile_group, all_sprites, tile_images)
            elif level[y][x] == '%':
                Tile('ladder', x, y, tile_group, all_sprites, tile_images)


generate_level(load_level('map.txt'))
go_left, go_right = False, False
image = pygame.transform.scale(load_image('covid3.png'), (50, 50))
bullet_image = load_image('vaccine.png')
bullet_image = pygame.transform.rotate(pygame.transform.scale(bullet_image, (10, 40)), -90)
doctor = Doctor(load_image('doctor.png'), 10, 10, 350, 400, player, all_sprites, tile_group, level_map)
covid = Covid(covid_group, all_sprites, image, doctor)
shout = False
ch = 0
go_n = 21
go_up = False
go_down = False
jump = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.WINDOWEXPOSED:   # Пауза при закртии окна
            pause = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if doctor.bullet > 0 and not (657 <= event.pos[0] <= 700 and 15 < event.pos[1] <= 50) \
                        and not (0 < event.pos[0] <= 35 and 0 < event.pos[1] <= 35):  #Стрельбы
                    shout = True
                    shout_n = 31
                    doctor.bullet -= 1
                    shout_pos = event.pos
            if 0 < event.pos[0] <= 35 and 0 < event.pos[1] <= 35:  # Нажатие на паузу
                pause = True
            if 657 <= event.pos[0] <= 700 and 15 < event.pos[1] <= 50:   # Новая игра
                for i in all_sprites:
                    if i.name == 'covid' or i.name == 'doctor' or i.name == 'vaccine_box':
                        i.kill()
                doctor = Doctor(load_image('doctor.png'), 10, 10, 350, 400, player, all_sprites, tile_group,
                                level_map)
                font = pygame.font.Font(None, 100)
                screen.fill(color)
                all_sprites.update()
                all_sprites.draw(screen)
                for i in range(3, 0, -1):
                    string_rendered = font.render(str(i), 1, pygame.Color('black'))
                    rect = string_rendered.get_rect()
                    rect.topleft = 300, 200
                    screen.blit(string_rendered, rect)
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    screen.fill(color)
                    all_sprites.draw(screen)
        if event.type == pygame.KEYUP:  # Движение героя
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                go_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                go_right = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                go_up = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                go_down = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                go_left = True
                go_n = 21
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                go_right = True
                go_n = 21
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                go_up = True
                go_n = 21
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                go_down = True
                go_n = 21
    if shout:   # Для анимации стрельбы
        doctor.shout(shout_n)
        shout_n += 1
        if shout_n == 39:
            vaccine = Vaccine(bullet_image, doctor.coords(1), doctor.coords(2), all_sprites, covid_group, shout_pos,
                              doctor.effect_vaccine)

        if shout_n == 41:
            shout = False
    if ch % 100 == 0:   # Создание новых вирусов
        covid = Covid(covid_group, all_sprites, image, doctor)
    screen.fill(color)
    if doctor.die:   # Анимация смерти
        sec = 40
        while doctor.die:
            clock.tick(10)
            doctor.die_n(sec)
            screen.fill(color)
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
            sec += 1
        clock.tick(FPS)
        start_screen()
        doctor.new_life()
        doctor.kill()
        for i in all_sprites:
            i.kill()
        generate_level(load_level('map.txt'))
        doctor = Doctor(load_image('doctor.png'), 10, 10, 350, 400, player, all_sprites, tile_group, level_map)
        shout = False
        go_n = 21
        go_up = False
        go_down = False
        jump = False
        go_left, go_right = False, False

    if ch % 3 == 0:   # Анимация ходьбы
        if go_left:
            if doctor.can_go(level_map, 'L'):
                doctor.rect = doctor.rect.move(-4, 0)
                doctor.go(go_n)
                go_n += 1
                if go_n == 31:
                    go_n = 21
        if go_right:
            if doctor.can_go(level_map, 'R'):
                doctor.rect = doctor.rect.move(4, 0)
                doctor.go(go_n)
                go_n += 1
                if go_n == 31:
                    go_n = 21
        if go_up:
            if doctor.can_go(level_map, 'U') and doctor.on_starway:
                doctor.rect = doctor.rect.move(0, -4)
                doctor.go(go_n)
                go_n += 1
                if go_n == 31:
                    go_n = 21
            elif doctor.can_go(level_map, 'U') and not doctor.on_starway:
                doctor.jump = True
            #    doctor.rect = doctor.rect.move(0, -40)
                go_up = False
        if doctor.jump:
            doctor.rect = doctor.rect.move(0, -10 + doctor.fall_n)
            doctor.fall_n += 1
        if go_down:
            if doctor.can_go(level_map, 'D'):
                doctor.rect = doctor.rect.move(0, 4)
                doctor.go(go_n)
                go_n += 1
                if go_n == 31:
                    go_n = 21
    if ch % 500 == 0:  # Шприц с патронами
        n = random.randint(1, len(can_find_box) - 1)
        Tile('vaccine_box', can_find_box[n], 0, tile_group, all_sprites, tile_images)
    if pause:   # Пауза
        intro_text = ["Пауза",
                      "Нажмите любую ",
                      "Кнопку, чтобы продолжить"]

        fon = pygame.transform.scale(load_image('covid4.jpg'), size)
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        r = True
        while r:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    r = False

            pygame.display.flip()
            clock.tick(FPS)
        font = pygame.font.Font(None, 100)
        screen.fill(color)
        all_sprites.update()
        all_sprites.draw(screen)
        for i in range(3, 0, -1):  #Обратный отсчет
            string_rendered = font.render(str(i), 1, pygame.Color('black'))
            rect = string_rendered.get_rect()
            rect.topleft = 300, 200
            screen.blit(string_rendered, rect)
            pygame.display.flip()
            pygame.time.delay(1000)
            screen.fill(color)
            all_sprites.draw(screen)
    pause = False
    all_sprites.update()
    all_sprites.draw(screen)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(f'Жизни {doctor.life}', 1, pygame.Color('White'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 10
    intro_rect.x = 80
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(f'Вакцины {doctor.bullet}', 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 10
    intro_rect.x = 500
    screen.blit(string_rendered, intro_rect)
    string_rendered = font.render(f'Эффективность {int(doctor.effect_vaccine * 100)}%', 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 10
    intro_rect.x = 200
    screen.blit(string_rendered, intro_rect)
    if doctor.effect_vaccine >= 1:
        о = True
        font = pygame.font.Font(None, 60)
        string_rendered = font.render('Победа!', 1, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 300
        intro_rect.top = 200
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        start_screen()
        for i in all_sprites:
            i.kill()
        generate_level(load_level('map.txt'))
        doctor = Doctor(load_image('doctor.png'), 10, 10, 350, 400, player, all_sprites, tile_group, level_map)
        shout = False
        go_n = 21
        go_up = False
        go_down = False
        jump = False
        go_left, go_right = False, False

    draw_button()
    draw_new_game()
    pygame.display.flip()
    clock.tick(FPS)
    ch += 1

terminate()
