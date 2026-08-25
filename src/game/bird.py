import pygame

class Bird():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.die = False
        self.gravity = 0.25
        self.jump_strength = -6
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def jump(self):
        self.velocity_y = self.jump_strength

    def update(self):
        if not self.die:
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            self.rect.center = (self.x, self.y)

    def check_floor_collision(self, floor_y):
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.die = True
            return True
        return False

    def check_collision(self, pillar):
        return self.rect.colliderect(pillar.rect_top) or self.rect.colliderect(pillar.rect_bottom)

    def draw(self, screen):
        screen.blit(self.image, self.rect)