import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, group1, group2, image):
        super().__init__(group1, group2)
        if tile_type != 'vaccine_box':
            self.tile_type = tile_type
            self.name = tile_type
            self.image = image[tile_type]
            self.rect = self.image.get_rect().move(
                50 * pos_x, 50 * pos_y)
        else:
            self.tile_type = tile_type
            self.name = tile_type
            self.image = image[tile_type]
            self.rect = self.image.get_rect().move(
                pos_x[0], pos_x[1])