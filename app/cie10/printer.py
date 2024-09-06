def imprimir_lista_capitulos(lista_elementos,archivo,tam,final):
    print("===================capitulos=================================\n")
    for elem in lista_elementos:   
        #print(str(elem)+"\n")
        print(archivo[elem:elem+tam]+";"+archivo[elem+tam:elem+tam+final]+"\n")
    print("=============================================================\n\n")

def imprimir_lista(lista_elementos,title):
    print("==================="+title+"=================================\n")
    for elem in lista_elementos:   
        print(str(elem)+"\n")
    print("=============================================================\n\n")

def imprimir_lista(lista_elementos,archivo,title):
    print("==================="+title+"=================================\n")
    for elem in lista_elementos:   
        # print(str(elem)+"\n")
        print(archivo[elem[0]:elem[1]]+"\n")
    print("=============================================================\n\n")

