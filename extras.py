import random
import pygame, os
from pygame.locals import *
from configuracion import *

 


def dibujar(screen, productos_en_pantalla, producto_principal, producto_candidato, puntos, segundos, nivel):

    defaultFont = pygame.font.Font("assets/font.ttf", 20)
    defaultFontSmall = pygame.font.Font("assets/font.ttf", 10)

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
            rect = pygame.Rect(600, y2, IMAGEN_PRODUCTO_WIDTH,IMAGEN_PRODUCTO_HEIGHT) 
            imagen = pygame.image.load(os.path.join("assets", "productos", f"{producto[0]}.png"))
            imagen_transformada = pygame.transform.scale(imagen, (IMAGEN_PRODUCTO_WIDTH, IMAGEN_PRODUCTO_HEIGHT))
            screen.blit(imagen_transformada, (rect.x, rect.y))
            render = defaultFont.render(f"${producto[2]}", True, (255,255,255))
            screen.blit(render, (675, y2 + 20))
            render = defaultFontSmall.render(f"{producto[1]}", True, (255,255,255))
            screen.blit(render, (675, y2 + 50))

            

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

def pintarRecords(screen, font, font2, apodo):
    apodo = apodo.split(" ")[0:-1]
    apodo = "".join(apodo)
    print(apodo)
    screen.fill((0, 0, 0))
    texto =  font.render("Highscores", True, (0, 0, 255))
    screen.blit(texto, [175, 25])
    texto =  font2.render("Posicion     Apodo          Puntos", True, (0, 0, 255))
    screen.blit(texto, [25, 125])
    archivo_records = open("./records.txt")
    y = 30
    for linea in archivo_records:
            linea = linea[0:-1]
            if linea.find(apodo) >= 0:
                texto = font2.render(linea, True, (255, 200, 23))
                y+= 30
                screen.blit(texto, [25, 125 + y])
            else:
                texto = font2.render(linea, True, (255, 0, 0))
                y+= 30
                screen.blit(texto, [25, 125 + y])

    archivo_records.close()

def dibujar_rect_productos():
    lista_rect = []
    y2 = 75
    for i in range(0,7):
        rect = pygame.Rect(600, y2, IMAGEN_PRODUCTO_WIDTH,IMAGEN_PRODUCTO_HEIGHT)
        lista_rect.append(rect)
        y2 += 75
    return lista_rect


def dibujar_disparos(screen, disparos):
    for disparo in disparos:
        pygame.draw.rect(screen, (255,0,0), disparo)

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def dibujar_nave(screen, rect):
    screen.blit(NAVE_ESPACIAL, (rect.x, rect.y))

def manejar_movimiento_nave(tecla_presionada , rectangulo):
    if tecla_presionada[pygame.K_w] and rectangulo.y - VELOCIDAD_NAVE >= 100 and rectangulo.y - VELOCIDAD_NAVE <= 550: # Arriba
        rectangulo.y -= VELOCIDAD_NAVE
    
    if tecla_presionada[pygame.K_s] and rectangulo.y - VELOCIDAD_NAVE >= 0 and rectangulo.y - VELOCIDAD_NAVE <= 500: # Abajo
        rectangulo.y += VELOCIDAD_NAVE


def manejar_disparos(lista_disparos, rectangulo):
    for disparo in lista_disparos:
        disparo.x += VELOCIDAD_DISPARO
        if rectangulo.colliderect(disparo):
            pygame.event.post(pygame.event.Event(DISPARO_IMPACTO, rect=rectangulo.y))
            lista_disparos.remove(disparo)
        if disparo.x > ANCHO:
            lista_disparos.remove(disparo)