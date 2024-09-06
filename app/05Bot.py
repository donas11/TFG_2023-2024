from PyPDF2 import PdfReader, PdfWriter
from bs4 import BeautifulSoup
import urllib.request
import subprocess
import time
from config import MONGODB_URL, DATABASE_NAME,PUERTO
import xml.etree.ElementTree as diccinario
from cie10 import *
from cie10 import filerwpe
from cie10 import manager
from cie10 import printer
from pymongo import MongoClient

# Asignamos el tiempo de inicio
start_time = time.time()


# Paso 00

# Funcion de llamada a Libreria pdf2htmlEX en el sistema
def convert_pdf_to_html(input_file, output_file):
    subprocess.call(['pdf2htmlEX', input_file, output_file])

# Variables de url,archivos de entrada o salida, numero de la pagina que nos interesa
url_pdffile='https://www.sanidad.gob.es/estadEstudios/estadisticas/normalizacion/CIE10/CIE10ES_2018_diag_pdf_20180202.pdf'
output_pdffile='./.CIE10ES_2018_diag_pdf_20180202LT.pdf'
input_pdffilem='./.CIE10ES_2018_diag_pdf_20180202LT.pdf'
output_htmlfile = "./CIE10LT.html"
page_num=659

# # # Abrimos archivo
archivo, header = urllib.request.urlretrieve(url_pdffile)

# Extraer pdf de la Lista Tabular de Enfermedades
with open(archivo, "rb") as f:
    pdf_reader = PdfReader(f)
    num_pages = len(pdf_reader.pages)
    pdf_writer = PdfWriter()  
    for page in range(page_num, num_pages):
    	pdf_writer.add_page(pdf_reader.pages[page])
    with open(output_pdffile, 'wb') as file1:
        pdf_writer.write(file1)


# # Convertimos PDF a HTML
#   sudo docker run -v "$(pwd):/pdf" bwits/pdf2htmlex pdf2htmlEX /pdf/archivo.pdf /pdf/salida.html
# convert_pdf_to_html(input_pdffilem, output_htmlfile)
convert_pdf_to_html(archivo, output_htmlfile)


#Paso 01
subprocess.call(['python','01preprocessHTML.py'])
# ruta_salida1="CIE10LTP16EFN2.html" 


# #Paso 02
subprocess.call(['python','02preHTML.py'])
# ruta_salida1="CIE10LTPclasses.html"


# Paso 03
# ruta_entrada="CIE10LTPclasses.html"
subprocess.call(['python','03Mod_diccionario'])
# ruta_salida="diccionario.xml"


# Paso 04
#Nombre de archivo de entrada 
ruta_entrada="diccionario.xml"
# Leemos el contenido del Archivo
contenido= filerwpe.leer_archivo(ruta_entrada)
# Parcheamos el archivo a Soup
soup= filerwpe.parchear_archivo_xml(contenido)


client = MongoClient(MONGODB_URL, PUERTO)
db = client[DATABASE_NAME]
collection_secciones = db['SECCION']  # SECCION(ID,Nombre,Aclaracion) ✅ 
collection_enfermedades = db['ENFERMEDAD']  #  ENFERMEDAD(Codigo,Nombre, Aclaracion) ✅ 
#collection_enfermedad_excluye = db['ENFERMEDAD_EXCLUYE'] #  ENFERMEDAD_EXCLUYE(ID,tipo,DESCRIPCION) ✅
#collection_enfermedad_excluye_enfermedad = db['ENFERMEDAD_EXCLUYE_ENFERMEDAD'] # ENFERMEDAD_REFERENCIA_ENFERMEDAD(ID_excluye,Codigo_Enfermedad,CodRef_Enfermedad) ✅
#collection_enfermedad_excluye_seccion = db['ENFERMEDAD_EXCLUYE_SECCION'] # ENFERMEDAD_REFERENCIA_SECCION(ID_excluye,Codigo_Enfermedad,ID_Seccion)  ✅





enfermedad_nivel0_actualizado = soup.find_all("Enfermedad-Nivel0", {"Actualizado": "cierto"})

nombre_enfermedadn0=""
nombre_enfermedadn1=""
nombre_enfermedadn2=""
aclaracion_enfermedadn0=""
aclaracion_enfermedadn1=""
aclaracion_enfermedadn2=""




