def records_helper():

    archivo_records = open("./datosRecords.txt")
    lista = []
    lista2 = []
    for linea in archivo_records:
        lista.append(int(linea[0:-1].split(",")[0]))
        lista2.append(linea[0:-1].split(",")[1])
  
    
    archivo_records.close()
    print(lista, lista2)
    return lista, lista2


def recordsDic(lista_puntajes, lista_apodos):
    copia_lista_puntajes = lista_puntajes[:]
    copia_lista_puntajes.sort(reverse=True)
    diccionario = {}

    for i in range(0, len(copia_lista_puntajes)):

        for j in range(0, len(lista_puntajes)):
            if copia_lista_puntajes[i] == lista_puntajes[j]:
                diccionario[str(i + 1)] = [copia_lista_puntajes[i], lista_apodos[j]]
                # lista.append([copia_lista_puntajes[i], lista_apodos[j]])
                lista_puntajes.pop(j)
                lista_apodos.pop(j)
                print(lista_apodos)
                break
    return diccionario


def write_records(dic):
    file = open("./records.txt", "w")
    contador = 0
    for x, y in dic.items():
        file.write(f"{x}            {y[1]}              {y[0]}\n")
        contador += 1
        if contador == 10:
            break

    file.close()
    

# diccionario_record = recordsDic(records_helper()[0], records_helper()[1])

# print(write_records(diccionario_record))

def write_in_record(puntos, apodo):
    file = open("./datosRecords.txt", "a")
    file.write("\n")
    apodo = apodo.split(" ")
    apodo = "".join(apodo)

    file.write(f"{str(puntos)},{apodo} ")

    file.close()

# write_in_record(19923, "K A N")