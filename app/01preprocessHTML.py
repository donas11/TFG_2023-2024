from cie10 import *
from cie10 import filerwpe
from cie10 import manager
from cie10 import printer
import cie10
import time
import sys
# from memory_profiler import profile

# Asignamos el tiempo de inicio
start_time = time.time()

###
###            PATRONES
###
# Enfermedades
patron_codigo0 =  r'(?!.*>[A-Z][A-Z][A-Z]<)(>[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])<)'
patron_codigo0_2 =r'>[A-Z][0-9][0-9]<'
patron_codigo1 = r'>[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])\.([0-9]|[A-Z])<'
patron_codigo2 = r'>[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])\.([0-9]|[A-Z])([A-Z]|[0-9])([0-9]|[A-Z])*<'

patron_codigo0_act =  r'([A-Z][A-Z][A-Z])[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])'
patron_codigo0_2_act =r'[A-Z][0-9][0-9]'
patron_codigo1_act = r'([A-Z][0-9]|[A-Z])([0-9]|[A-Z])\.([0-9]|[A-Z])'
patron_codigo2_act = r'[A-Z]([0-9]|[A-Z])([0-9]|[A-Z])\.([0-9]|[A-Z])([A-Z]|[0-9])([0-9]|[A-Z])*'

# Incluyes y excluyes
patron_incluye = r'Incluye:'
patron_excluye = r'Excluye 1:'
patron_excluye_1 = r'Excluye1:'
patron_excluye2 = r'Excluye 2:'
patron_excluye2_2 = r'Excluye2:'
# Capitulo
patron_capitulo = r'CAPÍTULO'
patron_mayusculas=r'^[A-ZÁÉÍÓÚÜÑ]+(?:\s[A-ZÁÉÍÓÚÜÑ]+)*$'   #+"|"+patron_seccion
patron_mayusculas2=r'\b[A-ZÁÉÍÓÚÜÑ]+(?:\s+[A-ZÁÉÍÓÚÜÑ]+)+\b'
# Secciones
patron_seccion = r'\>([A-ZÁÉÍÓÚÜÑ,-]+(\s[A-ZÁÉÍÓÚÜÑ,-]+)*)\s(\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)|\([A-Z][0-9][0-9]\))\<'
patron_codigos_seccion=r'\>(\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)|\([A-Z][0-9][0-9]\))\<'
patron_seccion_separado = r'\>([A-ZÁÉÍÓÚÜÑ,-]+(\s[A-ZÁÉÍÓÚÜÑ,-]+)*)</div><div class="t([^"]*)"'+patron_codigos_seccion
patron_recortar=r'</div><div class="t([^"]*)">'
patron_neom=r'NEOM\s(\([A-Z][0-9][0-9]\-[A-Z][0-9][0-9]\)|\([A-Z][0-9][0-9]\))'
patron_indice_capitulo= r'>Este capítulo contiene las siguientes secciones:<'
# Notas
patron_nota= r'>Nota:'
patron_nota1= r'>NOTA:'
patron_nota2= r'>Notas:<'
# Codifiques y código adicional
patron_codifique=r'Codifique primero:'
patron_codifique3=r'Codifique primero:\s'
patron_codifique1=r'>Codifique primero\s'
patron_codifique2=r'>Codifique primero,'
patron_codigo_adicional=r">Utilice código adicional"
# Pies de Pâgina
patron_pie_de_pagina=[
    r'>\b([6-9][5-9][8-9]|[1-9][0-9]{2}|1[0-3][0-9]{2}|14[0-6][0-9]|147[0-2])\b<',
    r'FACTORES QUE INFLUYEN EN EL ESTADO DE SALUD Y CONTACTO CON LOS SERVICIOS SANITARIOS',
    r'LISTA TABULAR ENFERMEDADES',
    r'Lista Tabular Enfermedades',
    r'CIERTAS ENFERMEDADES INFECCIOSAS Y PARASITARIAS',
    r'>NEOPLASIAS<',
    r'"pi',
    r'"pf w',
    r'"pc pc',
    r'"c x',
    r'"bi ',
    r'"fc5 sc1'
       
]
# FIN
patron_fin=r'"_ _27'
# Extensiones y actualización
patron_extension=r'(>[4-7]º<)|(>x 7º<)'
patron_extension_codigo=r'Se debe añadir el 7º carácter apropiado al código'
patron_actualizacion=r'>\+'
# Classes
patron_class = r'class="t([^"]*)"'
patron_class_capitulo = r'class="Capitulo"'
patron_classpiedpag = r'class="([^"]*)"'



#archivos de entrada y salida
ruta_archivo="CIE10LT.html" #archivo de entrada
ruta_salida1="CIE10LTP00rocesado.html" #archivo de salida




###
###             LECTURA ARCHIVO
###
contenido=filerwpe.leer_archivo(ruta_archivo) #leemos contenido del archivo   
contenido_en_lineas = contenido.splitlines()
###
###             VARIABLES
###
coincidencias_capitulos=list()
coincidencia_neoms=list()
coincidencia_seccion=list()
coincidencias_seccion_class=list()



# 
#           CAPITULOS
# 
countline=1

