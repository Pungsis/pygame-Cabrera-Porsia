#! /usr/bin/env python
import os
import random
import sys
import math
from button import Button
import pygame
from pygame.locals import *
from configuracion import *
from funcionesVACIAS import *
from extras import *
from records_utils import *

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()
# Preparar la ventana
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Peguele al precio")
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png")).convert()
NAVE_ESPACIAL_IMAGEN = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
NAVE_ESPACIAL_WIDTH = 100
NAVE_ESPACIAL_HEIGHT = 95
NAVE_ESPACIAL = pygame.transform.rotate(pygame.transform.scale(NAVE_ESPACIAL_IMAGEN, (NAVE_ESPACIAL_WIDTH, NAVE_ESPACIAL_HEIGHT)), 90)
VELOCIDAD_NAVE = 5
VELOCIDAD_DISPARO = 5
MAXIMOS_DISPAROS = 3
disparos = []
DISPARO_IMPACTO = pygame.USEREVENT + 2
IMAGEN_PRODUCTO_WIDTH = 50
IMAGEN_PRODUCTO_HEIGHT = 50

def dibujar_nave(rect):
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

def dibujar_rect_productos():
    lista_rect = []
    y2 = 75
    for i in range(0,7):
        rect = pygame.Rect(700, y2, IMAGEN_PRODUCTO_WIDTH,IMAGEN_PRODUCTO_HEIGHT)
        lista_rect.append(rect)
        y2 += 75
    return lista_rect

