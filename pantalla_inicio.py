import pygame
import random
from sonidos import reproducir_sonido_inicio

# Constantes
ANCHO, ALTO = 800, 500
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

def pantalla_inicio(pantalla):
    reloj = pygame.time.Clock()

    # Crear estrellas (listas de tuplas)
    estrellas = [(random.randint(0, ANCHO), random.randint(0, ALTO)) for _ in range(100)]

    # Cargar fuente y logo
    fuente = pygame.font.Font("assets/fuentes/PressStart2P.ttf", 20)
    logo = pygame.image.load("assets/space_invaders_logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (700, 300))  # Ajustar tamaño si es necesario

    # Variables para titilar el logo
    mostrar_logo = True
    tiempo_ultimo_cambio = pygame.time.get_ticks()
    intervalo_titileo = 500  # ms

    contador_texto = 0
    esperando_tecla = True

    while esperando_tecla:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                reproducir_sonido_inicio()
                efecto_desvanecimiento(pantalla)
                return

        pantalla.fill(NEGRO)

        # Mover y dibujar estrellas
        nuevas_estrellas = []
        for (x, y) in estrellas:
            y += 2
            if y > ALTO:
                y = 0
                x = random.randint(0, ANCHO)
            nuevas_estrellas.append((x, y))
            pygame.draw.circle(pantalla, BLANCO, (x, y), 2)
        estrellas = nuevas_estrellas

        # Actualizar titileo del logo
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_cambio >= intervalo_titileo:
            mostrar_logo = not mostrar_logo
            tiempo_ultimo_cambio = tiempo_actual

        # Dibujar logo más arriba, en el centro horizontal
        if mostrar_logo:
            pantalla.blit(logo, (ANCHO // 2 - logo.get_width() // 2, int(ALTO * 0.0)))

        # Texto animado
        contador_texto += 1
        if (contador_texto // 30) % 2 == 0:
            texto = fuente.render("Presiona cualquier tecla para comenzar", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO - 100))

        pygame.display.flip()
        reloj.tick(60)

def efecto_desvanecimiento(pantalla):
    fade = pygame.Surface((ANCHO, ALTO))
    fade.fill(NEGRO)
    for alpha in range(0, 255, 10):
        fade.set_alpha(alpha)
        pantalla.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)