with open(ruta_salida1, 'w') as procesadofile:
    for line in contenido_en_lineas:
        coincidencias_capitulo = [coincidencia.start()-53,coincidencia.end(),line,coincidencia.start()] if (coincidencia := re.search(patron_capitulo, line)) else None       
        if coincidencias_capitulo :
            coincidencia_mayusculas = re.search(patron_mayusculas,str(line[coincidencias_capitulo[3]:coincidencias_capitulo[1]]))            
            if coincidencia_mayusculas:
                coincidencias_capitulo_class = [coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),coincidencias_capitulo[2]] if (coincidencia := re.search(patron_class, str(line[coincidencias_capitulo[0]:coincidencias_capitulo[1]]))) else None
                if coincidencias_capitulo_class:
                        inicio = coincidencias_capitulo[0]+coincidencias_capitulo_class[0]
                        final =  coincidencias_capitulo[0]+coincidencias_capitulo_class[1]
                        texto = coincidencias_capitulo_class[3]
                        modificacion_class= texto[:inicio]+ "Capitulo" + texto[final:] 
                        coincidencias_capitulo_class[3]= modificacion_class
                        line= coincidencias_capitulo_class[3]
        if line!="":
            procesadofile.write(line + '\n')
        


ruta_archivo="CIE10LTP00rocesado.html" #archivo de entrada
ruta_salida1="CIE10LTP00Capitulos.html" #archivo de salida
contenido= filerwpe.leer_archivo(ruta_archivo)
soup= filerwpe.parchear_archivo(contenido)

images =soup.find_all('img')
for elemento in images:
    elemento.extract()
soup.prettify()

capitulos=soup.find_all(class_="Capitulo")
for elem in capitulos:
    siguiente = elem.find_next()
    while siguiente :
        if (siguiente.get_text()).isupper(): 
                siguiente['class']="Capitulo"
        else:
            break
        siguiente = siguiente.find_next()

filerwpe.archivar_completo(str(soup),ruta_salida1)

# 
#           PIES DE PÁGINA
# 

ruta_archivo="CIE10LTP00Capitulos.html" #archivo de entrada
ruta_salida1="CIE10LTP01PiedePagina.html" #archivo de salida


contenido=filerwpe.leer_archivo(ruta_archivo) #leemos contenido del archivo   
contenido_en_lineas = contenido.splitlines()

# Variables 
numero_decoind=list()
coincidencias_pie_depagina=list()
tam_cadena=54;
num_linea=0
numero_de_coin=0 
len_acumulado=0
tam_letras_pie=13
final_de=0

with open(ruta_salida1, 'w') as procesadofile:
    for line in contenido_en_lineas:
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,0] for coincidencia in re.finditer(patron_pie_de_pagina[0], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,1] for coincidencia in re.finditer(patron_pie_de_pagina[1], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,2] for coincidencia in re.finditer(patron_pie_de_pagina[2], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,3] for coincidencia in re.finditer(patron_pie_de_pagina[3], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,4] for coincidencia in re.finditer(patron_pie_de_pagina[4], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
                numero_decoind.append(len(coincidencias_pie_depagina))
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,5] for coincidencia in re.finditer(patron_pie_de_pagina[5], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,6] for coincidencia in re.finditer(patron_pie_de_pagina[6], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,7] for coincidencia in re.finditer(patron_pie_de_pagina[7], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,8] for coincidencia in re.finditer(patron_pie_de_pagina[8], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,9] for coincidencia in re.finditer(patron_pie_de_pagina[9], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)
        coincidencia_pie_depagina = [[coincidencia.start(),coincidencia.end(),line,10] for coincidencia in re.finditer(patron_pie_de_pagina[10], str(line) )]
        if coincidencia_pie_depagina:
            for coincidenenpie in coincidencia_pie_depagina:
                coincidencias_pie_depagina.append(coincidenenpie)


        if coincidencias_pie_depagina :
                
            pos_acummulado=0
            final_de=0
            len_acumulado+=len(coincidencias_pie_depagina)
            
            for numeric,coincidenciapiedepagina in enumerate(coincidencias_pie_depagina):
                if(coincidenciapiedepagina[3]>5):
                    tam_cadena=11
                else:
                    tam_cadena=54
                if(coincidenciapiedepagina[3]==0) or (coincidenciapiedepagina[3]==1) or (coincidenciapiedepagina[3]==2) or (coincidenciapiedepagina[3]==3):
                    tam_letras_pie=0;
                else:
                    if(coincidenciapiedepagina[3]==4) or (coincidenciapiedepagina[3]==7) or (coincidenciapiedepagina[3]==8) or (coincidenciapiedepagina[3]==9) or (coincidenciapiedepagina[3]==10):
                        tam_letras_pie=0 #26 
                        if(coincidenciapiedepagina[3]==4):
                            tam_letras_pie=26 
                        if(coincidenciapiedepagina[3]==7) or (coincidenciapiedepagina[3]==8):
                            final_de=7
                        if(coincidenciapiedepagina[3]==9) or (coincidenciapiedepagina[3]==10):
                            # tam_cadena=0
                            final_de=12
                            tam_letras_pie=0
                    else:
                        tam_letras_pie=13;

                coincidencias_pie_de_paginaclass = [coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] if (coincidencia := re.search(patron_classpiedpag, str(line[coincidenciapiedepagina[0]-tam_cadena-pos_acummulado-tam_letras_pie:coincidenciapiedepagina[1]+1-pos_acummulado-tam_letras_pie+final_de]))) else None
                if coincidencias_pie_de_paginaclass:
                    if(coincidenciapiedepagina[3]==4) or (coincidenciapiedepagina[3]==5) :
                        inicio=coincidenciapiedepagina[0]+(coincidencias_pie_de_paginaclass[0]-tam_cadena)-pos_acummulado-tam_letras_pie
                        final=coincidenciapiedepagina[0]+(coincidencias_pie_de_paginaclass[1]-tam_cadena)-pos_acummulado-tam_letras_pie 
                    else:
                        if (coincidenciapiedepagina[3]==6):
                            inicio=coincidenciapiedepagina[0]+(coincidencias_pie_de_paginaclass[0]-tam_cadena)-pos_acummulado-2*tam_letras_pie
                            final=coincidenciapiedepagina[0]+(coincidencias_pie_de_paginaclass[1]-tam_cadena)-pos_acummulado-2*tam_letras_pie                            
                        else:
                            inicio=coincidenciapiedepagina[0]+(coincidencias_pie_de_paginaclass[0]-tam_cadena)-pos_acummulado
                            final=coincidenciapiedepagina[0]+(coincidencias_pie_de_paginaclass[1]-tam_cadena)-pos_acummulado 
                
                    texto = line
                    pos_acummulado=coincidencias_pie_de_paginaclass[2]-tam_letras_pie    
                    modificacion_class= texto[:inicio]+ "Pie-de-pagina" + texto[final:]
                    coincidencias_pie_de_paginaclass[3]= modificacion_class
                    line= coincidencias_pie_de_paginaclass[3]
            coincidencias_pie_depagina.clear()
        if line!="": 
            procesadofile.write(line + '\n')

