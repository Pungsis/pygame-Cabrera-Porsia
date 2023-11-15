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

disparos = []

def main():
    rect = pygame.Rect(100, 300, NAVE_ESPACIAL_WIDTH,NAVE_ESPACIAL_HEIGHT)
    lista_rectangulos_prod = dibujar_rect_productos()
    diccionario = {}
    contador = 0
    for i in lista_rectangulos_prod:
        diccionario[contador] = [i.x, i.y]
        contador += 1
    gameClock = pygame.time.Clock()
    nivel = 1
    segundos = TIEMPO_MAX # Tiempo max va aca
    corriendo = True
    puntos = 0 
    producto_candidato = ""
    lista_productos = lectura()  
    producto = buscar_producto(lista_productos)
    productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
    producto_elegido_programa = dameProducto(producto, productos_en_pantalla[1:], MARGEN)
    index = index_producto_elegido(productos_en_pantalla, producto_elegido_programa)
    dibujar(screen, productos_en_pantalla, producto,
            producto_candidato, puntos, segundos, nivel)
    time_delay = 1000
    timer_event = pygame.USEREVENT+1
    pygame.time.set_timer(timer_event, time_delay)


    while corriendo:
        gameClock.tick(40)
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
                if e.key == pygame.K_RCTRL and len(disparos) < MAXIMOS_DISPAROS:
                    bullet = pygame.Rect(rect.x + rect.width, rect.y + rect.height // 2 - 2, 10, 5)
                    disparos.append(bullet)
            if e.type == DISPARO_IMPACTO:
                nivel += 1
                if e.rect == diccionario[index][1]:
                    print("PRODUCTO ELEGIDO GOLPEADO!!!")
                    puntos += procesar(productos_en_pantalla[index])
                
                producto = buscar_producto(lista_productos)
                print(producto)
                productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, MARGEN)
                print(productos_en_pantalla)
                producto_elegido_programa = dameProducto(producto, productos_en_pantalla[1:], MARGEN)
                print(producto_elegido_programa)
                index = index_producto_elegido(productos_en_pantalla, producto_elegido_programa)    
        for i in lista_rectangulos_prod:
            manejar_disparos(disparos,i)
        tecla_presionada = pygame.key.get_pressed()
        manejar_movimiento_nave(tecla_presionada, rect)

        screen.fill(COLOR_FONDO)
        screen.blit(BACKGROUND, (0, 0))
        dibujar_nave(screen, rect)
        dibujar_disparos(screen, disparos)
        dibujar(screen, productos_en_pantalla, producto,
            producto_candidato, puntos, segundos, nivel)

        pygame.display.update()

def menu():
    corriendo = True
    fpsClock = pygame.time.Clock()
    coordenadas_lista = []
    for i in range(60):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            coordenadas_lista.append([x,y])
    while corriendo:
        screen.fill((0,0,0))
        MENU_MOUSE_POSICION = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("PEGUELE AL PRECIO", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(None, pos=(400, 250), 
                            text_input="1 jugador", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        RECORDS_BUTTON = Button(None, pos=(400, 400), 
                            text_input="Records", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(None, pos=(400, 550), 
                            text_input="Salir", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        screen.blit(BACKGROUND_MENU_TRANSFORMADA, (0,0))
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, RECORDS_BUTTON, QUIT_BUTTON]:
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
              
                if RECORDS_BUTTON.chequearEntrada(MENU_MOUSE_POSICION):
                    records("F A L S E")
                if QUIT_BUTTON.chequearEntrada(MENU_MOUSE_POSICION):
                    pygame.quit()
                    sys.exit()
        for j in coordenadas_lista:
            x = j[0]
            y = j[1]
            pygame.draw.circle(screen, COLOR_TEXTO, (x,y), 2)
            j[1] += 1
            if j[1] > ALTO:
                j[1] = 0

         

        pygame.display.update()
        fpsClock.tick(30)
    
def instrucciones():
    fpsClock = pygame.time.Clock()
    font_titulo = pygame.font.Font('assets/font.ttf', 20)
    font_texto = pygame.font.Font('assets/font.ttf', 14)
    corriendo = True
    coordenadas_lista = []
    for i in range(60):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            coordenadas_lista.append([x,y])
    
    while True:
        texto =  font_titulo.render("Instrucciones", True, (23, 255, 255))
        screen.fill((0, 0, 0))        
        for event in pygame.event.get():
            # Presionar cualquier tecla para ir al juego 
            if event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                main()
                return
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                corriendo == False
        screen.blit(BACKGROUND_MENU_TRANSFORMADA, (0,0))
        screen.blit(texto, [275, 25])
        archivo_instrucciones = open("./instrucciones.txt")
        x = 30
        for linea in archivo_instrucciones:
            linea = linea[0:-1]
            texto = font_texto.render(linea, True, (200, 100, 200))
            x+= 30
            screen.blit(texto, [275, 100 + x])

        texto =  font_titulo.render("TOQUE CUALQUIER TECLA PARA EMPEZAR", True, (255, 255, 255))
        screen.blit(texto, [50, 500])
        archivo_instrucciones.close()

        for j in coordenadas_lista:
            x = j[0]
            y = j[1]
            pygame.draw.circle(screen, COLOR_TEXTO, (x,y), 2)
            j[1] += 1
            if j[1] > ALTO:
                j[1] = 0
        fpsClock.tick(30)
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
                if event.key == K_RETURN:
                    if len(str(apodo)) == 6:
                        
                        write_in_record(puntos, apodo)
                        diccionario_record = recordsDic(records_helper()[0], records_helper()[1])
                        write_records(diccionario_record)
                        records(apodo)

                if event.key == K_BACKSPACE:
                    apodo = apodo[0:len(apodo) - 2]
    
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(texto, (ANCHO / 2.5, 400)) 
        fpsClock.tick(30)
        pygame.display.update()

def records(apodo):
    fpsClock = pygame.time.Clock()
    pygame.display.flip()
    font = pygame.font.Font("assets/font.ttf", 40)
    font2 = pygame.font.Font("assets/font.ttf", 20)
    corriendo = True
    while corriendo:
        pintarRecords(screen, font, font2, apodo)
        MENU_MOUSE_POSICION = pygame.mouse.get_pos()
        MENU_TEXT = get_font(30).render("", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
        MENU_BUTTON = Button(None, pos=(400, 550), 
                                text_input="Volver al menu", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        screen.blit(MENU_TEXT, MENU_RECT)
        MENU_BUTTON.actualizar(screen)

        for event in pygame.event.get():
            # Presionar cualquier tecla para ir al juego 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.chequearEntrada(MENU_MOUSE_POSICION):
                    menu()
            MENU_BUTTON.actualizar(screen)
            
            fpsClock.tick(30)
            pygame.display.update()




# Programa Principal ejecuta Main
if __name__ == "__main__":
    menu()
