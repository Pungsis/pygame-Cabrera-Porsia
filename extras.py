import random
import pygame, os
from pygame.locals import *
from configuracion import *

     
 


def dibujar(screen, productos_en_pantalla, producto_principal, producto_candidato, puntos, segundos, nivel):

    defaultFont = pygame.font.Font("assets/font.ttf", 20)
    defaultFontGrande = pygame.font.Font("assets/font.ttf", 30)

    # Linea del piso
    pygame.draw.line(screen, (255, 255, 255),
                     (0, 100), (ANCHO, 100), 1)
    ren1 = defaultFont.render(producto_candidato, 1, COLOR_TEXTO)
    ren2 = defaultFont.render("Puntos: ", 1, COLOR_TEXTO)
    ren5 = defaultFont.render(str(puntos), 1, COLOR_TEXTO)
    ren4 = defaultFont.render(f"Nivel {nivel}: ", 1, (255,23,45))
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
    y2 = 75
    for producto in productos_en_pantalla:
        if producto[0] == producto_principal[0] and producto[1]== producto_principal[1]:
            imagen = pygame.image.load(os.path.join("assets", "productos", f"{producto[0]}.png")).convert_alpha()
            imagen_transformada = pygame.transform.scale(imagen, (60, 60))
            pygame.draw.rect(screen, (255, 0, 0), (475, 10, 70, 70), 2)
            screen.blit(imagen_transformada, (475, 10))
        else:
            rect = pygame.Rect(700, y2, IMAGEN_PRODUCTO_WIDTH,IMAGEN_PRODUCTO_HEIGHT) 
            imagen = pygame.image.load(os.path.join("assets", "productos", f"{producto[0]}.png"))
            imagen_transformada = pygame.transform.scale(imagen, (IMAGEN_PRODUCTO_WIDTH, IMAGEN_PRODUCTO_HEIGHT))
            screen.blit(imagen_transformada, (rect.x, rect.y))
            

        y2 += 75
        # nombre_en_pantalla = str(pos) + " - "+producto[0]+producto[1]
        # if producto[0] == producto_principal[0] and producto[1]== producto_principal[1]:
        #     screen.blit(defaultFontGrande.render(nombre_en_pantalla,
        #                 1, COLOR_TIEMPO_FINAL), (x_pos, y_pos))
        # else:
        #     screen.blit(defaultFontGrande.render(
        #         nombre_en_pantalla, 1, COLOR_LETRAS), (x_pos, y_pos))
        pos += 1
        y_pos += ESPACIO

    screen.blit(ren1, (190, 570))
    screen.blit(ren2, (600, 10))
    screen.blit(ren3, (10, 10))
    screen.blit(ren4, (300, 10))
    screen.blit(ren5, (600, 40))