# 
#       SECCIONES 
# 
ruta_archivo="CIE10LTP01PiedePagina.html" #archivo de salida
ruta_salida1="CIE10LTP02Secciones.html" #archivo de salida

# Variables
tam_despl_class=55  
tam_letras_class=13
tam_letras_seccion=7
pos_acummulado=0
num_linea=0
pos_acummulado_recorte=0
coincidencias_seccion=list()
no_especificados=list()
coincidencias_secciones=list()
coincidencias_secciones_separados=list()
no_coincidencias_seccion=list()
secciones_incidencias=list()

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            

            coincidencias_elemento = [[coincidencia.start(),coincidencia.end(),line[coincidencia.start():coincidencia.end()]] for coincidencia in re.finditer(patron_seccion_separado, str(line) )]
            coincidencias_secciones_separados.extend(coincidencias_elemento)
            for coincidencia in coincidencias_secciones_separados:
                inicio = coincidencia[0]+coinciden[0]-tam_letras_seccion-pos_acummulado_recorte
                final =  coincidencia[0]+coinciden[1]+1-pos_acummulado_recorte
                coincidencias_seccion_recortar = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line[coincidencia.start():coincidencia.end()]] for coincidencia in re.finditer(patron_recortar, str(line[coincidencia[0]-pos_acummulado_recorte:coincidencia[1]-pos_acummulado_recorte]))]                 
                if coincidencias_seccion_recortar:
                    for coinciden in coincidencias_seccion_recortar:
                        inicio = coincidencia[0]+coinciden[0]-tam_letras_seccion-pos_acummulado_recorte
                        final =  coincidencia[0]+coinciden[1]+1-pos_acummulado_recorte
                        texto = line 
                        modificacion_class= texto[:inicio] +" "+ texto[final:] 
                        tam_acumulado=final-inicio+1
                        line= modificacion_class
                        pos_acummulado_recorte+=tam_acumulado
            coincidencias_secciones_separados.clear()


            coincidencias_elementocap = [[coincidencia.start(),coincidencia.end(),line[coincidencia.start():coincidencia.end()]] for coincidencia in re.finditer(patron_capitulo, str(line) )]
            coincidencias_capitulos.extend(coincidencias_elementocap)

            coincidencias_elementoneom = [[coincidencia.start(),coincidencia.end(),line[coincidencia.start():coincidencia.end()]] for coincidencia in re.finditer(patron_neom, str(line) )]
            coincidencia_neoms.extend(coincidencias_elementoneom)

            coincidencias_elemento = [[coincidencia.start(),coincidencia.end(),line[coincidencia.start():coincidencia.end()]] for coincidencia in re.finditer(patron_seccion, str(line) )]
            coincidencias_secciones.extend(coincidencias_elemento)
            
           


            # Borramos los que no son secciones
            for coincidencia_seccion in coincidencias_secciones:
                for capis in coincidencias_capitulos:
                    if capis[2] in coincidencia_seccion[2]:
                        coincidencias_secciones.remove(coincidencia_seccion)
            for coincide_seccion in coincidencias_secciones:
                for neoms in coincidencia_neoms:
                    if neoms[2] in coincide_seccion[2]:
                        if coincide_seccion in coincidencias_secciones:
                            coincidencias_secciones.remove(coincide_seccion)
                            


              

            for coincidencia_seccion in coincidencias_secciones:
                pos_busqueda_inicio= coincidencia_seccion[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                pos_busqueda_final= coincidencia_seccion[1]-pos_acummulado
                coincidencias_seccion_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line[coincidencia.start():coincidencia.end()]] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                if coincidencias_seccion_class:                
                    for coinciden in coincidencias_seccion_class:
                        es_ENF=re.search(patron_codigo0, str(line[pos_busqueda_inicio:pos_busqueda_final]))
                        if not es_ENF:
                            es_ENF=re.search(patron_codigo1, str(line[pos_busqueda_inicio:pos_busqueda_final]))
                            if not es_ENF:
                                es_ENF=re.search(patron_codigo2, str(line[pos_busqueda_inicio:pos_busqueda_final]))
                                if not es_ENF:    
                                    if line[coincidencia_seccion[0]-pos_acummulado:coincidencia_seccion[1]-pos_acummulado].isupper():
                                                        inicio = pos_busqueda_inicio+coinciden[0]
                                                        final =  pos_busqueda_inicio+coinciden[1]
                                                        texto = line
                                                        modificacion_class= texto[:inicio]+ "Seccion" + texto[final:] 
                                                        line= modificacion_class
                                                        pos_acummulado+=coinciden[2]-tam_letras_seccion    
                coincidencias_seccion_class.clear()
            coincidencias_secciones.clear()                    
            coincidencias_capitulos.clear()      
            coincidencia_neoms.clear()              
            num_linea+=1                                            
            pos_acummulado=0
            pos_acummulado_recorte=0
            if line!="" and line!='\n' : 
                procesadofile.write(line + '\n')
            


