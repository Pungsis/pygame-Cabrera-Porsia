import pygame, os

MINIMO = 40
TAMANNO_LETRA = 30
TAMANNO_LETRA_GRANDE = 80
FPS_INICIAL = 30
TIEMPO_MAX = 61
N = 6

ANCHO = 800
ALTO = 600
COLOR_LETRAS = (20,200,20)
COLOR_FONDO = (0,0,0)
COLOR_TEXTO = (200,200,200)
COLOR_TIEMPO_FINAL = (200,20,10)
MARGEN = 1000
ESPACIO = 50
IMAGEN_PRODUCTO_WIDTH = 50
IMAGEN_PRODUCTO_HEIGHT = 50

DISPARO_IMPACTO = pygame.USEREVENT + 2
IMAGEN_PRODUCTO_WIDTH = 50
IMAGEN_PRODUCTO_HEIGHT = 50

VELOCIDAD_NAVE = 5
VELOCIDAD_DISPARO = 5
MAXIMOS_DISPAROS = 3
     
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
BACKGROUND_MENU = pygame.image.load(os.path.join("assets", "background2.jpg"))
BACKGROUND_MENU_TRANSFORMADA = pygame.transform.scale(BACKGROUND_MENU, (800, 800))
NAVE_ESPACIAL_IMAGEN = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
NAVE_ESPACIAL_WIDTH = 100
NAVE_ESPACIAL_HEIGHT = 95
NAVE_ESPACIAL = pygame.transform.rotate(pygame.transform.scale(NAVE_ESPACIAL_IMAGEN, (NAVE_ESPACIAL_WIDTH, NAVE_ESPACIAL_HEIGHT)), 90)
