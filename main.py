import pygame
import sys
import random
import importlib
import os
from pantalla_inicio import pantalla_inicio
from pantalla_gameover import mostrar_pantalla_gameover
from sonidos import (
    reproducir_sonido_disparo,
    reproducir_sonido_colision,
    reproducir_sonido_gameover,
    reproducir_sonido_inicio,
    iniciar_musica_fondo,
    detener_musica_fondo,
    reproducir_sonido_victoria
)
from nave import Nave

pygame.init()

ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invader 🚀")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

fuente = pygame.font.Font("assets/fuentes/PressStart2P.ttf", 20)

def mostrar_texto_nivel(nivel):
    texto_nivel = fuente.render(f"Nivel {nivel}", True, BLANCO)
    pantalla.fill(NEGRO)
    pantalla.blit(texto_nivel, (ANCHO // 2 - texto_nivel.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def cargar_imagenes_aliens():
    alien_imagenes = {}
    for i in range(1, 5):
        imagenes = []
        base_path = f"assets/aliens/alien_{i}.png"
        frame_2 = f"assets/aliens/alien_{i}_frame_2.png"
        frame_3 = f"assets/aliens/alien_{i}_frame_3.png"
        for path in [base_path, frame_2, frame_3]:
            if os.path.exists(path):
                imagenes.append(path)
        alien_imagenes[i] = imagenes
    return alien_imagenes

imagenes_aliens = cargar_imagenes_aliens()

reloj = pygame.time.Clock()
MAX_NIVELES = 5

# Estados posibles del juego
ESTADO_MENU = "MENU"
ESTADO_JUGANDO = "JUGANDO"
ESTADO_GAMEOVER = "GAMEOVER"

estado = ESTADO_MENU
nivel_actual = 1
jugando = True


 
while jugando:
    if estado == ESTADO_MENU:
        iniciar_musica_fondo()
        pantalla_inicio(pantalla)
        detener_musica_fondo()

        # Esperar a que el jugador presione una tecla para iniciar
        
        nivel_actual = 1
        estado = ESTADO_JUGANDO

    elif estado == ESTADO_JUGANDO:
        try:
            modulo_nivel = importlib.import_module(f"niveles.nivel_{nivel_actual}")
            cargar_funcion = getattr(modulo_nivel, f"cargar_nivel{nivel_actual}")
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Error al cargar el nivel {nivel_actual}: {e}")
            jugando = False
            continue

        enemigos_config, velocidad_disparo, musica_nivel = cargar_funcion(ANCHO, ALTO, fuente, imagenes_aliens)

        pygame.mixer.music.load(musica_nivel)
        pygame.mixer.music.play(-1)

        mostrar_texto_nivel(nivel_actual)

        nave = Nave(ANCHO // 2, ALTO - 40)
        grupo_nave = pygame.sprite.GroupSingle(nave)
        grupo_enemigos = enemigos_config
        posiciones_disparos = []
        disparos_enemigos = []

        jugando_nivel = True

        while jugando_nivel:
            reloj.tick(60)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jugando = False
                    jugando_nivel = False
                    break
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    disparo = pygame.Rect(nave.rect.centerx - 2, nave.rect.top, 5, 15)
                    posiciones_disparos.append(disparo)
                    reproducir_sonido_disparo()

            teclas = pygame.key.get_pressed()
            grupo_nave.update(teclas, ANCHO)

            # Movimiento disparos jugador
            for disparo in posiciones_disparos:
                disparo.y -= velocidad_disparo
            posiciones_disparos = [d for d in posiciones_disparos if d.y > 0]

            # Movimiento disparos enemigos
            for disparo in disparos_enemigos:
                disparo.y += 5
            disparos_enemigos = [d for d in disparos_enemigos if d.y < ALTO]

            # Disparos enemigos aleatorios
            if random.randint(0, 100) < 2:
                enemigos_lista = list(grupo_enemigos)
                if enemigos_lista:
                    atacante = random.choice(enemigos_lista)
                    disparo_enemigo = pygame.Rect(atacante.rect.centerx - 2, atacante.rect.bottom, 5, 15)
                    disparos_enemigos.append(disparo_enemigo)

            # Colisión disparo jugador con enemigo
            for disparo in posiciones_disparos[:]:
                for enemigo in grupo_enemigos:
                    if enemigo.rect.colliderect(disparo):
                        reproducir_sonido_colision()
                        grupo_enemigos.remove(enemigo)
                        posiciones_disparos.remove(disparo)
                        break

            # Colisión disparo enemigo con nave (GAME OVER)
            for disparo in disparos_enemigos[:]:
                if nave.rect.colliderect(disparo):
                    reproducir_sonido_gameover()
                    detener_musica_fondo()
                    mostrar_pantalla_gameover(pantalla)
                    estado = ESTADO_GAMEOVER
                    jugando_nivel = False
                    break

            grupo_enemigos.update()

            pantalla.fill(NEGRO)
            grupo_nave.draw(pantalla)
            grupo_enemigos.draw(pantalla)

            for disparo in posiciones_disparos:
                pygame.draw.rect(pantalla, BLANCO, disparo)
            for disparo in disparos_enemigos:
                pygame.draw.rect(pantalla, (255, 0, 0), disparo)

            # Nivel completado
            if len(grupo_enemigos) == 0:
                reproducir_sonido_victoria()
                detener_musica_fondo()
                texto_victoria = fuente.render("¡Nivel Completado!", True, BLANCO)
                pantalla.fill(NEGRO)
                pantalla.blit(texto_victoria, (ANCHO // 2 - texto_victoria.get_width() // 2, ALTO // 2))
                pygame.display.flip()
                pygame.time.delay(3000)
                nivel_actual += 1
                if nivel_actual > MAX_NIVELES:
                    estado = ESTADO_MENU  # Volver al menú después de terminar todos los niveles
                jugando_nivel = False

            pygame.display.flip()

    elif estado == ESTADO_GAMEOVER:
        # Esperar a que presione tecla para volver al menú
        estado = ESTADO_MENU

pygame.quit()
sys.exit()