# 
#       INDICE SECCIONES
# 
ruta_archivo="CIE10LTP02Secciones.html"  #archivo de entrada
ruta_salida1="CIE10LTP03IndiceSecciones.html" #archivo de salida

#  Variables
tam_letras_class=13
tam_despl_class=53

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file: 
            coincidencias_indice_capitulo = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_indice_capitulo, str(line) )]
            if coincidencias_indice_capitulo:
                for coinci in coincidencias_indice_capitulo:
                                    
                    coincidencias_indice_class = [coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),coinci[2]] if (coincidencia := re.search(patron_class, str(line[coinci[0]-tam_despl_class:coinci[1]]))) else None
                    if coincidencias_indice_class:
                       
                        inicio = coinci[0]+coincidencias_indice_class[0]-tam_despl_class #+tam_letras_class
                        final = coinci[0]+coincidencias_indice_class[1]-tam_despl_class
                        # -tam_despl_class

                        texto = coincidencias_indice_class[3]
                        modificacion_class= texto[:inicio]+ "Indice-Secciones" + texto[final:] 
                        coincidencias_indice_class[3]= modificacion_class
                        line=coincidencias_indice_class[3]
                        
                            # print(contenido_en_lineas[linea[3]]+"["+str(linea[3])+"]")
            if line!="":
                procesadofile.write(line + '\n')



contenido= filerwpe.leer_archivo(ruta_salida1)
soup= filerwpe.parchear_archivo(contenido)


indice_secciones=soup.find_all(class_="Indice-Secciones")
# import ipdb; ipdb.set_trace();
for elem in indice_secciones:
    # print(str(elem)+"\n")
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or  "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']  or "Excluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']: 
            # print("sale del bucle")
            break  
        if "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class'] and "Excluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Indice-Secciones"
            # print(siguiente)
        
        siguiente = siguiente.find_next()

ruta_salida1="CIE10LTP03IndiceSeccionesmod.html" #archivo de salida
filerwpe.archivar_completo(str(soup),ruta_salida1)

# 
#       INCLUYE
# 
ruta_archivo="CIE10LTP03IndiceSeccionesmod.html" #archivo de entrada
ruta_salida1="CIE10LTP04Incluye.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_incluye=7
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
        with open(ruta_salida1, 'w') as procesadofile:
            for line in file:
                coincidencias_incluye = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_incluye, str(line) )]
                if coincidencias_incluye :
                     
                    for coincidencia_incluye in coincidencias_incluye:
                        pos_busqueda_inicio=coincidencia_incluye[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final=coincidencia_incluye[1]-pos_acummulado
                        coincidencias_incluye_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                        if coincidencias_incluye_class:
                            for coinciden in coincidencias_incluye_class:
                                coinci_class_inicio=pos_busqueda_inicio+coinciden[0] #-pos_acummulado #-tam_letras_class
                                coinci_class_final=pos_busqueda_inicio+coinciden[1] #-pos_acummulado                   
                                inicio = coinci_class_inicio
                                final =  coinci_class_final
                                texto = line
                                modificacion_class= texto[:inicio]+ "Incluye" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]
                                pos_acummulado+=coinciden[2]-tam_letras_incluye 
                        
                    pos_acummulado=0
                num_linea+=1 
                if line!="": 
                    procesadofile.write(line + '\n')
                

# 
#       EXLUYE 
# 
ruta_archivo="CIE10LTP04Incluye.html" #archivo de entrada
ruta_salida1="CIE10LTP05Excluye.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_excluye=7
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
        with open(ruta_salida1, 'w') as procesadofile:
            for line in file:
                coincidencias_excluye = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_excluye_1, str(line) )]
                if coincidencias_excluye :
                     
                    for coincidencia_excluye in coincidencias_excluye:
                        pos_busqueda_inicio=coincidencia_excluye[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final=coincidencia_excluye[1]-pos_acummulado
                        coincidencias_excluye_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                        if coincidencias_excluye_class:
                            for coinciden in coincidencias_excluye_class:
                                coinci_class_inicio=pos_busqueda_inicio+coinciden[0] 
                                coinci_class_final=pos_busqueda_inicio+coinciden[1] 
                                inicio = coinci_class_inicio
                                final =  coinci_class_final
                                texto = line
                                modificacion_class= texto[:inicio]+ "Excluye" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]
                                
                                pos_acummulado+=coinciden[2]-tam_letras_excluye
                    pos_acummulado=0
                    coincidencia_excluye.clear()
                coincidencias_excluye = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_excluye, str(line) )]
                if coincidencias_excluye :
                     
                    for coincidencia_excluye in coincidencias_excluye:
                        pos_busqueda_inicio=coincidencia_excluye[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final=coincidencia_excluye[1]-pos_acummulado
                        coincidencias_excluye_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                        if coincidencias_excluye_class:
                            for coinciden in coincidencias_excluye_class:
                                coinci_class_inicio=pos_busqueda_inicio+coinciden[0] 
                                coinci_class_final=pos_busqueda_inicio+coinciden[1] 
                                inicio = coinci_class_inicio
                                final =  coinci_class_final
                                texto = line
                                modificacion_class= texto[:inicio]+ "Excluye" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]
                                
                                pos_acummulado+=coinciden[2]-tam_letras_excluye 
                                
                    pos_acummulado=0
                num_linea+=1 
                if line!="" and line!='\n' : 
                    procesadofile.write(line + '\n')


