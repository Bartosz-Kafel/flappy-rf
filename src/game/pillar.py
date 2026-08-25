import pygame, random

class Pillar():
    def __init__(self, x, image, image_body):
        self.x = x
        self.passage_y = random.randint(128, 384)
        self.gap_size = 128
        self.image_bottom = image
        self.image_body_bottom = image_body

        self.image_top = pygame.transform.flip(image, False, True)
        self.image_body_top = pygame.transform.flip(image_body, False, True)

        self.image_height = self.image_bottom.get_height()

        self.rect_top = self.image_top.get_rect(
            bottomleft=(self.x, self.passage_y - self.gap_size // 2)
        )
        self.rect_bottom = self.image_bottom.get_rect(
            topleft=(self.x, self.passage_y + self.gap_size // 2)
        )

    def draw(self, screen):
        screen.blit(self.image_top, self.rect_top)
        screen.blit(self.image_bottom, self.rect_bottom)

        body_height = self.image_body_top.get_height()

        for i in range(3):
            segment_y = self.rect_top.top - (i + 1) * body_height
            screen.blit(self.image_body_top, (self.x, segment_y))

        for i in range(3):
            segment_y = self.rect_bottom.bottom + i * body_height
            screen.blit(self.image_body_bottom, (self.x, segment_y))

    def update(self, speed=2):
        self.x -= speed
        self.rect_top.x = self.x
        self.rect_bottom.x = self.x

    def check_erase(self):
        if self.x + self.image_bottom.get_width() < 0:
            return True
        return False