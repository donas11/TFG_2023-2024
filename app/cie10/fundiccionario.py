from bs4 import BeautifulSoup
from cie10 import *
from cie10 import manager
import cie10
import xml.etree.ElementTree as diccionario
from copy import deepcopy
# Función que lee el contenido del token hasta que el token cambie
def leer_token(siguiente,token):
    contenido=""
    while token in siguiente['class']:
        # texto_padre = ''.join(siguiente.stripped_strings)
        texto_padre = siguiente.find(text=True, recursive=False)
        if str(texto_padre) not in contenido and texto_padre is not None:   
            contenido+=str(texto_padre)
        siguiente = siguiente.find_next()
        while "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
    return siguiente,contenido  

# Función que lee el contenido del token hasta que el token cambie con control de finalización
def leer_token_confinalizacion(siguiente,token,cont_finalizar,final):
    contenido=""
    while token in siguiente['class']:  
        texto_padre = siguiente.find(text=True, recursive=False)
        # texto_padre = ''.join(siguiente.stripped_strings)
        if str(texto_padre) not in contenido and texto_padre is not None:   
            contenido+=str(texto_padre)
        siguiente = siguiente.find_next()
        while "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
            cont_finalizar+=1
            if cont_finalizar > final:
                return siguiente,contenido,cont_finalizar
    return siguiente,contenido,cont_finalizar
# Función que lee el contenido del token con Descripcición hasta que el token cambie
def leer_tokencondescripcion(siguiente,token):
    contenido=""
    tokendescripcion= token+"-Descripcion"
    while token in siguiente['class']: 
        texto_padre = siguiente.find(text=True, recursive=False)
        # texto_padre = ''.join(siguiente.stripped_strings)
        if str(texto_padre) not in contenido and texto_padre is not None:   
            contenido+=str(texto_padre)
        siguiente = siguiente.find_next()
        while tokendescripcion in siguiente['class']:
            texto_padre = siguiente.find(text=True, recursive=False)
            # texto_padre = ''.join(siguiente.stripped_strings)
            if str(texto_padre) not in contenido and texto_padre is not None:  
                contenido+=str(texto_padre)
            siguiente = siguiente.find_next()
            while "Pie-de-pagina" in siguiente['class']:
                siguiente = siguiente.find_next()
    return siguiente,contenido

# Función que lee el contenido del token con Descripcición hasta que el token comprobando que hay Pie-de-pagina 
def leer_tokencondescripcionext(siguiente,token):
    contenido=""
    tokendescripcion= token+"-Descripcion"
    while token in siguiente['class']:      
        texto_padre = siguiente.find(text=True, recursive=False)
        # texto_padre = ''.join(siguiente.stripped_strings)
        if str(texto_padre) not in contenido and texto_padre is not None:   
            contenido+=str(texto_padre)            
        siguiente = siguiente.find_next()
        while "Pie-de-pagina" in siguiente['class']:
                siguiente = siguiente.find_next()
        while tokendescripcion in siguiente['class']:
            texto_padre = siguiente.find(text=True, recursive=False)
            # texto_padre = ''.join(siguiente.stripped_strings)
            if str(texto_padre) not in contenido and texto_padre is not None:   
                contenido+=str(texto_padre)
            siguiente = siguiente.find_next()
            while "Pie-de-pagina" in siguiente['class']:
                siguiente = siguiente.find_next()
    return siguiente,contenido

# Función para asignar sublemento al elemento padre y su contenido
def asignar_contenido(raiz,sublemento,subelemento_contenido,contador_subelementos,nombre_elemento,nombre_contenido):
    contador_subelementos+=1                                           # Aumentamos el contador de capitulo 
    nom_var_subelemento= f"{nombre_elemento}{contador_subelementos}"   # Asignamos nombre a la variable
    if(isinstance(raiz, dict)):                                        # Comprobamos que es instancia 
        clavesdict= list(raiz.keys())
        sublemento[nom_var_subelemento] = diccionario.SubElement(raiz[clavesdict[0]], nombre_elemento)      # añadimos un sublemento al diccinario <cie10> <nombre_elemento>
    else:
        sublemento[nom_var_subelemento] = diccionario.SubElement(raiz, nombre_elemento)      # añadimos un sublemento al diccinario <cie10> <nombre_elemento>
    sublemento[nom_var_subelemento].set(nombre_contenido,subelemento_contenido)              # Asignamos en el diccionario <cie10> <capitulo nombre_contenido="subelemento_contenido">
    subelemento_contenido=""                              # vaciamos variable 
    # final_capitulo=1   
    return raiz,sublemento,nom_var_subelemento,subelemento_contenido,contador_subelementos