# 
#           EXCLUYES2
# 
ruta_archivo="CIE10LTP05Excluye.html" #archivo de entrada
ruta_salida1="CIE10LTP06Excluye2.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_excluye=8
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
        with open(ruta_salida1, 'w') as procesadofile:
            for line in file:
                coincidencias_excluye2 = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_excluye2_2, str(line) )]
                if coincidencias_excluye2 :
                    for coincidencia_excluye2 in coincidencias_excluye2:
                        pos_busqueda_inicio=coincidencia_excluye2[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final=coincidencia_excluye2[1]-pos_acummulado
                        coincidencias_excluye2_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                        if coincidencias_excluye2_class:
                            for coinciden in coincidencias_excluye2_class:
                                coinci_class_inicio=pos_busqueda_inicio+coinciden[0] 
                                coinci_class_final=pos_busqueda_inicio+coinciden[1] 
                                inicio = coinci_class_inicio
                                final =  coinci_class_final
                                texto = line
                                modificacion_class= texto[:inicio]+ "Excluye2" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]
                                
                                pos_acummulado+=coinciden[2]-tam_letras_excluye 
                                
                    pos_acummulado=0
                    coincidencia_excluye2.clear()
                coincidencias_excluye2 = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_excluye2, str(line) )]
                if coincidencias_excluye2 :
                    for coincidencia_excluye2 in coincidencias_excluye2:
                        pos_busqueda_inicio=coincidencia_excluye2[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final=coincidencia_excluye2[1]-pos_acummulado
                        coincidencias_excluye2_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                        if coincidencias_excluye2_class:
                            for coinciden in coincidencias_excluye2_class:
                                coinci_class_inicio=pos_busqueda_inicio+coinciden[0] 
                                coinci_class_final=pos_busqueda_inicio+coinciden[1] 
                                inicio = coinci_class_inicio
                                final =  coinci_class_final
                                texto = line
                                modificacion_class= texto[:inicio]+ "Excluye2" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]
                                
                                pos_acummulado+=coinciden[2]-tam_letras_excluye 
                                
                    pos_acummulado=0
                num_linea+=1 
                if line!="" and line!='\n' : 
                    procesadofile.write(line + '\n')

# 
#    NOTA 
# 
ruta_archivo="CIE10LTP06Excluye2.html" #archivo de entrada
ruta_salida1="CIE10LTP07Nota.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_nota=4
pos_acummulado=0
coincidencias_nota_class=list()
num_linea=0

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            coincidencias_nota = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_nota, str(line) )]
            if coincidencias_nota: 
                for coincidencia_nota in coincidencias_nota:
                    pos_busqueda_inicio= coincidencia_nota[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_nota[1]-pos_acummulado
                    coincidencias_nota_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                    if coincidencias_nota_class:
                        for coinciden in coincidencias_nota_class:
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1] 
                            texto = coinciden[3]
                            modificacion_class= texto[:inicio]+ "Nota" + texto[final:]
                            coinciden[3]= modificacion_class
                            line=coinciden[3]
                            
                            pos_acummulado+=coinciden[2]-tam_letras_nota
            pos_acummulado=0
            coincidencias_nota = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_nota1, str(line) )]
            if coincidencias_nota: 
                for coincidencia_nota in coincidencias_nota:
                    pos_busqueda_inicio= coincidencia_nota[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_nota[1]-pos_acummulado
                    coincidencias_nota_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                    if coincidencias_nota_class:
                        for coinciden in coincidencias_nota_class:
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1]
                            texto = coinciden[3]
                            modificacion_class= texto[:inicio]+ "Nota" + texto[final:]
                            coinciden[3]= modificacion_class
                            line=coinciden[3]
                            pos_acummulado+=coinciden[2]-tam_letras_nota 
            pos_acummulado=0            
            coincidencias_nota = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_nota2, str(line) )]
            if coincidencias_nota: 
                for coincidencia_nota in coincidencias_nota:
                    pos_busqueda_inicio= coincidencia_nota[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_nota[1]-pos_acummulado
                    coincidencias_nota_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]))]
                    if coincidencias_nota_class:
                        for coinciden in coincidencias_nota_class:
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1] 
                            texto = coinciden[3]
                            modificacion_class= texto[:inicio]+ "Nota" + texto[final:] 
                            coinciden[3]= modificacion_class
                            line=coinciden[3]
                            pos_acummulado+=coinciden[2]-tam_letras_nota
            pos_acummulado=0
            num_linea+=1 
            if line!="" and line!='\n' : 
                procesadofile.write(line + '\n')

