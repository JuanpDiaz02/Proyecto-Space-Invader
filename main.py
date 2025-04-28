import pygame
import sys
import random
from enemigos import Enemigos


# Inicializar Pygame
pygame.init()

# Tamaño de pantalla de juego
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader 🚀")

# Colores
NEGRO = (0, 0, 0) #Fondo pantalla
BLANCO = (255, 255, 255) #Bala de la nave

# Nave
nave_img = pygame.Surface((50, 10)) # Cambia el tamaño del jugador
nave_img.fill((0, 255, 0))
posicion_nave_x = ANCHO // 2
posicion_nave_y = ALTO - 10
velocidad_nave = 5

# Lista de disparos en eje y
posiciones_disparos = []
velocidad_disparo = 15
grupo_enemigos = pygame.sprite.Group()

imagenes_aliens = [
    "assets/alien_1.png",
    "assets/alien_2.png",
    "assets/alien_3.png",
    "assets/alien_4.png"
] 

# Acá lo que hacemos basicamente es una lista y bucles para crear a los enemigos en forma de matriz
for fila in range(4):  # Con 4 filas
    for columna in range(6):  #Y 6 enemigos por fila
        x = 100 + columna * 100
        y = 50 + fila * 70
        imagen_aleatoria = random.choice(imagenes_aliens)  # Elige una imagen al azar
        enemigo = Enemigos(x, y, imagen_aleatoria)
        grupo_enemigos.add(enemigo)

# Bucle principal
reloj = pygame.time.Clock()
movimiento_lateral = True

while movimiento_lateral:
    reloj.tick(60)  # 60 FPS

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            movimiento_lateral = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Crear disparo
                posiciones_disparos.append(pygame.Rect(posicion_nave_x + 25, posicion_nave_y, 5, 15)) # Cambia el tamaño del disparo

        
    # Teclas para mover la nave
    teclas_movimiento = pygame.key.get_pressed()
    if teclas_movimiento[pygame.K_LEFT] and posicion_nave_x > 0:
        posicion_nave_x -= velocidad_nave
    if teclas_movimiento[pygame.K_RIGHT] and posicion_nave_x < ANCHO - 50:
        posicion_nave_x += velocidad_nave
                
    # Mover los disparos hacia arriba 
    for disparo in posiciones_disparos:
        disparo.y -= velocidad_disparo

    # Eliminar disparos que salieron de la pantalla
    posiciones_disparos = list(filter(lambda d: d.y > 0, posiciones_disparos))

    # Dibujar fondo, jugador y disparos de nave
    pantalla.fill(NEGRO)
    pantalla.blit(nave_img, (posicion_nave_x, posicion_nave_y))
    grupo_enemigos.update()
    grupo_enemigos.draw(pantalla)
    for disparo in posiciones_disparos:
        pygame.draw.rect(pantalla, BLANCO, disparo)
    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()

#revision y control que se apliquen todos los los conceptos aprendido en clases 
#matrices lo podemos usar en los puntajes del jugador pero todavia no "sabemos" archivos x eso no lo usamos.
#se hacer archivos(nacho) pero eso no podria aplicarlo ahora xq eso entraria en lo q es el 100% del juego.