import random
import pygame
from pygame.locals import *
from configuracion import *


def dameLetraApretada(key):
    if K_0 <= key <= K_9:
        return str(key - K_0)
    else:
        return ""


def dibujar(screen, productos_en_pantalla, producto_principal, producto_candidato, puntos, segundos):

    defaultFont = pygame.font.Font(pygame.font.get_default_font(), 20)
    defaultFontGrande = pygame.font.Font(pygame.font.get_default_font(), 30)

    # Linea del piso
    pygame.draw.line(screen, (255, 255, 255),
                     (0, ALTO-70), (ANCHO, ALTO-70), 5)
    ren1 = defaultFont.render(producto_candidato, 1, COLOR_TEXTO)
    ren2 = defaultFont.render("Puntos: " + str(puntos), 1, COLOR_TEXTO)
    if (segundos < 15):
        ren3 = defaultFont.render(
            "Tiempo: " + str(int(segundos)), 1, COLOR_TIEMPO_FINAL)
    else:
        ren3 = defaultFont.render(
            "Tiempo: " + str(int(segundos)), 1, COLOR_TEXTO)
   # Dibujar los nombres de los productos uno debajo del otro
    x_pos = 130
    y_pos = ALTO - (ALTO-100)

    pos = 0
    for producto in productos_en_pantalla:
        nombre_en_pantalla = str(pos) + " - "+producto[0]+producto[1]
        if producto[0] == producto_principal[0] and producto[1]== producto_principal[1]:
            screen.blit(defaultFontGrande.render(nombre_en_pantalla,
                        1, COLOR_TIEMPO_FINAL), (x_pos, y_pos))
        else:
            screen.blit(defaultFontGrande.render(
                nombre_en_pantalla, 1, COLOR_LETRAS), (x_pos, y_pos))
        pos += 1
        y_pos += ESPACIO

    screen.blit(ren1, (190, 570))
    screen.blit(ren2, (600, 10))
    screen.blit(ren3, (10, 10))
