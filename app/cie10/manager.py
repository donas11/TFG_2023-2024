import re
from cie10 import *
from cie10 import filerwpe
import cie10

# variables de tamaños:
global tam_cod_capitulos 
global tam_inicio_seccion 
global tam_seccion 
global tam_codigocapitulosfin 
global tam_indice_seccion
# variables de patrones:
global patron_capitulos1d 
global patron_capitulos2d  
global patron_capitulosinicio 
global patron_capitulosfin 
global patron_codigo_secciones 
global patron_secciones
global patron_secciones2 
global patron_codigo0
global patron_codigo1
global patron_codigo2
global patron_en0
global patron_en1
global patron_en2
global patron_inicio_seccion
global patron_excluye1
global patron_excluye
global patro_incluye
global patron_extension
global patron_extension2
global patron_mas0
global patron_mas1
global patron_mas2



# PATRONES DE CAPITULOS
patron_capitulos1d = ('CAPÍTULO [0-9]\.') #11(tamaño)
patron_capitulos2d = ('CAPÍTULO [0-9][0-9]\.') #12(tamaño) 
patron_capitulos = r'(CAPÍTULO [0-9][0-9]\.|CAPÍTULO [0-9]\.)'
patron_capitulosinicio = ('[A-Z][0-9][0-9]\-[A-Z][0-9][0-9]') #r"[A-Z]\d{2}-[A-Z]\d{2}" #7
patron_capitulosfin = ('\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)') #r"[A-Z]\d{2}-[A-Z]\d{2}" #9
patron_capitulos_completos = r'CAPÍTULO\s([0-9]|[0-9][0-9]).\s([A-ZÁÉÍÓÚÜ]+(\s[A-ZÁÉÍÓÚÜ]+)*)\s(\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)|\([A-Z][0-9][0-9]\))'
patron_point = 'CAPÍTULO [0-9].\s([A-ZÁÉÍÓÚÜÑ]+(\s[A-ZÁÉÍÓÚÜÑ]+)*)\s(\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)|\([A-Z][0-9][0-9]\))'
patron_point1 = 'CAPÍTULO [0-9][0-9].\s([A-ZÁÉÍÓÚÜÑ]+(\s[A-ZÁÉÍÓÚÜÑ]+)*)\s(\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)|\([A-Z][0-9][0-9]\))'