# 
#       CODIFIQUE PRIMERO 
# 
ruta_archivo="CIE10LTP07Nota.html" #archivo de entrada
ruta_salida1="CIE10LTP08CPrimero.html" #archivo de salida
# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_primero=17
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
        with open(ruta_salida1, 'w') as procesadofile:
            for line in file:
                # if num_linea==4247:
                #     import ipdb; ipdb.set_trace();
                coincidencias_codifique = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_codifique, str(line) )]              
                if coincidencias_codifique:
                    for coincidencia_codifique in coincidencias_codifique:
                        pos_busqueda_inicio= coincidencia_codifique[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final= coincidencia_codifique[1]-pos_acummulado  
                        coincidencias_codifique_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                        if coincidencias_codifique_class:
                            for coinciden in coincidencias_codifique_class:      
                                inicio = pos_busqueda_inicio+coinciden[0]
                                final =  pos_busqueda_inicio+coinciden[1] 
                                texto = str(coinciden[3])
                                modificacion_class= texto[:inicio]+ "Codifique-primero" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]

                                pos_acummulado+=coinciden[2]-tam_letras_primero

                pos_acummulado=0
                coincidencias_codifique = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_codifique3, str(line) )]              
                if coincidencias_codifique:
                    for coincidencia_codifique in coincidencias_codifique:
                        pos_busqueda_inicio= coincidencia_codifique[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final= coincidencia_codifique[1]-pos_acummulado  
                        coincidencias_codifique_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                        if coincidencias_codifique_class:
                            for coinciden in coincidencias_codifique_class:      
                                inicio = pos_busqueda_inicio+coinciden[0]
                                final =  pos_busqueda_inicio+coinciden[1] 
                                texto = str(coinciden[3])
                                modificacion_class= texto[:inicio]+ "Codifique-primero" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]

                                pos_acummulado+=coinciden[2]-tam_letras_primero
                pos_acummulado=0
                coincidencias_codifique = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_codifique1, str(line) )]
                if coincidencias_codifique:
                    for coincidencia_codifique in coincidencias_codifique:
                        pos_busqueda_inicio= coincidencia_codifique[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final= coincidencia_codifique[1]-pos_acummulado  
                        coincidencias_codifique_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                        if coincidencias_codifique_class:
                            for coinciden in coincidencias_codifique_class:      
                                inicio = pos_busqueda_inicio+coinciden[0]
                                final =  pos_busqueda_inicio+coinciden[1] 
                                texto = str(coinciden[3])
                                modificacion_class= texto[:inicio]+ "Codifique-primero" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]

                                pos_acummulado+=coinciden[2]-tam_letras_primero
                pos_acummulado=0
                coincidencias_codifique = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_codifique2, str(line) )]    
                if coincidencias_codifique:
                    for coincidencia_codifique in coincidencias_codifique:
                        pos_busqueda_inicio= coincidencia_codifique[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                        pos_busqueda_final= coincidencia_codifique[1]-pos_acummulado  
                        coincidencias_codifique = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                        if coincidencias_codifique:
                            for coinciden in coincidencias_codifique:      
                                inicio = pos_busqueda_inicio+coinciden[0]
                                final =  pos_busqueda_inicio+coinciden[1] 
                                texto = str(coinciden[3])
                                modificacion_class= texto[:inicio]+ "Codifique-primero" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]

                                pos_acummulado+=coinciden[2]-tam_letras_primero
                num_linea+=1 
                if line!="" and line!='\n' : 
                    procesadofile.write(line + '\n')

# 
#           CARACTER
# 
ruta_archivo="CIE10LTP08CPrimero.html" #archivo de entrada
ruta_salida1="CIE10LTP09Caracter.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_caracter=8
pos_acummulado=0
coincidencias_nota_class=list()
num_linea=0

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            coincidencias_extension = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_extension, str(line) )]
            if coincidencias_extension:
                for coincidencia_extension in coincidencias_extension:
                    pos_busqueda_inicio= coincidencia_extension[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_extension[1]-pos_acummulado
                    coincidencias_extension_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                    if coincidencias_extension_class:
                        for coinciden in coincidencias_extension_class:
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1] 
                            texto = coinciden[3]
                            modificacion_class= texto[:inicio]+ "caracter" + texto[final:] 
                            coinciden[3]= modificacion_class
                            line= coinciden[3]

                            pos_acummulado+=coinciden[2]-tam_letras_caracter
            num_linea+=1
            pos_acummulado=0 
            if line!="" and line!='\n' : 
                procesadofile.write(line + '\n')

# 
#       EXTENSION CARACTER
# 
ruta_archivo="CIE10LTP09Caracter.html" #archivo de entrada
ruta_salida1="CIE10LTP10EXTCaracter.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_extcaracter=18
pos_acummulado=0
coincidencias_nota_class=list()
num_linea=0

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            coincidencias_extension_cod = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_extension_codigo, str(line) )]
            if coincidencias_extension_cod:
                for coincidencia_extension_cod in coincidencias_extension_cod:
                    pos_busqueda_inicio= coincidencia_extension_cod[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_extension_cod[1]-pos_acummulado
                    coincidencias_extension_cod_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                    if coincidencias_extension_cod_class:
                        for coinciden in coincidencias_extension_cod_class:
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1] 
                            texto = coinciden[3]
                            modificacion_class= texto[:inicio]+ "extension-caracter" + texto[final:] 
                            coinciden[3]= modificacion_class
                            line= coinciden[3]

                            pos_acummulado+=coinciden[2]-tam_letras_extcaracter
            pos_acummulado=0
            if line!="" and line!='\n' :  
                procesadofile.write(line + '\n')

# 
#           ACTUALIZACIÓN
# 
ruta_archivo="CIE10LTP10EXTCaracter.html" #archivo de entrada
ruta_salida1="CIE10LTP11Actualización.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_extcaracter=13
pos_acummulado=0
coincidencias_nota_class=list()
num_linea=0


with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            coincidencias_extension_cod = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_actualizacion, str(line) )]
            if coincidencias_extension_cod:
                for coincidencia_extension_cod in coincidencias_extension_cod:
                    pos_busqueda_inicio= coincidencia_extension_cod[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_extension_cod[1]-pos_acummulado
                    coincidencias_extension_cod_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                    if coincidencias_extension_cod_class:
                        for coinciden in coincidencias_extension_cod_class:
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1] 
                            texto = coinciden[3]
                            modificacion_class= texto[:inicio]+ "actualizacion" + texto[final:] 
                            coinciden[3]= modificacion_class
                            line= coinciden[3]

                            pos_acummulado+=coinciden[2]-tam_letras_extcaracter
            pos_acummulado=0
            if line!="" and line!='\n' :  
                procesadofile.write(line + '\n')

