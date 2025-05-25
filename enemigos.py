import pygame

class Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y, image_paths, pantalla_ancho=800):
        super().__init__()
        if isinstance(image_paths, str):
            image_paths = [image_paths]

        # Cargar y escalar todas las imágenes proporcionadas
        self.imagenes = [
            pygame.transform.scale(pygame.image.load(path).convert_alpha(), (50, 50))
            for path in image_paths
        ]
        
        self.index_imagen = 0
        self.image = self.imagenes[self.index_imagen]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocidad_x = 1
        self.velocidad_y = 10
        self.contador_animacion = 0
        self.frecuencia_animacion = 20
        self.pantalla_ancho = pantalla_ancho

        # Lambda que verifica si está dentro del área visible
        self.esta_en_pantalla = lambda x: 0 <= x <= (self.pantalla_ancho - self.rect.width)

    def update(self):
        # Movimiento horizontal
        self.rect.x += self.velocidad_x

        # Si se sale de los límites, cambia de dirección y baja
        if not self.esta_en_pantalla(self.rect.x):
            self.velocidad_x *= -1
            self.rect.y += self.velocidad_y
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > self.pantalla_ancho - self.rect.width:
                self.rect.x = self.pantalla_ancho - self.rect.width

        # Animación de cambio de frame
        self.contador_animacion += 1
        if self.contador_animacion >= self.frecuencia_animacion:
            self.contador_animacion = 0
            self.index_imagen = (self.index_imagen + 1) % len(self.imagenes)
            self.image = self.imagenes[self.index_imagen]

    def disparar(self):
        """
        Retorna un pygame.Rect que representa el disparo del enemigo,
        posicionado justo en el centro bajo el enemigo.
        """
        disparo_rect = pygame.Rect(self.rect.centerx - 2, self.rect.bottom, 5, 15)
        return disparo_rect
