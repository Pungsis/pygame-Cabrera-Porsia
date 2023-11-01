from principal import *
from configuracion import *
import random
import math
from extras import *

# lee el archivo y carga en la lista lista_producto todas las palabras
def lectura2():
    lista = []
    archivo = open("./productos.txt")
    for linea in archivo:
        linea = linea[0:-1]
        lista.append(linea.split(","))
    archivo.close()
    return lista

print(lectura2())

def lectura():
    return [["Arroz", 1001, 1037],
            ["Yerba mate", 4546, 4904],
            ["Televisor Smart", 2055, 2439],
            ["Aceite de cocina", 3674, 4783],
            ["Mouse", 1635, 3603],
            ["Monitor de computadora", 2782, 2870],
            ["Silla de oficina", 3174, 4391],
            ["Lavadora", 3720, 4197],
            ["Refrigerador", 3352, 4533],
            ["Smartphone", 2070, 2224],
            ["Laptop", 4650, 4854],
            ["Cafetera", 2358, 3646],
            ["Batidora", 183, 4401],
            ["Microondas", 4254, 4624]]


#De la lista de productos elige uno al azar y devuelve una lista de 3 elementos, el primero el nombre del producto, el segundo si es economico
#o premium y el tercero el precio.
def buscar_producto(lista_productos):
    # producto = ["Silla de oficina", "(premium)", 4391]
    producto_azar = lista_productos[random.randint(0, len(lista_productos) - 1)]
    index = random.randint(1,2)
    precio = producto_azar[index]
    if index == 1:
        return [producto_azar[0], "(Economico)", precio]
    else:
        return [producto_azar[0], "(Premium)", precio]



#Elige el producto. Debe tener al menos dos productos con un valor similar
def dameProducto(lista_productos, margen):
    busqueda = []
    while len(busqueda) < 2:
        producto = lista_productos[random.randint(0,5)]
        if producto[1] == "(Premium)":
            busqueda = list(filter(lambda x: abs(producto[2] - x[2]) < margen, lista_productos))
        else:
            busqueda = list(filter(lambda x: abs(producto[2] - x[2]) < margen, lista_productos))
    return producto




#Devuelve True si existe el precio recibido como parametro aparece al menos 3 veces. Debe considerar el Margen.
def esUnPrecioValido(precio, lista_productos, margen):
    busqueda = list(filter(lambda x: abs(precio - x[1]) < margen or precio == x[1], lista_productos))
    return len(busqueda) >= 3


# Busca el precio del producto_principal y el precio del producto_candidato, si son iguales o dentro
# del margen, entonces es valido y suma a la canasta el valor del producto. No suma si eligió directamente
#el producto
def procesar(producto_principal, producto_candidato, margen):
    precio_principal = producto_principal[2]
    precio_candidato = producto_candidato[2]
    if precio_principal == precio_candidato or abs(precio_principal - precio_candidato) < margen:
        return producto_principal[2]
    else:
        return 0



#Elegimos productos aleatorios, garantizando que al menos 2 tengan el mismo precio.
#De manera aleatoria se debera tomar el valor economico o el valor premium. Agregar al nombre '(economico)' o '(premium)'
#para que sea mostrado en pantalla.
def dameProductosAleatorios(producto, lista_productos, margen):

    lista_copia = lista_productos[:]
    print(len(lista_copia))
    # Busco el producto de la copia de la lista de productos y lo remuevo
    lista_copia = list(filter(lambda x: producto[0] != x[0], lista_copia))
    print(len(lista_copia), producto[0])
    nueva_lista = []
    while len(nueva_lista) < 6:
        index_azar = random.randint(0, len(lista_copia) - 1)
        nueva_lista.append(lista_copia[index_azar])
        lista_copia.pop(index_azar)
    def transformada(x):
            azar = random.randint(1,2)
            if azar == 1:
                return [x[0], "(Economico)", x[1]]
            else:
                return [x[0], "(Premium)", x[2]]

    if esUnPrecioValido(producto[2], nueva_lista, margen): 
        lista_devolver = list(map(transformada, nueva_lista))
        return [producto] + lista_devolver
    else:
        lista_devolver = list(map(transformada, nueva_lista))
        return [producto] + lista_devolver
        
def index_producto_elegido(lista_productos, producto_elegido):
    index = 0
    for i in range(0, len(lista_productos)):
        if lista_productos[i][0] == producto_elegido[0]:
            index = i
            break
            
    return index


# lista_productos = lectura()  
# producto = dameProducto(lista_productos, 1000)
# productos_en_pantalla = dameProductosAleatorios(producto, lista_productos, 1000)
# producto2 = dameProducto(productos_en_pantalla[1:],1000)
# print(productos_en_pantalla)
# print(producto2)
# print(index_producto_elegido(productos_en_pantalla, producto2))