# 
#       FINAL DE DOCUMENTO
# 
ruta_archivo="CIE10LTP11Actualización.html" #archivo de entrada
ruta_salida1="CIE10LTP12FIN.html" #archivo de salida


tam_despl_class=55
tam_letras_class=13
tam_letras_fin=3
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
        with open(ruta_salida1, 'w') as procesadofile:
            for line in file:
                coincidencias_fin = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_fin, str(line) )]
                if coincidencias_fin:
                    # import ipdb; ipdb.set_trace();
                    for coincidencia_fin in coincidencias_fin:
                        pos_busqueda_inicio= coincidencia_fin[0]-pos_acummulado-tam_letras_class
                        pos_busqueda_final= coincidencia_fin[1]-pos_acummulado+1
                        coincidencias_fin_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_classpiedpag, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                        if coincidencias_fin_class:
                            for coinciden in coincidencias_fin_class:
                                inicio = pos_busqueda_inicio+coinciden[0]
                                final =  pos_busqueda_inicio+coinciden[1] 
                                texto = coinciden[3]
                                modificacion_class= texto[:inicio]+ "FIN" + texto[final:] 
                                coinciden[3]= modificacion_class
                                line= coinciden[3]
                    
                                pos_acummulado+=coinciden[2]-tam_letras_fin
                pos_acummulado=0
                if line!="" and line!='\n' :  
                    procesadofile.write(line + '\n')

# 
#       CÓDIGO ADICIONAL 
# 
ruta_archivo="CIE10LTP12FIN.html" #archivo de entrada
ruta_salida1="CIE10LTP13UCodigoAdicional.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_cod_adicional=24
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            coincidencias_cod_adicional = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_codigo_adicional, str(line) )]
            if coincidencias_cod_adicional:
                for coincidencia_cod_adicional in coincidencias_cod_adicional:
                    pos_busqueda_inicio= coincidencia_cod_adicional[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_cod_adicional[1]-pos_acummulado
                    coincidencias_cod_adicional = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_classpiedpag, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                    if coincidencias_cod_adicional:
                        for coinciden in coincidencias_cod_adicional:
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1]
                            texto = coinciden[3]
                            modificacion_class= texto[:inicio]+ "Utilice-codigo-adicional" + texto[final:] 
                            coinciden[3]= modificacion_class
                            line= coinciden[3]

                            pos_acummulado+=coinciden[2]-tam_letras_cod_adicional
            pos_acummulado=0
            if line!="" and line!='\n' :  
                procesadofile.write(line + '\n')

# 
#       ENFERMEDADES NIVEL 0
# 

ruta_archivo="CIE10LTP13UCodigoAdicional.html" #archivo de entrada
ruta_salida1="CIE10LTP14EFN0.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_ENF=31
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            coincidencias_nivel0 = [[coincidencia.start(),coincidencia.end(),line[coincidencia.start():coincidencia.end()]] for coincidencia in re.finditer(patron_codigo0, str(line) )]
            if coincidencias_nivel0:
                for coincidencia_nivel0 in coincidencias_nivel0:
                    pos_busqueda_inicio= coincidencia_nivel0[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_nivel0[1]-pos_acummulado
                    es_actualizacion=re.search(patron_actualizacion, str(line[pos_busqueda_inicio:pos_busqueda_final]))
                    if es_actualizacion:
                        pos_busqueda_inicio+=tam_despl_class
                        # import ipdb; ipdb.set_trace();    
                    coincidencias_nivel0_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_classpiedpag, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                    if coincidencias_nivel0_class:
                        for coinciden in coincidencias_nivel0_class:
                            #print("Modificando Nivel 0......")
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1]
                            texto = coinciden[3]
                            
                            if es_actualizacion:
                                modificacion_class= texto[:inicio]+ "Enfermedad_nivel0-actualizacion" + texto[final:] 
                                tam_letras_ENF=31
                            else:
                                modificacion_class= texto[:inicio]+ "Enfermedad_nivel0" + texto[final:] 
                                tam_letras_ENF=17
                            coinciden[3]= modificacion_class
                            line= coinciden[3]
                
                            pos_acummulado+=coinciden[2]-tam_letras_ENF
                    es_actualizacion=False
            coincidencias_nivel0 = [[coincidencia.start(),coincidencia.end(),line[coincidencia.start():coincidencia.end()]] for coincidencia in re.finditer(patron_codigo0_2, str(line) )]
            if coincidencias_nivel0:
                for coincidencia_nivel0 in coincidencias_nivel0:
                    pos_busqueda_inicio= coincidencia_nivel0[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_nivel0[1]-pos_acummulado
                    es_actualizacion=re.search(patron_actualizacion, str(line[pos_busqueda_inicio:pos_busqueda_final]))
                    if es_actualizacion:
                        pos_busqueda_inicio+=tam_despl_class
                        # import ipdb; ipdb.set_trace();    
                    coincidencias_nivel0_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_class, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                    if coincidencias_nivel0_class:
                        for coinciden in coincidencias_nivel0_class:
                            #print("Modificando Nivel 0......")
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1]
                            texto = coinciden[3]
                            
                            if es_actualizacion:
                                modificacion_class= texto[:inicio]+ "Enfermedad_nivel0-actualizacion" + texto[final:] 
                                tam_letras_ENF=31
                            else:
                                modificacion_class= texto[:inicio]+ "Enfermedad_nivel0" + texto[final:] 
                                tam_letras_ENF=17
                            coinciden[3]= modificacion_class
                            line= coinciden[3]
                
                            pos_acummulado+=coinciden[2]-tam_letras_ENF
                    es_actualizacion=False

            pos_acummulado=0
            num_linea+=1
            if line!="" and line!='\n' :  
                procesadofile.write(line + '\n')



