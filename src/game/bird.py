import pygame

class Bird():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.die = False
        self.gravity = 0.25
        self.action = 0
        self.jump_strength = -6
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect = self.rect.inflate(-self.rect.width * 0.2, -self.rect.height * 0.2) 

    def jump(self):
        self.velocity_y = self.jump_strength

    def update(self):
        if self.action == 1:
            self.jump()

        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.rect.center = (self.x, self.y)

    def check_floor_collision(self, floor_y):
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.die = True
            return True
        return False

    def check_collision(self, sprite):
        return self.rect.colliderect(sprite.rect_top) or self.rect.colliderect(sprite.rect_bottom)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.velocity_y * 5)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect)