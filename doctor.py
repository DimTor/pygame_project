import pygame


class Doctor(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group, group2, group3, level_map):
        super().__init__(group, group2)
        self.group = group3
        self.frames = []
        self.level_map = level_map
        self.on_starway = False
        self.bullet = 30
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.life = 3
        self.speed_covid = 5
        self.virus_kill = 0
        self.effect_vaccine = 0.7
        self.die = False
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (50, 50))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.fall_n = 1
        self.jump = False
        self.fall = True
        self.name = 'doctor'

    def cut_sheet(self, sheet, columns, rows):   # Для анимации спрайта
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def shout(self, n):   # Для анимации стрельбы
        self.image = self.frames[n]
        self.image = pygame.transform.scale(self.image, (50, 50))

    def go(self, n):  # Для анимации ходьбы
        self.image = self.frames[n]
        self.image = pygame.transform.scale(self.image, (50, 50))

    def coords(self, r):   # Возвращение своих координат
        if r == 1:
            return self.rect.x + 25
        if r == 2:
            return self.rect.y + 20

    def can_go(self, level_map, direction=None):  # Проверка перед передвижением
        width = 700
        tile_width = 1
        tile_height = 1
        height = 500
        if direction:
            if direction == 'L' and 45 <= self.rect.move(-tile_width, 0).left\
                    and self.level_map[self.rect.move(0, 0).y // 50][self.rect.move(0, 0).x // 50] \
                    not in ('#'):
                return True
            elif direction == 'R' and self.rect.move(tile_width, 0).left <= width - 100:
                return True
            elif direction == 'U' and 40 <= self.rect.move(0, -tile_height).y:
                return True
            elif direction == 'D' and self.rect.move(0, tile_height).y <= height - 100 and self.on_starway:
                return True
        else:
            return False

    def kill_covid(self):   # Для повышения эффективности
        self.virus_kill += 1
        if self.virus_kill == 5:
            if self.effect_vaccine <= 1:
                self.effect_vaccine += 0.05
                self.speed_covid += 1
                self.virus_kill = 0

    def attack(self):   # При столкновении с вирусом
        self.life -= 1
        self.virus_kill == 0
        if self.life == 0:
            self.die = True

    def die_n(self, i):   # Анимация смерти
        self.image = self.frames[i]
        self.image = pygame.transform.scale(self.image, (50, 50))
        if i == 49:
            pygame.time.delay(500)
            self.die = False

    def update(self):   # еремещения и столкновения
        if pygame.sprite.spritecollideany(self, self.group):
            z = []
            for i in pygame.sprite.spritecollide(self, self.group, False):
                z.append(i.tile_type)
            if 'ladder' in z:
                self.on_starway = True
                self.fall = False
                self.jump = False
                self.fall_n = 1
            elif 'wall' in z and 40 < self.rect.y < 450 and\
                    self.level_map[self.rect.move(0, -25).y // 50][self.rect.x // 50 + 1] in ('#'):
                self.fall = True
                self.jump = False
                self.fall_n = 1
            elif 'wall' in z and 40 < self.rect.y < 450 and\
                    self.level_map[self.rect.move(0, 0).y // 50 + 1][self.rect.x // 50 + 1] in ('#', '%'):
                self.fall = False
                self.jump = False
                self.fall_n = 1
            else:
                self.on_starway = False
                self.fall = True
                self.fall_n = 1
        else:
            self.on_starway = False
            self.fall = True
        if self.fall and self.rect.y <= 400 and not self.jump:
            self.fall_n += 0.1
            self.rect = self.rect.move(0, self.fall_n)
        if pygame.sprite.spritecollideany(self, self.group):
            for i in pygame.sprite.spritecollide(self, self.group, False):
                if i.name == 'vaccine_box':
                    i.kill()
                    self.bullet += 30

    def new_life(self):   # Для начала новой игры
        self.on_starway = False
        self.cur_frame = 0
        self.life = 3
        self.die = False
        self.fall_n = 1
        self.jump = False
        self.fall = True
        self.name = 'doctor'

