from bs4 import BeautifulSoup

# Función para leer de archivo
def leer_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read()
    return contenido  

# Función para escribir en archivo
def escribir_archivo(ruta_salida1,archivo_completo):
    with open(ruta_salida1, 'w') as archivo_salida:
        archivo_salida.write(archivo_completo)

# Función para extraer contenido del archivo html
def parchear_archivo(contenido):
    soup = BeautifulSoup(contenido, 'html.parser')
    return soup

# Función para extraer contenido del archivo xml
def parchear_archivo_xml(contenido):
    soup = BeautifulSoup(contenido, 'xml')
    return soup

# Función para extraer el contenido de la class que empieza por "t"
def extraer_class(soup):
    lista_class = soup.find_all(class_="t")
    return lista_class

# Función para crear archivo del contenido del archivo en un determinado formato
def archivar_lista(lista_elementos,archivo,title,nombre_archivo):
    with open(nombre_archivo, 'w') as archivo_salida:
        archivo_salida.write("==================="+title+"=================================\n")
        for elem in lista_elementos:   
            archivo_salida.write(archivo[elem[0]:elem[1]]+"\n")
        archivo_salida.write("=============================================================\n\n")

# Función para crear archivo del contenido del archivo
def archivar_completo(archivo,nombre_archivo):
    with open(nombre_archivo, 'w') as archivo_salida:   
        archivo_salida.write(archivo+"\n")
        
# Función para crear archivo de la lista con saltos de linea 
def escribir_archivo_saltos(ruta_salida1,lista_elementos):
    with open(ruta_salida1, 'w') as archivo_salida:
        for elem in lista_elementos:   
            archivo_salida.write(str(elem)+"\n")

# Función para crear archivo del contenido de la lista con saltos de linea 
def escribir_archivo_saltos_elem(ruta_salida1,lista_elementos):
    with open(ruta_salida1, 'w') as archivo_salida:
        for elem in lista_elementos:   
            archivo_salida.write(str(elem.text)+"\n")

# Función para crear archivo del contenido de la lista[3] con saltos de linea 
def escribir_archivo_saltos_elemento(ruta_salida1,lista_elementos):
    with open(ruta_salida1, 'w') as archivo_salida:
        for elem in lista_elementos:   
            archivo_salida.write(str(elem[3])+"\n")