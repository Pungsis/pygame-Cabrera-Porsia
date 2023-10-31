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

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

def main():

    # tiempo total del juego
    gameClock = pygame.time.Clock()
    totaltime = 0
    segundos = 5 # Tiempo max va aca
    fps = FPS_inicial
    corriendo = True

    puntos = 0  # puntos o dinero acumulado por el jugador
    producto_candidato = ""


    #Lee el archivo y devuelve una lista con los productos,
    lista_productos = lectura()  # lista de productos

    # Elegir un producto, [producto, calidad, precio]
    producto = dameProducto(lista_productos, MARGEN)

    # Elegimos productos aleatorios, garantizando que al menos 2 mas tengan el mismo precio.
    # De manera aleatoria se debera tomar el valor economico o el valor premium.
    # Agregar  '(economico)' o '(premium)' y el precio
    productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
    print(productos_en_pantalla)

    # dibuja la pantalla la primera vez
    dibujar(screen, productos_en_pantalla, producto,
            producto_candidato, puntos, segundos)
    time_delay = 1000
    timer_event = pygame.USEREVENT+1
    pygame.time.set_timer(timer_event, time_delay)

    while segundos > fps/1000 or corriendo:
        # 1 frame cada 1/fps segundos
        gameClock.tick(fps)
        totaltime += gameClock.get_time()

        if True:
            fps = 10

        # Buscar la tecla apretada del modulo de eventos de pygame
        for e in pygame.event.get():

            # QUIT es apretar la X en la ventana
            if e.type == QUIT:
                pygame.quit()
                return ()
            if e.type == timer_event:
                segundos -= 1
                if segundos == 0:
                    juego_terminado(puntos)
                    corriendo = False

            

            # Ver si fue apretada alguna tecla
            if e.type == KEYDOWN:
                letra = dameLetraApretada(e.key)
                producto_candidato += letra  # va concatenando las letras que escribe
                if e.key == K_BACKSPACE:
                    # borra la ultima
                    producto_candidato = producto_candidato[0:len(producto_candidato)-1]
                if e.key == K_RETURN:  # presionó enter
                    indice = int(producto_candidato)
                    # chequeamos si el prducto no es el producto principal. Si no lo es procesamos el producto
                    if indice < len(productos_en_pantalla):
                        puntos += procesar(producto, productos_en_pantalla[indice], MARGEN)
                        producto_candidato = ""
                        # Elegir un producto
                        producto = dameProducto(lista_productos, MARGEN)
                        # elegimos productos aleatorios, garantizando que al menos 2 mas tengan el mismo precio
                        productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
                    else:
                        producto_candidato = ""
        # Hay que cambiar esto! get ticks se inicializa en pygame.init()
        
            

        # Limpiar pantalla anterior
        screen.fill(COLOR_FONDO)

        # Dibujar de nuevo todo
        dibujar(screen, productos_en_pantalla, producto,
                producto_candidato, puntos, segundos)

        pygame.display.flip()

    while 1 or corriendo:
        # Esperar el QUIT del usuario
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()

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
    menu()
