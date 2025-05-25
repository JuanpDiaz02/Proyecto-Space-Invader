import random
import pygame
from enemigos import Enemigos

def cargar_nivel5(ANCHO, ALTO, fuente, imagenes_aliens):
    grupo_enemigos = pygame.sprite.Group()
    for fila in range(8):
        for columna in range(10):
            x = 40 + columna * 75
            y = 10 + fila * 50
        
            tipo_alien = random.choice([1, 2, 3, 4])  # Elegir tipo alien válido
            imagenes_para_enemigo = imagenes_aliens[tipo_alien]  # Obtener sus imágenes

            enemigo = Enemigos(x, y, imagenes_para_enemigo)
            grupo_enemigos.add(enemigo)

    velocidad_disparo = 26
    musica_nivel = "assets/sonidos/nivel_5.mp3"
    return grupo_enemigos, velocidad_disparo, musica_nivel