for elem in enfermedad_nivel0_actualizado:
    # Codigo de Enfermedad (Codigo)
    codigo_enfermedadn0 = elem.get('Codigo')

    


    # (NOMBRE)
    nombre_enfermedadn0 +=elem.text

    
    #Leemos toda la descripcion de Enfermedad (ACLARACIÓN)
    deeescripcigsgsdfgsones= elem.find_all('Descripcion') 
    if deeescripcigsgsdfgsones is not None:
        for descripcion_elem in elem.find_all('Descripcion'):
            if descripcion_elem.find('Descripcion') is not None:
                aclaracion_enfermedadn0 += descripcion_elem.text

    #Leemos toda la Nota de la enfermedad (ACLARACIÓN)
    for nota_elem in elem.find_all('Nota'):
        aclaracion_enfermedadn0 += nota_elem.text

    #Leemos todas las todos los Codifique_Primero (ACLARACIÓN)
    for codifique_elem in elem.find_all('Codifique_Primero'):
        if codifique_elem.find('Codifique_Primero') is not None:
            aclaracion_enfermedadn0 += codifique_elem.find('Codifique_Primero').text
        #Leemos todas las todas las Referencias  (ACLARACIÓN)
        for referencias in codifique_elem.find_all('Referencia_enfermedad'):
            if referencias.find('Referencia_enfermedad') is not None:
                aclaracion_enfermedadn0 += referencias.find('Referencia_enfermedad').text

    #Leemos todas las todos los Utilice_Codigo_adicional (ACLARACIÓN)
    for codadicional_elem in elem.find_all('Utilice_Codigo_adicional'):
        if codadicional_elem.find('Utilice_Codigo_adicional') is not None:
            aclaracion_enfermedadn0 += codadicional_elem.find('Utilice_Codigo_adicional').text
        #Leemos todas las todas las Referencias (ACLARACIÓN)
        for referencias in codadicional_elem.find_all('Referencia_enfermedad'):
            if referencias.find('Referencia_enfermedad') is not None:
                aclaracion_enfermedadn0 += referencias.find('Referencia_enfermedad').text

    for incluye_elem in elem.find_all('Incluye'):
        #Leemos toda la descripcion del incluye (DESCRIPCIION)
        aclaracion_enfermedadn0+=  incluye_elem.text

        for descripcion_elemenfermedadn0_elem in incluye_elem.find_all('Descripcion'):
            aclaracion_enfermedadn0+=  descripcion_elem.text
            aclaracion_enfermedadn0+= descripcion_elem.find('Descripcion').text

    # Formateamos la inserción ENFERMEDAD(Codigo,Nombre, Aclaracion)
    data_enfermedad_nivel0={
        'Codigo':codigo_enfermedadn0,
        'Nombre':nombre_enfermedadn0, 
        'Aclaracion':aclaracion_enfermedadn0
    }
    # Actualizamos en db['ENFERMEDAD']
    actualizado= collection_enfermedades.update_one({'Codigo': codigo_enfermedadn0},{"$set":data_enfermedad_nivel0})
    if actualizado.modified_count < 1:
        collection_enfermedades.insert_one(data_enfermedad_nivel0)


    
    # reiniciamos variable
    nombre_enfermedadn0=""
    aclaracion_enfermedadn0=""


        

  

enfermedad_nivel1_actualizado = soup.find_all("Enfermedad-Nivel1", {"Actualizado": "cierto"})
for elem in enfermedad_nivel1_actualizado:
    
    # Codigo de Enfermedad (Codigo)
    codigo_enfermedadn1 = elem.get('Codigo')
    
    # ENFERMEDAD(Codigo,Nombre, Aclaracion)
    # Codigo de Enfermedad (Codigo)
    codigo_enfermedadn1 = elem.get('Codigo')
    # (NOMBRE)
    nombre_enfermedadn1 +=elem.text

    #Leemos toda la descripcion de Enfermedad (ACLARACIÓN)
    for descripcion_elem in elem.find_all('Descripcion'):
        aclaracion_enfermedadn1 += descripcion_elem.text

    #Leemos toda la Nota de la enfermedad (ACLARACIÓN)
    for nota_elem in elem.find_all('Nota'):
        aclaracion_enfermedadn1 += nota_elem.text


    #Leemos todas las todos los Codifique_Primero (ACLARACIÓN)
    for codifique_elem in elem.find_all('Codifique_Primero'):
        if codifique_elem.find('Codifique_Primero') is not None:
            aclaracion_enfermedadn1 += codifique_elem.find('Codifique_Primero').text
        #Leemos todas las todas las Referencias  (ACLARACIÓN)
        for referencias in codifique_elem.find_all('Referencia_enfermedad'):
            if referencias.find('Referencia_enfermedad') is not None:
                aclaracion_enfermedadn1 += referencias.find('Referencia_enfermedad').text

    #Leemos todas las todos los Utilice_Codigo_adicional (ACLARACIÓN)
    for codadicional_elem in elem.find_all('Utilice_Codigo_adicional'):
        if codadicional_elem.find('Utilice_Codigo_adicional') is not None:
            aclaracion_enfermedadn1 += codadicional_elem.find('Utilice_Codigo_adicional').text
        #Leemos todas las todas las Referencias (ACLARACIÓN)
        for referencias in codadicional_elem.find_all('Referencia_enfermedad'):
            if referencias.find('Referencia_enfermedad') is not None:
                aclaracion_enfermedadn1 += referencias.find('Referencia_enfermedad').text

    for incluye_elem in elem.find_all('Incluye'):
        aclaracion_enfermedadn1+=  incluye_elem.text

        for descripcion_elem in incluye_elem.find_all('Descripcion'):
            aclaracion_enfermedadn1+=  descripcion_elem.text

    # Formateamos la inserción ENFERMEDAD(Codigo,Nombre, Aclaracion)
    data_enfermedad_nivel1={
        'Codigo':codigo_enfermedadn1,
        'Nombre':nombre_enfermedadn1, 
        'Aclaracion':aclaracion_enfermedadn1
    }
    
    # Actualizamos en db['ENFERMEDAD']
    actualizado= collection_enfermedades.update_one({'Codigo': codigo_enfermedadn1},{"$set":data_enfermedad_nivel1})
    if actualizado.modified_count < 1:
        collection_enfermedades.insert_one(data_enfermedad_nivel1)
    # reiniciamos variable
    nombre_enfermedadn1=""
    aclaracion_enfermedadn1=""
    
    