# PATRONES DE SECCIONES
patron_inicio_seccion="Este capítulo contiene las siguientes secciones:" #48
patron_codigo_secciones = ('[A-Z][0-9][0-9]')    #3
patron_secciones=('[A-Z\s]+\s\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)') #'\s[A-Z\s]+\s\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)'
patron_secciones2=('\s[A-Z\s]+\s\([A-Z][0-9][0-9]\)')
patron_secciones_completos = r'([A-ZÁÉÍÓÚÜÑ]+(\s[A-ZÁÉÍÓÚÜÑ]+)*)\s(\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)|\([A-Z][0-9][0-9]\))' #mayusculas y mayusculas con acentos y termina con el código   
# PATRONES DE CONJUNTOS 
patron_codigo0 = ('\s[A-Z][0-9][0-9]\s((?!Incluye|Excluye|[A-Z][0-9]|[4-7]º)[A-Za-zÁ-Úá-úüñ0-9,]+[ ]?)+')   #  
patron_codigo1 = ('[A-Z][0-9][0-9].[0-9]\s((?!Incluye|Excluye|[A-Z][0-9]|[4-7]º)[A-Za-zÁ-Úá-úüñ0-9,]+[ ]?)+')  #5
patron_codigo2 = ('[A-Z][0-9][0-9].[0-9][0-9]\s((?!Incluye|Excluye|[A-Z][0-9]|[4-7]º)[A-Za-zÁ-Úá-úüñ0-9,]+[ ]?)+') #6
# PATRONES DE ENFERMEDADES
patron_en0=('[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])')
patron_en1=('[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])\.([0-9]|[A-Z])')
patron_en2=('[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])\.(([0-9]|[A-Z])([A-Z]|[0-9]))')
patron_en2_subnivel=('[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])\.([0-9]|[A-Z])([A-Z]|[0-9])([A-Z]|[0-9])')
patron_referencia=r"\([A-Z][0-9]{2}.*?\)"
patron_referencia_basica=r"\-[A-Z]" 
# PATRON DE EXCLUYES
patron_excluye=r'\sExcluye 1:\s((?!(Excluye 2)|[0-9][0-9][0-9]\sLista\sTabular\sEnfermedades\s|[A-Z][0-9])[A-Za-zÁ-Úá-úüñ0-9,\n]+[ ]?)+'
patron_excluye1=r'\s\bExcluye 2:\b\s((?![0-9][0-9][0-9]\sLista\sTabular\sEnfermedades\s|[A-Z][0-9])[A-Za-zÁ-Úá-úüñ0-9,\n]+[ ]?)+'
# PATRON DE INCLUYE
patro_incluye=r'\sIncluye:\s((?![0-9][0-9][0-9]\sLista\sTabular\sEnfermedades\s|Excluye|[A-Z][0-9])[A-Za-zÁ-Úá-úüñ0-9,\n]+[ ]?)+' # (?!([A-ZÁÉÍÓÚÜ]+)|([4-7º])|\s([0-9][0-9][0-9]\sLista\sTabular\sEnfermedades))
# PATRONES DE INFORMACIÓN ADICIONAL
patron_inicio_seccion="Este capítulo contiene las siguientes secciones:" #48
patron_mas0="Codifique primero:"
patron_mas1="Utilice código adicional"
patron_mas2="Nota:"
# PATRON DE ACTUALIZACIONES
patron_extension=('[4-7]º')
patron_extension2=('[4-7]º+')
# PATRONES ESPECIALES muy concretas:
patron_neom = r'(([A-Z])|NEOM)\s\([A-Z][0-9][0-9]\)'
patron_letras=r"\b[A-Z][a-zA-Z]+\s*?\("



# Inicialización de variables 
tam_cod_capitulos = 12 
tam_inicio_seccion = 2778  # tamaño max
tam_seccion = 200  # tamaño max
tam_codigocapitulosfin = 9
tam_indice_seccion = 48


#funcion para unir todo el texto
def unir_contenido(lista_class,lista_contenido,posicion_final):
    for elementc in lista_class:
        lista_contenido.append(elementc.getText())
    archivo_completo= ' '.join(lista_contenido)
    posicion_final= len(archivo_completo)
    return archivo_completo,lista_contenido,posicion_final


#
#                CAPITULOS
#
def buscar_indices_capitulos(archivo_completo): 
    lista_indice_capitulosall= [coincidencia.start() for coincidencia in re.finditer(patron_capitulos, archivo_completo)] 
    lista_indice_capitulos = [coincidencia.start() for coincidencia in re.finditer(patron_capitulos1d, archivo_completo)]
    lista_indice_capitulos2d = [coincidencia.start() for coincidencia in re.finditer(patron_capitulos2d, archivo_completo)]
    return lista_indice_capitulos,lista_indice_capitulos2d,lista_indice_capitulosall



def buscar_capitulos(coincidencias_capis,lista_contenido):
    for id,elemento in enumerate(lista_contenido):
        coincidencias_elemento = [(coincidencia.start(),coincidencia.end(),id,elemento) for coincidencia in re.finditer(patron_capitulos1d, str(elemento) )]
        coincidencias_capis.extend(coincidencias_elemento)
        coincidencias_elemento = [(coincidencia.start(),coincidencia.end(),id,elemento) for coincidencia in re.finditer(patron_capitulos2d, str(elemento) )]
        coincidencias_capis.extend(coincidencias_elemento)
    return coincidencias_capis


