import random
import pygame
from enemigos import Enemigos

def cargar_nivel4(ANCHO, ALTO, fuente, imagenes_aliens):
    grupo_enemigos = pygame.sprite.Group()
    for fila in range(7):
        for columna in range(9):
            x = 50 + columna * 80
            y = 20 + fila * 55
            
            tipo_alien = random.choice([1, 2, 3, 4])  # Elegir tipo alien válido
            imagenes_para_enemigo = imagenes_aliens[tipo_alien]  # Obtener sus imágenes

            enemigo = Enemigos(x, y, imagenes_para_enemigo)
            grupo_enemigos.add(enemigo)

    velocidad_disparo = 23
    musica_nivel = "assets/sonidos/nivel_4.mp3"
    return grupo_enemigos, velocidad_disparo, musica_nivel
