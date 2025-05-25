
import pygame

class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imagenes = [
            pygame.transform.scale(pygame.image.load("assets/nave.png").convert_alpha(), (60, 40))
        ]
        self.index_imagen = 0
        self.image = self.imagenes[self.index_imagen]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.velocidad = 5

    def update(self, teclas, ancho_pantalla):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ancho_pantalla:
            self.rect.x += self.velocidad