def buscar_capitulos_completos(archivo_completo,lista_contenido):
    
    
    coincidencias_elemento = [(coincidencia.start(),coincidencia.end()) for coincidencia in re.finditer(patron_capitulos_completos, archivo_completo )]    
    
    return coincidencias_elemento

 
    

###
###              LISTAS
###
def extraer_neom(lista_codigos_secciones,lista_codigos_sec_neom):
    
    lista_codigos_final=list(set(lista_codigos_secciones) - set(lista_codigos_sec_neom))
    lista_codigos_final.sort()
    return lista_codigos_final


###
###           SECCIONES QUE NO SON SECCIONES EN CAPITULOS
###



def Lista_de_secciones_que_no_son(archivo_completo,lista_indice_capitulos):
    lista_secciones_que_no_son_secciones=list()

    for id,elemento in enumerate(lista_indice_capitulos):
        coincidencia = [(elemento[0]+coincidencia.start()+12,elemento[1]) for coincidencia in re.finditer(patron_point, archivo_completo[elemento[0]:elemento[1]] )]    
        lista_secciones_que_no_son_secciones.extend(coincidencia)
        coincidencia = [(elemento[0]+coincidencia.start()+13,elemento[1]) for coincidencia in re.finditer(patron_point1, archivo_completo[elemento[0]:elemento[1]] )]    
        lista_secciones_que_no_son_secciones.extend(coincidencia)
    return lista_secciones_que_no_son_secciones


def extraer_secc_no_son(lista_codigos_secciones,lista_codigos_sec_no_son):
    lista_codigos_final=list(set(lista_codigos_secciones) - set(lista_codigos_sec_no_son))
    lista_codigos_final.sort()    
    return lista_codigos_final



#
#               SECCIONES
#
def buscar_secciones_completos(archivo_completo,lista_indice_capitulos,posicion_final):
      
    lista_secciones=list()
    lista_no_especificado_de_otra_manera=list()
    for id,elemento in enumerate(lista_indice_capitulos):
        if id+1 < len(lista_indice_capitulos):
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_secciones_completos, archivo_completo[elemento[0]:lista_indice_capitulos[id+1][0]] )]    
            coincidencia_neom= [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_neom, archivo_completo[elemento[0]:lista_indice_capitulos[id+1][0]] )]    
            lista_no_especificado_de_otra_manera.extend(coincidencia_neom)
            lista_secciones.extend(coincidencia)

        else:
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_secciones_completos, archivo_completo[elemento[0]:posicion_final] )]    
            coincidencia_neom= [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_neom, archivo_completo[elemento[0]:posicion_final] )]               
            lista_no_especificado_de_otra_manera.extend(coincidencia_neom)
            lista_secciones.extend(coincidencia)

    return lista_secciones,lista_no_especificado_de_otra_manera


def buscar_secciones(inicio_capitulo,final_capitulo,lista_contenido):
    coincidencias_elemento= list()
    lista_secciones=list()
    for i in range(inicio_capitulo,final_capitulo):
        coincidencias_elemento = [(coincidencia.start(),coincidencia.end(),i,lista_contenido[i]) for coincidencia in re.finditer(patron_secciones, lista_contenido[i])]
        lista_secciones.extend(coincidencias_elemento)
        coincidencias_elemento = [(coincidencia.start(),coincidencia.end(),i,lista_contenido[i]) for coincidencia in re.finditer(patron_secciones2, lista_contenido[i])]
        lista_secciones.extend(coincidencias_elemento)
    return lista_secciones



def buscar_capitulos_en_secciones(coincidencias_capis,lista_secciones,lista_contenido,posicion_final):
    lista_secciones.clear()
    Lista_de_secciones=list()
    for id,elemento in enumerate(coincidencias_capis):
        print(str(elemento)+"\n")
        if id+1 < len(coincidencias_capis):
            lista_secciones=buscar_secciones(elemento[2],coincidencias_capis[id+1][2],lista_contenido)
            Lista_de_secciones.append([lista_secciones])
            lista_secciones.clear()    
        else:
            lista_secciones=buscar_secciones(elemento[2],posicion_final,lista_contenido)
            Lista_de_secciones.append([lista_secciones])
            lista_secciones.clear()
    return Lista_de_secciones