# Función para asignar sublemento al elemento padre
def asignar(raiz,subelemento,contador_subelementos,titulo_elemento):
    nom_var_subelemento= f"{titulo_elemento}{contador_subelementos}"                  # Asignamos nombre a la variable
    subelemento[nom_var_subelemento] = diccionario.SubElement(raiz, titulo_elemento)  # Asignamos suelemento al elemento
    return raiz,subelemento,nom_var_subelemento

# Función para asignar referencias (sublementos) al elemento padre
def asignar_lista_referencia(lista_referencia,subelemento,contador_subelemento,elemento,non_referencia_elem,titulo,subtitulo):
    for referencia in lista_referencia:
        contador_subelemento+=1
        nombre_referencia = f"{subtitulo}{contador_subelemento}"
        subelemento[nombre_referencia]=diccionario.SubElement(elemento[non_referencia_elem],subtitulo+"_"+titulo)
        subelemento[nombre_referencia].set(subtitulo,referencia[1])
        subelemento[nombre_referencia].text=referencia[0] + " " + referencia[1]
    return subelemento,elemento,contador_subelemento

# Función para asignar especificación (sublemento) al elemento padre con su contenido
def asignar_especificacion(raiz,sublemento,subelemento_contenido,contador_subelementos,titulo_elemento):
    contador_subelementos+=0   
    nom_var_subelemento= f"{titulo_elemento}{contador_subelementos}"
    sublemento[nom_var_subelemento] =diccionario.SubElement(raiz,titulo_elemento)
    sublemento[nom_var_subelemento].text=subelemento_contenido
    return sublemento,nom_var_subelemento,subelemento_contenido,contador_subelementos

# Función para asignar especificación (sublemento) al elemento padre con su contenido
def asignar_especificacion_consubtitulo(raiz,sublemento,subelemento_contenido,contador_subelementos,subtitulo_elemento,titulo):
    contador_subelementos+=0
    nom_var_subelemento= f"{subtitulo_elemento}-{titulo}{contador_subelementos}"
    sublemento[nom_var_subelemento] =diccionario.SubElement(raiz,subtitulo_elemento)
    sublemento[nom_var_subelemento].text=subelemento_contenido
    return sublemento,nom_var_subelemento,subelemento_contenido,contador_subelementos

# Lista de funciones de busqueda de referencias
buscar_ref_enf_nivel =[manager.buscar_ref_enfermedades_en_enfermedades_nivel0,manager.buscar_ref_enfermedades_en_enfermedades_nivel1,manager.buscar_ref_enfermedades_en_enfermedades_nivel2]

# Función para asignar subelemento al elemento padre con su contenido
def asignar_elemento_nivel(contador_subelemento,subelemento,titulo_subelemento,cod_nivel,nivel,siguiente,elemento):
    contador_subelemento+=1
    nombre_subelemento = f"{titulo_subelemento}{contador_subelemento}"
    cod_nivel= buscar_ref_enf_nivel[nivel](siguiente.text)
    subelemento[nombre_subelemento]= diccionario.SubElement(elemento,titulo_subelemento)
    return contador_subelemento,nombre_subelemento,subelemento,cod_nivel,elemento

# Función para asignar Codigos de la enfermedad y asignar si es Actualizada o no
def asignar_codigo(siguiente, nombre_subelemento, subelemento,control_nv,cod_nivel,actualizado):
    for codniv in cod_nivel:
        subelemento[nombre_subelemento].set("Codigo",codniv)
        if actualizado == 1:
                subelemento[nombre_subelemento].set("Actualizado","cierto")
        Enfermedad=siguiente.text
        codigo = codniv
        EnfermedadN = Enfermedad.replace(codigo,"")
        subelemento[nombre_subelemento].text=EnfermedadN
        siguiente = siguiente.find_next()
        control_nv=1
    return  siguiente,subelemento,nombre_subelemento,control_nv




