import pygame
import math


class Vaccine(pygame.sprite.Sprite):
    def __init__(self, image, x, y, group, covid, direction, effect):
        super().__init__(group)
        self.image = image
        self.target_x = direction[0]
        self.target_y = direction[1]
        self.covid = covid
        self.effect = effect
        self.name = 'vaccine'
        self.rect = self.image.get_rect()
        self.start_x = x
        self.start_y = y
        self.rect = self.rect.move(x, y)
        self.vx = 0
        self.vy = 0
        self.find_speed()

    def update(self):  # Проверяем на столкновения
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, self.covid):
            for i in pygame.sprite.spritecollide(self, self.covid, False):
                i.wounded(self.effect)
            self.kill()

    def find_speed(self):  # Высчитываем скорость по x и по y и определяем наклон изображения
        if self.target_x - self.start_x + 0.01 > 0:
            tg = (self.target_y - self.start_y) / (self.target_x - self.start_x + 0.01)
            x = math.sqrt(100 / (tg ** 2 + 1))
            y = x * tg
            self.vx = x
            self.vy = y
            degr = math.degrees(math.acos(math.cos(self.vy / 10)))
            if -5 <= self.target_x - self.start_x <= 15 and self.target_y - self.start_y > 0:
                self.image = pygame.transform.rotate(self.image, -90)
            elif -5 <= self.target_x - self.start_x <= 15 and self.target_y - self.start_y <= 0:
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.target_y - self.start_y <= 0 and self.target_x - self.start_x > 0:
                self.image = pygame.transform.rotate(self.image, degr)
            elif self.target_y - self.start_y > 0 and self.target_x - self.start_x > 0:
                self.image = pygame.transform.rotate(self.image, -degr)
        else:
            tg = -(self.start_y - self.target_y) / (self.start_x - self.target_x)
            x = math.sqrt(100 / (tg ** 2 + 1))
            y = x * tg
            self.vx = -x
            self.vy = y
            degr = math.degrees(math.acos(math.cos(self.vy / 10)))
            if self.target_y - self.start_y <= 0 and self.target_x - self.start_x < 0:
                self.image = pygame.transform.rotate(self.image, -180 - degr)
            elif self.target_y - self.start_y > 0 and self.target_x - self.start_x < 0:
                self.image = pygame.transform.rotate(self.image, 180 + degr)