def buscar_indice_secciones(archivo_completo):
    lista_indice_secciones = [coincidencia.start()+tam_indice_seccion for coincidencia in re.finditer(patron_inicio_seccion, archivo_completo)]
    return lista_indice_secciones



###  
###            ENFERMEDADES  
### 



def buscar_enfermedades_en_secciones_nivel0(archivo_completo,lista_indice_secciones,posicion_final):
    
    lista_enfermedad_nivel0=list()
    
    for id,elemento in enumerate(lista_indice_secciones):
        if id+1 < len(lista_indice_secciones):
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_codigo0, archivo_completo[elemento[0]:lista_indice_secciones[id+1][0]] )]    
            lista_enfermedad_nivel0.extend(coincidencia)
        else:
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_codigo0, archivo_completo[elemento[0]:posicion_final] )]    
            lista_enfermedad_nivel0.extend(coincidencia)

    return lista_enfermedad_nivel0

def buscar_referencias(texto):
   


    lista_enfermedad_codigo =list()
    lista_posiciones=list()
    

    coincidencias = [([coincidencia.start(),coincidencia.end()]) for coincidencia in re.finditer(patron_referencia,texto)] 
    
    if coincidencias:
        for id,coincidencia in enumerate(coincidencias):
            
            if id == 0:            
                coincidencialista = [texto[0:coincidencias[id][0]-1],texto[coincidencia[0]:coincidencia[1]] ] 
            else:
                coincidencialista = [texto[coincidencias[id-1][1]:coincidencia[0]-1],texto[coincidencia[0]:coincidencia[1]] ] 
            if coincidencialista:
                lista_enfermedad_codigo.append(coincidencialista)
                
    return lista_enfermedad_codigo

def buscar_ref_enfermedades_en_enfermedades_nivel1(texto):
    coincidencia = [(texto[coincidencia.start():coincidencia.end()]) for coincidencia in re.finditer(patron_en1, texto)]    
    return coincidencia

def buscar_ref_enfermedades_en_enfermedades_nivel0(texto):
    coincidencia = [(texto[coincidencia.start():coincidencia.end()]) for coincidencia in re.finditer(patron_en0, texto)]    
    return coincidencia

def buscar_ref_enfermedades_en_enfermedades_nivel2(texto):
    
    coincidencia = [(texto[coincidencia.start():coincidencia.end()]) for coincidencia in re.finditer(patron_en2_subnivel, texto)]
    if not coincidencia:
        coincidencia = [(texto[coincidencia.start():coincidencia.end()]) for coincidencia in re.finditer(patron_en2, texto)] 

    return coincidencia

def tipo_referencia(texto):
     
    coincidencias = [([coincidencia.start(),coincidencia.end()]) for coincidencia in re.finditer(patron_referencia_basica,texto)] 
    
    if coincidencias:
        return 2
    else:
        return 1

def buscar_enfermedades_en_enfermedades_nivel1(archivo_completo,lista_indice_enfermedades,posicion_final):

    lista_enfermedad_nivel1=list()
    
    for id,elemento in enumerate(lista_indice_enfermedades):
        if id+1 < len(lista_indice_enfermedades):
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_codigo1, archivo_completo[elemento[0]:lista_indice_enfermedades[id+1][0]] )]    
            lista_enfermedad_nivel1.extend(coincidencia)
        else:
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_codigo1, archivo_completo[elemento[0]:posicion_final] )]    
            lista_enfermedad_nivel1.extend(coincidencia)

    return lista_enfermedad_nivel1




