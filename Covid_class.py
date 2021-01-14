import pygame
import random
import math


class Covid(pygame.sprite.Sprite):
    def __init__(self, group, group2, image, target):
        super().__init__(group, group2)
        self.image = image
        self.enemy = target
        self.speed = target.speed_covid
        self.target_x = 0
        self.name = 'covid'
        self.target_y = 0
        self.live = 3
        x, y = None, None
        self.group2 = group2
        self.rect = self.image.get_rect()
        field_x1 = (50, target.rect.x - 150)
        field_x2 = (target.rect.x + 150, 650)
        field_y1 = (50, target.rect.y - 150)
        field_y2 = (target.rect.y + 150, 450)
        if target.rect.x - 150 < 50:
            x = random.randint(field_x2[0], field_x2[1])
        elif target.rect.x + 150 > 650:
            x = random.randint(field_x1[0], field_x1[1])
        if target.rect.y - 150 < 50:
            y = random.randint(field_y2[0], field_y2[1])
        elif target.rect.y + 150 > 450:
            y = random.randint(field_y1[0], field_y1[1])
        if not x:
            if random.randint(0, 1):
                x = random.randint(field_x1[0], field_x1[1])
            else:
                x = random.randint(field_x2[0], field_x2[1])
        if not y:
            if random.randint(0, 1):
                y = random.randint(field_y2[0], field_y2[1])
            else:
                y = random.randint(field_y1[0], field_y1[1])
        self.rect.topleft = (x, y)
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.vx = 0
        self.vy = 0

    def update(self):   # Высчитываем скорость
        self.target_x = self.enemy.rect.x
        self.target_y = self.enemy.rect.y
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        if self.target_x - self.start_x + 0.01 > 0:
            tg = (self.target_y - self.start_y) / (self.target_x - self.start_x + 0.01)
            x = math.sqrt(self.speed / (tg ** 2 + 1))
            y = x * tg
            self.vx = x
            self.vy = y
        else:
            tg = -(self.start_y - self.target_y) / (self.start_x - self.target_x)
            x = math.sqrt(self.speed / (tg ** 2 + 1))
            y = x * tg
            self.vx = -x
            self.vy = y
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, self.group2):
            for i in pygame.sprite.spritecollide(self, self.group2, False):
                if i.name == 'doctor':
                    self.enemy.attack()
                    self.kill()
        if pygame.sprite.spritecollideany(self, self.group2):   # Замедление при столкновении с tile
            for i in pygame.sprite.spritecollide(self, self.group2, False):
                if i.name == 'wall' or i.name == 'ladder':
                    self.speed = 3

    def wounded(self, effect):   # Поражение вакциной
        self.live -= effect
        if self.live <= 0:
            self.enemy.kill_covid()
            self.kill()
