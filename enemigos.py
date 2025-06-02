import pygame

import pygame

def crear_enemigo(x, y, image_paths, pantalla_ancho=800):
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    imagenes = [
        pygame.transform.scale(pygame.image.load(path).convert_alpha(), (40, 40))  # Tamaño más pequeño
        for path in image_paths
    ]

    return {
        "imagenes": imagenes,
        "index_imagen": 0,
        "rect": imagenes[0].get_rect(topleft=(x, y)),
        "velocidad_x": 1,
        "velocidad_y": 10,
        "contador_animacion": 0,
        "frecuencia_animacion": 20,
        "pantalla_ancho": pantalla_ancho
    }

def actualizar_enemigo(enemigo):
    enemigo["rect"].x += enemigo["velocidad_x"]

    if enemigo["rect"].x < 0 or enemigo["rect"].x > enemigo["pantalla_ancho"] - enemigo["rect"].width:
        enemigo["velocidad_x"] *= -1
        enemigo["rect"].y += enemigo["velocidad_y"]
        if enemigo["rect"].x < 0:
            enemigo["rect"].x = 0
        elif enemigo["rect"].x > enemigo["pantalla_ancho"] - enemigo["rect"].width:
            enemigo["rect"].x = enemigo["pantalla_ancho"] - enemigo["rect"].width

    enemigo["contador_animacion"] += 1
    if enemigo["contador_animacion"] >= enemigo["frecuencia_animacion"]:
        enemigo["contador_animacion"] = 0
        enemigo["index_imagen"] = (enemigo["index_imagen"] + 1) % len(enemigo["imagenes"])

def dibujar_enemigo(pantalla, enemigo):
    imagen_actual = enemigo["imagenes"][enemigo["index_imagen"]]
    pantalla.blit(imagen_actual, enemigo["rect"])

def disparo_enemigo(enemigo):
    return pygame.Rect(enemigo["rect"].centerx - 2, enemigo["rect"].bottom, 5, 15)