def buscar_enfermedades_en_enfermedades_nivel2(archivo_completo,lista_indice_enfermedades,posicion_final):
    lista_enfermedad_nivel2=list()
    
    for id,elemento in enumerate(lista_indice_enfermedades):
        if id+1 < len(lista_indice_enfermedades):
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_codigo2, archivo_completo[elemento[0]:lista_indice_enfermedades[id+1][0]] )]    
            lista_enfermedad_nivel2.extend(coincidencia)
        else:
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_codigo2, archivo_completo[elemento[0]:posicion_final] )]    
            lista_enfermedad_nivel2.extend(coincidencia)
    return lista_enfermedad_nivel2



def buscar_incluye_en_enfermedades_(archivo_completo,lista_indice_enfermedades,posicion_final):
    lista_incluye_enfermedad=list()
    
    for id,elemento in enumerate(lista_indice_enfermedades):
        if id+1 < len(lista_indice_enfermedades):
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patro_incluye, archivo_completo[elemento[0]:lista_indice_enfermedades[id+1][0]] )]    
            lista_incluye_enfermedad.extend(coincidencia)
        else:
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patro_incluye, archivo_completo[elemento[0]:posicion_final] )]    
            lista_incluye_enfermedad.extend(coincidencia)
    return lista_incluye_enfermedad




def buscar_excluye_en_enfermedades_(archivo_completo,lista_indice_enfermedades,posicion_final):
    lista_excluye_enfermedad=list()
    
    for id,elemento in enumerate(lista_indice_enfermedades):
        if id+1 < len(lista_indice_enfermedades):
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_excluye, archivo_completo[elemento[0]:lista_indice_enfermedades[id+1][0]] )]    
            lista_excluye_enfermedad.extend(coincidencia)
        else:
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_excluye, archivo_completo[elemento[0]:posicion_final] )]    
            lista_excluye_enfermedad.extend(coincidencia)
    return lista_excluye_enfermedad



def buscar_excluye2_en_enfermedades_(archivo_completo,lista_indice_enfermedades,posicion_final):
    lista_excluye2_enfermedad=list()
    
    for id,elemento in enumerate(lista_indice_enfermedades):
        if id+1 < len(lista_indice_enfermedades):
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_excluye1, archivo_completo[elemento[0]:lista_indice_enfermedades[id+1][0]] )]    
            lista_excluye2_enfermedad.extend(coincidencia)
        else:
            coincidencia = [(coincidencia.start()+elemento[0],coincidencia.end()+elemento[0]) for coincidencia in re.finditer(patron_excluye1, archivo_completo[elemento[0]:posicion_final] )]    
            lista_excluye2_enfermedad.extend(coincidencia)
    return lista_excluye2_enfermedad





def obtener_lista_capitulos(texto_completo):
    lista_coincidencias=list()
    lista_capitulos=list()
    

    coincidencia = [(coincidencia.start(),coincidencia.end()) for coincidencia in re.finditer(patron_capitulos_completos,texto_completo)]    
    lista_coincidencias.extend(coincidencia)

    
    for elemento in lista_coincidencias:
        lista_capitulos.append(str(texto_completo[elemento[0]:elemento[1]]))

    

    return lista_capitulos


def obtener_lista_secciones(texto_completo):
    lista_coincidencias=list()
    lista_secciones=list()
    
    coincidencia = [(coincidencia.start(),coincidencia.end()) for coincidencia in re.finditer(patron_secciones_completas,texto_completo)]    
    lista_coincidencias.extend(coincidencia)

    for elemento in lista_coincidencias:
        lista_secciones.append(str(texto_completo[elemento[0]:elemento[1]]))

    # print(lista_secciones)
    

    return lista_secciones