enfermedad_nivel2_actualizado = soup.find_all("Enfermedad-Nivel2", {"Actualizado": "cierto"})
for elem in enfermedad_nivel2_actualizado:
# Codigo de Enfermedad (Codigo)
   
    codigo_enfermedadn2 = elem.get('Codigo')
    enfermedadencontrada = collection_enfermedades.find_one({'Codigo': codigo_enfermedadn0})


    # (NOMBRE)
    nombre_enfermedadn2 +=elem.text

    #Leemos toda la descripcion de Enfermedad (ACLARACIÓN)
    for descripcion_elem in elem.find_all('Descripcion'):
        if descripcion_elem.find('Descripcion') is not None:
            aclaracion_enfermedadn2 += descripcion_elem.text

    #Leemos toda la Nota de la enfermedad (ACLARACIÓN)
    for nota_elem in elem.find_all('Nota'):
        aclaracion_enfermedadn2 += nota_elem.text

    #Leemos todas las todos los Codifique_Primero (ACLARACIÓN)
    for codifique_elem in elem.find_all('Codifique_Primero'):
        if codifique_elem.find('Codifique_Primero') is not None:
            aclaracion_enfermedadn2 += codifique_elem.find('Codifique_Primero').text
        #Leemos todas las todas las Referencias  (ACLARACIÓN)
        for referencias in codifique_elem.find_all('Referencia_enfermedad'):
            if referencias.find('Referencia_enfermedad') is not None:    
                aclaracion_enfermedadn2 += referencias.find('Referencia_enfermedad').text

    #Leemos todas las todos los Utilice_Codigo_adicional (ACLARACIÓN)
    for codadicional_elem in elem.find_all('Utilice_Codigo_adicional'):
        aclaracion_enfermedadn2 += codadicional_elem.find('Utilice_Codigo_adicional').text
        #Leemos todas las todas las Referencias (ACLARACIÓN)
        for referencias in codadicional_elem.find_all('Referencia_enfermedad'):
                aclaracion_enfermedadn2 += referencias.find('Referencia_enfermedad').text

    for incluye_elem in elem.find_all('Incluye'):
        #Leemos toda la descripcion del incluye (DESCRIPCIION)
        aclaracion_enfermedadn2+=  incluye_elem.text

        for descripcion_elem in incluye_elem.find_all('Descripcion'):
            aclaracion_enfermedadn2+=  descripcion_elem.text
            aclaracion_enfermedadn2+= descripcion_elem.find('Descripcion').text

    # Formateamos la inserción ENFERMEDAD(Codigo,Nombre, Aclaracion)
    data_enfermedad_nivel2={
        'Codigo':codigo_enfermedadn2,
        'Nombre':nombre_enfermedadn2, 
        'Aclaracion':aclaracion_enfermedadn2
    }
    # Actualizamos en db['ENFERMEDAD']
    actualizado= collection_enfermedades.update_one({'Codigo': codigo_enfermedadn2},{"$set":data_enfermedad_nivel2})
    if actualizado.modified_count < 1:
        collection_enfermedades.insert_one(data_enfermedad_nivel2)
    # reiniciamos variables
    nombre_enfermedadn2=""
    aclaracion_enfermedadn2=""
        
        
# Asignamos el tiempo final
end_time = time.time()

# Imprimimos tiempo que ha tardado
print(f"Tiempo de ejecución: {end_time - start_time} segundos")
                
    



                        # Actualización
# fc1 sc4
# fs3 fc1



# elementos_modificados = soup.find_all(class_="fc1 sc4")

# for elem in elementos_modificados:
    
#     print(elem)
#     print("\n")






