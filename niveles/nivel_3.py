
import pygame
import random
from enemigos import Enemigos

def cargar_nivel3(ANCHO, ALTO, fuente, imagenes_aliens):
    grupo_enemigos = pygame.sprite.Group()
    for fila in range(6):
        for columna in range(8):
            x = 60 + columna * 85
            y = 30 + fila * 60
            
            tipo_alien = random.choice([1, 2, 3, 4])  # Elegir tipo alien válido
            imagenes_para_enemigo = imagenes_aliens[tipo_alien]  # Obtener sus imágenes

            enemigo = Enemigos(x, y, imagenes_para_enemigo)
            grupo_enemigos.add(enemigo)

    velocidad_disparo = 20
    musica_nivel = "assets/sonidos/nivel_3.mp3"

    return grupo_enemigos, velocidad_disparo, musica_nivel