def dibujar_disparos(disparos):
    for disparo in disparos:
        pygame.draw.rect(screen, (255,0,0), disparo)

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def main():
    rect = pygame.Rect(100, 300, NAVE_ESPACIAL_WIDTH,NAVE_ESPACIAL_HEIGHT)
    lista_rectangulos_prod = dibujar_rect_productos()
    diccionario = {}
    contador = 0
    for i in lista_rectangulos_prod:
        diccionario[contador] = [i.x, i.y]
        contador += 1
    print(diccionario)
    gameClock = pygame.time.Clock()
    totaltime = 0
    nivel = 1
    segundos = TIEMPO_MAX # Tiempo max va aca
    corriendo = True
    puntos = 0 
    producto_candidato = ""
    lista_productos = lectura()  
    producto = dameProducto(lista_productos, MARGEN)
    productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
    producto_elegido_programa = dameProducto(productos_en_pantalla[1:], MARGEN)
    index = index_producto_elegido(productos_en_pantalla, producto_elegido_programa)
    print(productos_en_pantalla)
    dibujar(screen, productos_en_pantalla, producto,
            producto_candidato, puntos, segundos, nivel)
    time_delay = 1000
    timer_event = pygame.USEREVENT+1
    pygame.time.set_timer(timer_event, time_delay)


    while corriendo:
        gameClock.tick(40)
        totaltime += gameClock.get_time()

        for e in pygame.event.get():

            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == timer_event:
                segundos -= 1
                if segundos == 0:
                    juego_terminado(puntos)
                    corriendo = False
            if e.type == KEYDOWN:
                # Hay un error si pones una letra por ejemplo y clickeas
                # aunque no aparezca en  pantalla!
                # letra = dameLetraApretada(e.key)
                # producto_candidato += letra  # va concatenando las letras que escribe
                # if e.key == K_BACKSPACE:
                #     producto_candidato = producto_candidato[0:len(producto_candidato)-1]
                # if e.key == K_RETURN:  # presionó enter
                #     nivel += 1
                   
                #     if indice < len(productos_en_pantalla):
                #         puntos += procesar(producto, productos_en_pantalla[indice], MARGEN)
                #         producto_candidato = ""
                #         producto = dameProducto(lista_productos, MARGEN)
                #         productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
                #     else:
                #         producto_candidato = ""
                if e.key == pygame.K_RCTRL and len(disparos) < MAXIMOS_DISPAROS:
                    bullet = pygame.Rect(rect.x + rect.width, rect.y + rect.height // 2 - 2, 10, 5)
                    disparos.append(bullet)
            if e.type == DISPARO_IMPACTO:
                print(diccionario[index][1])
                if e.rect == diccionario[index][1]:
                    print("PRODUCTO ELEGIDO GOLPEADO!!!")
                    puntos += procesar(producto, productos_en_pantalla[index], MARGEN)
                producto = dameProducto(lista_productos, MARGEN)
                productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
                producto_elegido_programa = dameProducto(productos_en_pantalla[1:], MARGEN)
                index = index_producto_elegido(productos_en_pantalla, producto_elegido_programa)    
        for i in lista_rectangulos_prod:
            manejar_disparos(disparos,i)
        tecla_presionada = pygame.key.get_pressed()
        manejar_movimiento_nave(tecla_presionada, rect)

        screen.fill(COLOR_FONDO)
        screen.blit(BACKGROUND, (0, 0))
        dibujar_nave(rect)
        dibujar_disparos(disparos)
        dibujar(screen, productos_en_pantalla, producto,
            producto_candidato, puntos, segundos, nivel)

        pygame.display.update()



def menu():
    corriendo = True
    fpsClock = pygame.time.Clock()
    pygame.display.flip()
    while corriendo:
        MENU_MOUSE_POSICION = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("PEGUELE AL PRECIO", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(None, pos=(400, 250), 
                            text_input="1 jugador", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(None, pos=(400, 400), 
                            text_input="2 jugadores", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(None, pos=(400, 550), 
                            text_input="Records", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.cambiarColor(MENU_MOUSE_POSICION)
            button.actualizar(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                if PLAY_BUTTON.chequearEntrada(MENU_MOUSE_POSICION):
                    instrucciones()
                    corriendo = False
              
                if QUIT_BUTTON.chequearEntrada(MENU_MOUSE_POSICION):
                    corriendo = False
                    pygame.quit()
                    sys.exit()

        if corriendo:
            pygame.display.update()
            fpsClock.tick(30)
    
def instrucciones():
    fpsClock = pygame.time.Clock()
    pygame.display.flip()
    font_titulo = pygame.font.Font('assets/font.ttf', 20)
    font_texto = pygame.font.Font('assets/font.ttf', 14)
    corriendo = True
    while True:
        screen.fill((0, 0, 0))
        texto =  font_titulo.render("Instrucciones", True, (255, 255, 255))
        screen.blit(texto, [250, 25])
        archivo_instrucciones = open("./instrucciones.txt")
        x = 30

        for linea in archivo_instrucciones:
            linea = linea[0:-1]
            texto = font_texto.render(linea, True, (255, 255, 255))
            x+= 30
            screen.blit(texto, [25, 100 + x])

        texto =  font_titulo.render("TOQUE CUALQUIER TECLA PARA EMPEZAR", True, (255, 255, 255))
        screen.blit(texto, [50, 500])

        archivo_instrucciones.close()

        fpsClock.tick(30)
        pygame.display.flip()

        pygame.time.wait(1000)
        for event in pygame.event.get():
            # Presionar cualquier tecla para ir al juego 
            if event.type == KEYDOWN:
                main()
                return
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                corriendo == False

        if corriendo:
            pygame.display.update()

def juego_terminado(puntos):
    fpsClock = pygame.time.Clock()
    pygame.display.flip()
    font = pygame.font.Font("assets/font.ttf", 40)
    font2 = pygame.font.Font("assets/font.ttf", 20)
    font3 = pygame.font.Font("assets/font.ttf", 25)
    apodo = ""
    while True:
        screen.fill((0, 0, 0))
        texto = font.render("GAME OVER", True, (255,0,0), (180, 200, 200))
        screen.blit(texto, (200, 100))
        
        texto = font2.render(f"Sus puntos fueron {str(puntos)}", True, (255, 255,255))
        screen.blit(texto, (ANCHO / 5, 200))
        
        texto = font2.render(f"Ingrese un apodo", True, (255, 150,200))
        screen.blit(texto, (ANCHO / 3.5, 300))

        texto = font3.render(apodo, True, (255, 255, 222))
        pygame.draw.line(screen, (255, 255, 255),
                     (450, 450), (410, 450), 5)
        pygame.draw.line(screen, (255, 255, 255),
                     (400, 450), (360, 450), 5)
        pygame.draw.line(screen, (255, 255, 255),
                     (350, 450), (310, 450), 5)

        for event in pygame.event.get():
            # Presionar cualquier tecla para ir al juego 
            if event.type == pygame.KEYDOWN:
                if K_a <= event.key <= K_z:
                    # Recordar los espacios en blanco! por eso el 6
                    if len(str(apodo)) < 6:
                        apodo += str(pygame.key.name(event.key)).upper() + " "
                        print(apodo)
                if event.key == K_RETURN:
                    if len(str(apodo)) == 6:
                        write_in_record(puntos, apodo)
                        diccionario_record = recordsDic(records_helper()[0], records_helper()[1])
                        write_records(diccionario_record)
                        records()

                if event.key == K_BACKSPACE:
                    apodo = apodo[0:len(apodo) - 2]
            
            # if event.type == pygame.KEYDOWN:
            #     if event.key == K_RETURN:
            #         print("hello world")
            #     if event.key == K_BACKSPACE:
            #         apodo = apodo[0:len(apodo) - 2]
            #         print("h")
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(texto, (ANCHO / 2.5, 400)) 
        fpsClock.tick(30)
        pygame.display.update()


def records():
    fpsClock = pygame.time.Clock()
    pygame.display.flip()
    font = pygame.font.Font("assets/font.ttf", 40)
    font2 = pygame.font.Font("assets/font.ttf", 20)
    while True:
        pintarDeNuevo(font, font2)

        for event in pygame.event.get():
            # Presionar cualquier tecla para ir al juego 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
         
        fpsClock.tick(30)
        pygame.display.update()


def pintarDeNuevo(font, font2):
    screen.fill((0, 0, 0))
    texto =  font.render("Highscores", True, (0, 0, 255))
    screen.blit(texto, [175, 25])
    texto =  font2.render("Posicion     Apodo      puntos", True, (0, 0, 255))
    screen.blit(texto, [25, 125])
    archivo_records = open("./records.txt")
    x = 30

    for linea in archivo_records:
            linea = linea[0:-1]
            texto = font2.render(linea, True, (255, 0, 0))
            x+= 30
            screen.blit(texto, [25, 125 + x])

    archivo_records.close()


# Programa Principal ejecuta Main
if __name__ == "__main__":
    main()
