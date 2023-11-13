from principal import *
from configuracion import *
import random
import math
from extras import *

# lee el archivo y carga en la lista lista_producto todas las palabras
def lectura():
    lista = []
    archivo = open("./productos.txt")
    contador = 0
    for linea in archivo:
        linea = linea[0:-1]
        lista.append(linea.split(","))
        lista[contador][1] = int(lista[contador][1])
        lista[contador][2] = int(lista[contador][2])
        contador += 1
    archivo.close()
    return lista

# Funcion de prueba
# def lectura():
#     return [["Arroz", 1001, 1037],
#             ["Yerba mate", 4546, 4904],
#             ["Televisor Smart", 2055, 2439],
#             ["Aceite de cocina", 3674, 4783],
#             ["Mouse", 1635, 3603],
#             ["Monitor de computadora", 2782, 2870],
#             ["Silla de oficina", 3174, 4391],
#             ["Lavadora", 3720, 4197],
#             ["Refrigerador", 3352, 4533],
#             ["Smartphone", 2070, 2224],
#             ["Laptop", 4650, 4854],
#             ["Cafetera", 2358, 3646],
#             ["Batidora", 183, 4401],
#             ["Microondas", 4254, 4624]]



def buscar_producto(lista_productos):
    producto_azar = lista_productos[random.randint(0, len(lista_productos) - 1)]
    index = random.randint(1,2)
    precio = producto_azar[index]
    if index == 1:
        return [producto_azar[0], "(Economico)", int(precio)]
    else:
        return [producto_azar[0], "(Premium)", int(precio)]



def dameProducto(lista_productos, margen):
    busqueda = []
    while len(busqueda) < 2:
        producto = lista_productos[random.randint(0,5)]
        if producto[1] == "(Premium)":
            busqueda = list(filter(lambda x: abs(producto[2] - x[2]) < margen, lista_productos))
        else:
            busqueda = list(filter(lambda x: abs(producto[2] - x[2]) < margen, lista_productos))
    return producto




#Devuelve True si existe el precio recibido como parametro aparece al menos 2 veces. Debe considerar el Margen.
def esUnPrecioValido(precio, lista_productos, margen):
    busqueda = list(filter(lambda x: abs(precio - x[2]) < margen or precio == x[1], lista_productos))
    return len(busqueda) >= 2



def procesar(producto_elegido):
    precio_elegido = producto_elegido[2]
    return precio_elegido
  



#Elegimos productos aleatorios, garantizando que al menos 2 tengan el mismo precio.
#De manera aleatoria se debera tomar el valor economico o el valor premium. Agregar al nombre '(economico)' o '(premium)'
#para que sea mostrado en pantalla.
def dameProductosAleatorios(producto, lista_productos, margen):

    #  Genero una lista de 7 productos (incluido el producto principal) 
    lista_aleatoria = generarListaProdAleatorios(producto, lista_productos)
    # Quiero garantizar que al menos 2 tengan precios similares
    while esUnPrecioValido(producto[2], lista_aleatoria, margen):
        lista_aleatoria = generarListaProdAleatorios(producto, lista_productos)

    def transformada(x):
            azar = random.randint(1,2)
            if azar == 1:
                return [x[0], "(Economico)", int(x[1])]
            else:
                return [x[0], "(Premium)", int(x[2])]
    lista_transformada = list(map(transformada, lista_aleatoria))
    return [producto] + lista_transformada
    
        
def index_producto_elegido(lista_productos, producto_elegido):
    index = 0
    for i in range(0, len(lista_productos)):
        if lista_productos[i][0] == producto_elegido[0]:
            index = i
            break
            
    return index

def generarListaProdAleatorios(producto, lista_productos):
    lista_copia = lista_productos[:]
    print(len(lista_copia))
    # Busco el producto de la copia de la lista de productos y lo remuevo
    lista_copia = list(filter(lambda x: producto[0] != x[0], lista_copia))
    nueva_lista = []
    while len(nueva_lista) < 6:
        index_azar = random.randint(0, len(lista_copia) - 1)
        nueva_lista.append(lista_copia[index_azar])
        lista_copia.pop(index_azar)
    return nueva_lista

# lista_productos = lectura()  
# producto = dameProducto(lista_productos, 1000)
# productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, 1000)
# producto2 = dameProducto(productos_en_pantalla[1:],1000)
# print(productos_en_pantalla)
# print(producto2)
# print(index_producto_elegido(productos_en_pantalla, producto2))