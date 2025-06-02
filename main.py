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
    reproducir_sonido_victoria,
    reproducir_sonido_explosion_nave
)
from nave import crear_nave, mover_nave, dibujar_nave
from enemigos import crear_enemigo, actualizar_enemigo, dibujar_enemigo, disparo_enemigo

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
    nuevas_dimensiones = (40, 40)
    for i in range(1, 5):
        imagenes = []
        base_path = f"assets/aliens/alien_{i}.png"
        frame_2 = f"assets/aliens/alien_{i}_frame_2.png"
        frame_3 = f"assets/aliens/alien_{i}_frame_3.png"
        for path in [base_path, frame_2, frame_3]:
            if os.path.exists(path):
                imagen = pygame.image.load(path).convert_alpha()
                imagen = pygame.transform.scale(imagen, nuevas_dimensiones)
                imagenes.append(imagen)
        alien_imagenes[i] = imagenes
    return alien_imagenes

imagenes_aliens = cargar_imagenes_aliens()
explosion_enemigo_img = pygame.image.load("assets/explosion_enemigos.png").convert_alpha()
explosion_enemigo_img = pygame.transform.scale(explosion_enemigo_img, (60, 60))
explosion_nave_img = pygame.image.load("assets/explosion_nave.png").convert_alpha()
explosion_nave_img = pygame.transform.scale(explosion_nave_img, (60, 60))

reloj = pygame.time.Clock()
MAX_NIVELES = 5
jugando = True

while jugando:
    iniciar_musica_fondo()
    pantalla_inicio(pantalla)
    detener_musica_fondo()

    nivel_actual = 1

    while nivel_actual <= MAX_NIVELES:
        try:
            modulo_nivel = importlib.import_module(f"niveles.nivel_{nivel_actual}")
            cargar_funcion = getattr(modulo_nivel, f"cargar_nivel{nivel_actual}")
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Error al cargar el nivel {nivel_actual}: {e}")
            jugando = False
            break

        enemigos_config, velocidad_disparo, musica_nivel = cargar_funcion(ANCHO, ALTO, fuente, imagenes_aliens)
        pygame.mixer.music.load(musica_nivel)
        pygame.mixer.music.play(-1)
        mostrar_texto_nivel(nivel_actual)

        nave = crear_nave(ANCHO // 2, ALTO - 40)
        grupo_enemigos = enemigos_config
        posiciones_disparos = []
        disparos_enemigos = []
        explosiones = []

        nivel_en_curso = True
        while nivel_en_curso:
            reloj.tick(60)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jugando = False
                    nivel_en_curso = False
                    break
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    disparo = pygame.Rect(nave["rect"].centerx - 2, nave["rect"].top, 5, 15)
                    posiciones_disparos.append(disparo)
                    reproducir_sonido_disparo()

            teclas = pygame.key.get_pressed()
            mover_nave(nave, teclas, ANCHO)

            for disparo in posiciones_disparos:
                disparo.y -= velocidad_disparo
            posiciones_disparos = [d for d in posiciones_disparos if d.y > 0]

            for disparo in disparos_enemigos:
                disparo.y += 5
            disparos_enemigos = [d for d in disparos_enemigos if d.y < ALTO]

            if random.randint(0, 100) < 2 and grupo_enemigos:
                atacante = random.choice(grupo_enemigos)
                disparos_enemigos.append(disparo_enemigo(atacante))

            for disparo in posiciones_disparos[:]:
                for enemigo in grupo_enemigos[:]:
                    if enemigo["rect"].colliderect(disparo):
                        reproducir_sonido_colision()
                        posiciones_disparos.remove(disparo)
                        grupo_enemigos.remove(enemigo)
                        explosiones.append((explosion_enemigo_img, enemigo["rect"].center, 15))
                        break

            for disparo in disparos_enemigos[:]:
                if nave["rect"].colliderect(disparo):
                    reproducir_sonido_explosion_nave()
                    explosiones.append((explosion_nave_img, nave["rect"].center, 30))

                    pantalla.fill(NEGRO)
                    for enemigo in grupo_enemigos:
                        dibujar_enemigo(pantalla, enemigo)
                    for d in posiciones_disparos:
                        pygame.draw.rect(pantalla, BLANCO, d)
                    for d in disparos_enemigos:
                        pygame.draw.rect(pantalla, (255, 0, 0), d)
                    for imagen, centro, _ in explosiones:
                        rect = imagen.get_rect(center=centro)
                        pantalla.blit(imagen, rect)
                    pygame.display.flip()
                    pygame.time.delay(1000)

                    reproducir_sonido_gameover()
                    detener_musica_fondo()
                    mostrar_pantalla_gameover(pantalla)

                    nivel_en_curso = False
                    nivel_actual = MAX_NIVELES + 1  # fuerza volver al menú
                    break

            for enemigo in grupo_enemigos:
                actualizar_enemigo(enemigo)

            pantalla.fill(NEGRO)
            dibujar_nave(pantalla, nave)
            for enemigo in grupo_enemigos:
                dibujar_enemigo(pantalla, enemigo)
            for disparo in posiciones_disparos:
                pygame.draw.rect(pantalla, BLANCO, disparo)
            for disparo in disparos_enemigos:
                pygame.draw.rect(pantalla, (255, 0, 0), disparo)

            for exp in explosiones[:]:
                imagen, centro, tiempo = exp
                rect = imagen.get_rect(center=centro)
                pantalla.blit(imagen, rect)
                tiempo -= 1
                if tiempo <= 0:
                    explosiones.remove(exp)
                else:
                    idx = explosiones.index(exp)
                    explosiones[idx] = (imagen, centro, tiempo)

            if not grupo_enemigos:
                reproducir_sonido_victoria()
                detener_musica_fondo()
                texto_victoria = fuente.render("¡Nivel Completado!", True, BLANCO)
                pantalla.fill(NEGRO)
                pantalla.blit(texto_victoria, (ANCHO // 2 - texto_victoria.get_width() // 2, ALTO // 2))
                pygame.display.flip()
                pygame.time.delay(3000)
                nivel_en_curso = False
                nivel_actual += 1

            pygame.display.flip()

pygame.quit()
sys.exit()