def obtener_listas_exportacion(ruta_entrada,ruta_salida):
    num_capitulo=0
    capitulo_actual=""
    aclaracion_capitulo=""


    num_seccion=0
    seccion_actual=""
    aclaracion_seccion=""

    cod_enfermedad=""
    enfermedad_nombre=""
    enfermedad_aclaracion=""


    tipo=0

    # id_cap_excluye()
    # id_cap_incluye()


    id_cap_ex_enf=0
    id_cap_inc_enf=0
    id_cap_ex_secc=0
    descripcion_excluye=""

    # id_enf_ex-secc=0
    # id_inc_ex-secc=0
    # descripcion_incluye=""

    # id_enf_ex_enf=0
    # id_inc_ex_enf=0

    

    

    lista_de_capitulos=list()
    lista_de_secciones=list()
    lista_de_enfermedades=list()

    lista_capitulos_excluye=list()
    lista_capitulos_incluye=list()
    

    Lista_capitulo_excluye_seccion=list()
    Lista_capitulo_incluye_enfermedad=list()
    Lista_capitulo_excluye_enfermedad=list()

    Lista_enfermedad_excl=list()



    

    contenido=filerwpe.leer_archivo(ruta_entrada) #leemos contenido del archivo  
    soup= filerwpe.parchear_archivo(contenido)
    primer_elemento = soup.find(class_="Capitulo")
    # import ipdb; ipdb.set_trace();
    siguiente = primer_elemento
    while siguiente :
        while "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()    
        while "Capitulo" in siguiente['class']:
                capitulo_actual+=siguiente.text
                siguiente = siguiente.find_next()
        num_capitulo+=1
        while "Capitulo-Descripcion" in siguiente['class']:
            aclaracion_capitulo+=siguiente.text
            siguiente = siguiente.find_next()
        while "Codifique-primero" in siguiente['class']:
            aclaracion_capitulo+=siguiente.text
            siguiente = siguiente.find_next()
        while "Indice-Secciones" in siguiente['class']:
            siguiente = siguiente.find_next()
            
        while "Nota" in siguiente['class']:
            aclaracion_capitulo+=siguiente.text
            siguiente = siguiente.find_next()
        # while "Incluye" in siguiente['class']:  
            
            
        #     or "Excluye" in siguiente['class']   
        #     or "Excluye2" in siguiente['class']   
             

        lista_de_capitulos.append([num_capitulo,capitulo_actual,aclaracion_capitulo])
        capitulo_actual=""
        aclaracion_capitulo=""
        while "Seccion" in siguiente['class']:
                seccion_actual+=siguiente.text
        num_seccion+=1      
            # or "Enfermedad_nivel2" in siguiente['class']  
            # or "Enfermedad_nivel1" in siguiente['class']  
            # or "Enfermedad_nivel0" in siguiente['class'] 
            # or "caracter" in siguiente['class']  
            # or "actualizacion" in siguiente['class']

            # "Seccion"
        while "Seccion-Descripcion" in siguiente['class']:
            aclaracion_seccion+=siguiente.text
            siguiente = siguiente.find_next()
        while "Seccion-primero" in siguiente['class']:
            aclaracion_seccion+=siguiente.text
            siguiente = siguiente.find_next()
        lista_de_secciones.append([num_seccion,seccion_actual,aclaracion_seccion])
        seccion_actual=""
        aclaracion_seccion=""



    #     while "Enfermedad_nivel2" in siguiente['class']  
    #             cod_enfermedad+=siguiente.text
    #             siguiente = siguiente.find_next()
    #         # or "Enfermedad_nivel1" in siguiente['class']  
    #         # or "Enfermedad_nivel0" in siguiente['class'] 

    #         cod_enfermedad=""
    # enfermedad_nombre=""
    # enfermedad_aclaracion=""

        if num_capitulo == 4:
            break
        siguiente = siguiente.find_next()   

    filerwpe.escribir_archivo_saltos("./exportacion/Capitulos_export.txt",lista_de_capitulos)

    filerwpe.escribir_archivo_saltos("./exportacion/secciones_export.txt",lista_de_secciones)

    return lista_de_capitulos,lista_de_secciones