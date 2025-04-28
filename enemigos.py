import pygame

class Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen_path):
        super().__init__()
        self.image = pygame.image.load("assets/alien_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass  # por ahora no le vamos a poner movimiento. Eso va a ser para la próxima entrega.