# 
#       ENFERMEDADES NIVEL 1
# 
ruta_archivo="CIE10LTP14EFN0.html" #archivo de entrada
ruta_salida1="CIE10LTP15EFN1.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_ENF=31
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            coincidencias_nivel1 = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_codigo1, str(line) )]
            if coincidencias_nivel1:
                for coincidencia_nivel1 in coincidencias_nivel1:
                    pos_busqueda_inicio= coincidencia_nivel1[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_nivel1[1]-pos_acummulado
                    es_actualizacion=re.search(patron_actualizacion, str(line[pos_busqueda_inicio:pos_busqueda_final]))
                    if es_actualizacion:
                        pos_busqueda_inicio+=tam_despl_class
                        
                    coincidencias_nivel1_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_classpiedpag, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                    if coincidencias_nivel1_class:
                        for coinciden in coincidencias_nivel1_class:
                            
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1]
                            texto = coinciden[3]
                            
                            if es_actualizacion:
                                modificacion_class= texto[:inicio]+ "Enfermedad_nivel1-actualizacion" + texto[final:] 
                                tam_letras_ENF=31
                            else:
                                modificacion_class= texto[:inicio]+ "Enfermedad_nivel1" + texto[final:] 
                                tam_letras_ENF=17
                            coinciden[3]= modificacion_class
                            line= coinciden[3]
                
                            pos_acummulado+=coinciden[2]-tam_letras_ENF
                    es_actualizacion=False
            pos_acummulado=0
            if line!="" and line!='\n' :  
                procesadofile.write(line + '\n')



# 
#       ENFERMEDADES NIVEL 2
# 
ruta_archivo="CIE10LTP15EFN1.html" #archivo de entrada
ruta_salida1="CIE10LTP16EFN2.html" #archivo de salida

# Variables
tam_despl_class=55
tam_letras_class=13
tam_letras_ENF=31
pos_acummulado=0
num_linea=0

with open(ruta_archivo, 'r') as file:
    with open(ruta_salida1, 'w') as procesadofile:
        for line in file:
            coincidencias_nivel2 = [[coincidencia.start(),coincidencia.end(),line] for coincidencia in re.finditer(patron_codigo2, str(line) )]
            if coincidencias_nivel2:
                for coincidencia_nivel2 in coincidencias_nivel2:
                    pos_busqueda_inicio= coincidencia_nivel2[0]-tam_despl_class-pos_acummulado-2*tam_letras_class
                    pos_busqueda_final= coincidencia_nivel2[1]-pos_acummulado
                    es_actualizacion=re.search(patron_actualizacion, str(line[pos_busqueda_inicio:pos_busqueda_final]))
                    if es_actualizacion:
                        pos_busqueda_inicio+=tam_despl_class
                        
                    coincidencias_nivel2_class = [[coincidencia.start()+7,coincidencia.end()-1,(coincidencia.end()-1)-(coincidencia.start()+7),line] for coincidencia in re.finditer(patron_classpiedpag, str(line[pos_busqueda_inicio:pos_busqueda_final]) )]
                    if coincidencias_nivel2_class:
                        for coinciden in coincidencias_nivel2_class:
                            
                            inicio = pos_busqueda_inicio+coinciden[0]
                            final =  pos_busqueda_inicio+coinciden[1]
                            texto = coinciden[3]
                            
                            if es_actualizacion:
                                modificacion_class= texto[:inicio]+ "Enfermedad_nivel2-actualizacion" + texto[final:] 
                                tam_letras_ENF=31
                            else:
                                modificacion_class= texto[:inicio]+ "Enfermedad_nivel2" + texto[final:] 
                                tam_letras_ENF=17
                            coinciden[3]= modificacion_class
                            line= coinciden[3]
                
                            pos_acummulado+=coinciden[2]-tam_letras_ENF
                    es_actualizacion=False
            pos_acummulado=0
            if line!="" and line!='\n' :  
                procesadofile.write(line + '\n')


# 
#       ENFERMEDADES NIVEL 0,1,2 ACTUALIZACIÓN
# 
ruta_salida1="CIE10LTP16EFN2.html" #archivo de salida
contenido= filerwpe.leer_archivo(ruta_salida1)
soup= filerwpe.parchear_archivo(contenido)


elementos_modificados = soup.find_all(class_="fc1 sc4")

for elem in elementos_modificados:
    coincidencias_nivel0 = [[coincidencia.start(),coincidencia.end()] for coincidencia in re.finditer(patron_codigo0_act, str(elem.get_text()) )]
    if coincidencias_nivel0:
        elem['class']="Enfermedad_nivel0-actualizacion"
    coincidencias_nivel0 = [[coincidencia.start(),coincidencia.end()] for coincidencia in re.finditer(patron_codigo0_2_act, str(elem.get_text()) )]
    if coincidencias_nivel0:
        elem['class']="Enfermedad_nivel0-actualizacion"
    coincidencias_nivel1 = [[coincidencia.start(),coincidencia.end()] for coincidencia in re.finditer(patron_codigo1_act, str(elem.get_text()) )]
    if coincidencias_nivel1:
        elem['class']="Enfermedad_nivel1-actualizacion"
    coincidencias_nivel2 = [[coincidencia.start(),coincidencia.end()] for coincidencia in re.finditer(patron_codigo2_act, str(elem.get_text()) )]
    if coincidencias_nivel2:
        elem['class']="Enfermedad_nivel2-actualizacion"


filerwpe.archivar_completo(str(soup),ruta_salida1)

# Asignamos el tiempo final
end_time = time.time()

# Imprimimos tiempo que ha tardado
print(f"Tiempo de ejecución: {end_time - start_time} segundos")