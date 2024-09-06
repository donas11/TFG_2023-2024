from cie10 import *
from cie10 import filerwpe
from cie10 import manager
from cie10 import printer
from cie10 import printer
from cie10 import fundiccionario
import time
import cie10
import xml.etree.ElementTree as diccionario

# Asignamos el tiempo de inicio        
start_time = time.time()

#Nombre de archivo de entrada 
ruta_entrada="CIE10LTPclasses.html"

# Crea el elemento raíz del XML
raiz = diccionario.Element("cie10")  # Creamos la raiz del dicionario <cie10>


contenido=filerwpe.leer_archivo(ruta_entrada) #leemos contenido del archivo  
soup= filerwpe.parchear_archivo(contenido) #parcheamos archivo a un elemento soup 

##############################################################################################################################################################
#   VARIABLES CON CONTENIDO DEL ARCHIVO TEMPORALES
############################################################################################################################################################## 

capitulo_actual=""   #variable para título del capítulo
capitulo_descripcion="" #variable para la descripciones/notas del capítulo

seccion_actual=""
seccion_descripcion=""

en0_descripcion=""
en1_descripcion=""
en2_descripcion=""


nota_actual=""
exten_actual=""
cofifique_cod_adicional=""
codifique_primero=""

ref_en_capitulo=""

incluye_actual=""
excluye_actual=""
excluye2_actual=""





##############################################################################################################################################################
#   VARIABLES CON CONTENIDO ESTRUCTURADO DEL ARCHIVO PARCIALES
############################################################################################################################################################## 


# variable de capitulos
variables_capitulos={}        #diccionario intermedio para capítulos
   

# variables de secciones
variables_secciones={}


# variables de enfermedades
variables_enfnv0={}
variables_enfnv1={}
variables_enfnv2={}

# variables para descripción de capítulos,secciones y enfermedades
variables_des_capitulos={}   #diccionario intermedio para descripción capítulos
variables_des_secciones={}    #diccionario intermedio para descripción secciones
variables_des_enfnv0={} 
variables_des_enfnv1={} 
variables_des_enfnv2={} 

# variables para Notas
variables_secc_notas={}
variables_enfn0_notas={}
variables_enfn1_notas={}
variables_enfn2_notas={}

# variables de excluyes
variables_excluyes={}
variables_excluyes_cap={}       #diccionario intermedio para excluyes de capítulos
variables_excluyes_ref={}       #diccionario intermedio para referencias de excluyes de capítulos

variables_excluyes_enf={}
variables_excluyes_enf1={}
variables_excluyes_enf2={}

variables_excluyes_enf_ref={}
variables_excluyes_enf1_ref={}
variables_excluyes_enf2_ref={}

# variables de incluyes
variables_incluyes_cap={}       #diccionario intermedio para incluyes de capítulos

variables_incluyes_enf={} 
variables_incluyes_enf1={}
variables_incluyes_enf2={}

variables_incluyes_ref={}       #diccionario intermedio para referencias de incluyes de capítulos
variables_incluyes_enf_ref={}

# variables de excluyes2
variables_excluyes2={} 
variables_excluyes2_cap={}   #diccionario intermedio para excluyes2 de capítulos
variables_excluyes2_enf={}
variables_excluyes2_enf1={}
variables_excluyes2_enf2={}


variables_excluyes2_ref={}   #diccionario intermedio para referencias de excluyes2 de capítulos
variables_excluyes2_enf_ref={}
variables_excluyes2_enf1_ref={}
variables_excluyes2_enf2_ref={}


# variables de codifique primero
variables_codifique_enf={}
variables_codifique_enf1={}
variables_codifique_enf2={}

variables_codifique_ref={}
variables_codifique_ref1={}
variables_codifique_ref2={}

# variables de extensión caracter
variables_enfn0_ext_car={}
variables_enfn1_ext_car={}
variables_enfn2_ext_car={}

# variables de codifique adicional
variables_codifique_adiccional_cap={}
variables_codifique_adiccional_enf0={}
variables_codifique_adiccional_enf1={}
variables_codifique_adiccional_enf2={}

# variables de referencias de codifique adicional
variables_codifiqueadi_cap={}
variables_codifiqueadi_ref0={}
variables_codifiqueadi_ref1={}
variables_codifiqueadi_ref2={}




##############################################################################################################################################################
#   VARIABLES CON NOMBRE DE LAS VARIABLES
############################################################################################################################################################## 

nom_var_cap=f"" #nombre_variable_capitulo

nom_var_secc=f"" #nombre_variable_seccion

non_var_enf_nv0=f"" #nombre_variable_enfermedad_nivel0
non_var_enf_nv1=f"" #nombre_variable_enfermedad_nivel0
non_var_enf_nv2=f"" #nombre_variable_enfermedad_nivel0


nom_var_secc_notas=f""
nom_var_enfn0_notas=f""
nom_var_enfn1_notas=f""
nom_var_enfn2_notas=f""


nom_var_des_cap=f"" #nombre_variable_descripcion_capitulo
nom_var_des_sec=f"" #nombre_variable_descripcion_seccion
nom_var_des_en0=f"" #nombre_variable_descripcion_enfermedadNivel0
nom_var_des_en1=f"" #nombre_variable_enfermedadNivel1
nom_var_des_en2=f"" #nombre_variable_enfermedadNivel2

nom_var_inc_cap=f"" #nombre_variable_incluye_capitulo
nom_var_inc_enf0=f""
nom_var_inc_enf1=f""
nom_var_inc_enf2=f""



nom_var_ref_inc=f"" #nombre_variable_referencia_incluye
nom_var_ref_inc_enf0=f""
nom_var_ref_inc_enf1=f""
nom_var_ref_inc_enf2=f""



nom_var_exc_cap=f"" #nombre_variable_excluye_capitulo
nom_var_exc_enf=f""
nom_var_exc_enf1=f""
nom_var_exc_enf2=f""


nom_var_exc2_cap=f"" #nombre_variable_excluye2_capitulo
nom_var_exc2_enf=f""
nom_var_exc2_enf1=f""
nom_var_exc2_enf2=f""



nom_var_ref_exc=f"" #nombre_variable_referencia_excluye
nom_var_ref_exc2=f"" #nombre_variable_referencia_excluye



nom_var_codpri_enf0=f""
nom_var_codpri_enf1=f""
nom_var_codpri_enf2=f""

nom_var_ref_codpri_enf0=f""
nom_var_ref_codpri_enf1=f""
nom_var_ref_codpri_enf2=f""

nom_var_enfn0_extcar=f""
nom_var_enfn1_extcar=f""
nom_var_enfn2_extcar=f""

nom_var_codadicional_cap=f""
nom_var_codadicional_enf2=f""
nom_var_codadicional_enf1=f""
nom_var_codadicional_enf0=f""

nom_var_ref_codadi_cap=f""
nom_var_ref_codadi_enf2=f""
nom_var_ref_codadi_enf1=f""
nom_var_ref_codadi_enf0=f""




##############################################################################################################################################################
#   VARIABLES CON CONTADORES de ID DE VARIABLES
############################################################################################################################################################## 


cont_capitulos=0  # Contador de capitulos
cont_secciones=0  # Contador de secciones 
cont_enfnv0=0 # Contador de Enfermedades nivel 0 
cont_enfnv1=0 # Contador de Enfermedades nivel 1 
cont_enfnv2=0 # Contador de Enfermedades nivel 2 

# Contadores de descripciones de capitulo,seccion,Enfermedad nivel 0, nivel 1, nivel 2
cont_des_capitulos=0 
cont_des_secciones=0  
cont_des_enfnv0=0 
cont_des_enfnv1=0 
cont_des_enfnv2=0 



# Contadores de excluyes de capitulo,Enfermedad nivel 0, nivel 1, nivel 2
cont_excluyes=0      
cont_excluyes_enf=0
cont_excluyes_enf1=0
cont_excluyes_enf2=0

# Contadores de excluye2 de capitulo,Enfermedad nivel 0, nivel 1, nivel 2
cont_excluyes2=0
cont_excluyes2_enf=0
cont_excluyes2_enf1=0
cont_excluyes2_enf2=0

# Contadores de referencias en excluyes en Enfermedad nivel 0, nivel 1, nivel 2
cont_ref_excluyes=0
cont_ref_excluyes_enf0=0
cont_ref_excluyes_enf1=0
cont_ref_excluyes_enf2=0

# Contadores de referencias en excluyes2 en Enfermedad nivel 0, nivel 1, nivel 2
cont_ref_excluyes2=0
cont_ref_excluyes2_enf=0
cont_ref_excluyes2_enf1=0
cont_ref_excluyes2_enf2=0

# Contadores de incluyes de capitulo,Enfermedad nivel 0, nivel 1, nivel 2
cont_incluyes=0
cont_incluyes_enf=0
cont_incluyes_enf1=0
cont_incluyes_enf2=0

# Contadores de referencias en incluyes en Enfermedad nivel 0, nivel 1, nivel 2
cont_ref_incluyes=0
cont_ref_incluyes_enf=0
cont_ref_incluyes_enf1=0
cont_ref_incluyes_enf2=0

# Contadores de Notas de capitulo,Enfermedad nivel 0, nivel 1, nivel 2
cont_secc_notas=0
cont_enfn0_notas=0
cont_enfn1_notas=0
cont_enfn2_notas=0

# Contadores de Extension de caracter de Enfermedad nivel 0, nivel 1, nivel 2
cont_enfn0_extcar=0
cont_enfn1_extcar=0
cont_enfn2_extcar=0

# Contadores de codifique primero de Enfermedad nivel 0, nivel 1, nivel 2
cont_codifique_enf0=0
cont_codifique_enf1=0
cont_codifique_enf2=0

# Contadores de referencias en codifique primero en Enfermedad nivel 0, nivel 1, nivel 2
cont_ref_codpri_enf0=0
cont_ref_codpri_enf1=0
cont_ref_codpri_enf2=0

# Contadores de codigos adicionales en Capitulo, Enfermedad nivel 0, nivel 1, nivel 2
cont_codifique_adiccional_cap=0
cont_codifique_adiccional_enf1=0
cont_codifique_adiccional_enf0=0
cont_codifique_adiccional_enf2=0
# Contadores de referencias en codigo adicional en Capitulo, Enfermedad nivel 0, nivel 1, nivel 2
cont_ref_codadi_cap=0
cont_ref_codadi_enf0=0
cont_ref_codadi_enf1=0
cont_ref_codadi_enf2=0



##############################################################################################################################################################
#   VARIABLES DE CODIGOs DE LA ENFERMEDAD EN EL NIVEL
############################################################################################################################################################## 

cod_nivel0={}
cod_nivel1={}
cod_nivel2={}

##############################################################################################################################################################
#   VARIABLES DE CONTROL DEL BUCLE WHILE
############################################################################################################################################################## 

control_nv0=0
control_nv1=0
control_nv2=0

##############################################################################################################################################################
#   VARIABLES DE CONTROL DE ACTUALIZADO
############################################################################################################################################################## 

actualizado=1
noactualizado=0

##############################################################################################################################################################
#   VARIABLES DE CONTROL DE FINALIZACIÓN
############################################################################################################################################################## 

cont_finalizar=0 # variable para conocer si necestitamos finalizar
final=14 # variable finalizador de número maximo de bucle

utltimo_siguiente=0


lista_ref_enfermedad=list() # Lista temporal para almacenar referencias de enfermedades

# import ipdb; ipdb.set_trace();

primer_elemento = soup.find(class_="Capitulo")
siguiente = primer_elemento
nuevo_siguiente= siguiente.find_next()

while siguiente : # Mientras haya siguiente elemento
    ##############################################################################################################################################################
    #   CAPITULO
    ############################################################################################################################################################## 
    siguiente,capitulo_actual=fundiccionario.leer_token(siguiente,"Capitulo")
    #Si hemos leido el capítulo 
    if capitulo_actual != "":
        #aumentamos el contador de capitulo                
        cont_capitulos += 1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">
        raiz,variables_capitulos,nom_var_cap,capitulo_actual,cont_capitulos = fundiccionario.asignar_contenido(raiz,variables_capitulos,capitulo_actual,cont_capitulos, "capitulo","Titulo")
        
    ##############################################################################################################################################################
    #   CAPITULO-DESCRIPCCION
    ##############################################################################################################################################################                                                          
    siguiente,capitulo_descripcion=fundiccionario.leer_token(siguiente,"Capitulo-Descripcion")

    #Si hemos leido la descripcion del capítulo 
    if capitulo_descripcion != "":      
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Descripcion>
        variables_des_capitulos[nom_var_des_cap],nom_var_des_cap,capitulo_descripcion,cont_des_capitulos = fundiccionario.asignar_especificacion(variables_capitulos[nom_var_cap],variables_des_capitulos,capitulo_descripcion,cont_des_capitulos,"Descripcion") 
        
        #reiniciamos variable
        capitulo_descripcion=""  
        
       
    ##############################################################################################################################################################
    #   CAPITULO-INCLUYE
    ############################################################################################################################################################## 
    siguiente,incluye_actual=fundiccionario.leer_token(siguiente,"Incluye")
    #Si hemos leido el incluye del capítulo 
    if incluye_actual != "":
        #aumentamos el contador de incluyes                
        cont_incluyes+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Incluye>
        variables_incluyes_cap[nom_var_cap],variables_incluyes_cap,nom_var_inc_cap = fundiccionario.asignar(variables_capitulos[nom_var_cap],variables_incluyes_cap,cont_incluyes,"Incluye")
        
        
        #buscamos referencias en el incluye
        lista_ref_enfermedad=manager.buscar_referencias(incluye_actual) 

        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Incluye>  ref_enfermedad[0] <Refere_enfermedad>
            
            variables_incluyes_ref,variables_incluyes_cap,cont_ref_incluyes = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_incluyes_ref,cont_ref_incluyes,variables_incluyes_cap,nom_var_inc_cap,"enfermedad","Referencia")

        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Incluye> incluye_actual
            variables_incluyes_cap[nom_var_inc_cap].text=incluye_actual  

    # reiniciamos variables
    incluye_actual="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades

    ##############################################################################################################################################################
    #   CAPITULO-INCLUYE-UTILICE_CODIGO_ADICIONAL 
    ############################################################################################################################################################## 
    siguiente,cofifique_cod_adicional=fundiccionario.leer_tokencondescripcion(siguiente,"Utilice-codigo-adicional")
    #Si hemos leido el código adicional del capítulo 
    if cofifique_cod_adicional != "" :
        #aumentamos el contador de incluyes
        cont_codifique_adiccional_cap+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Incluye> <Utilice-codigo-adicional>
        variables_capitulos[nom_var_cap],variables_codifique_adiccional_cap,nom_var_codadicional_cap = fundiccionario.asignar(variables_capitulos[nom_var_cap],variables_codifique_adiccional_cap,nom_var_codadicional_cap,"Utilice_Codigo_adicional")
        
        #buscamos referencias en el incluye
        lista_ref_enfermedad=manager.buscar_referencias(cofifique_cod_adicional) 

        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">  <Incluye> <Utilice-codigo-adicional> <Referencia_enfermedad Referencia= =ref_enfermedad[0]> 
            variables_codifiqueadi_cap,variables_codifique_adiccional_cap,cont_ref_codadi_cap= fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_codifiqueadi_cap,cont_ref_codadi_cap,variables_codifique_adiccional_cap,nom_var_codadicional_cap,"enfermedad","Referencia")
           
        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Incluye> <Utilice-codigo-adicional> cofifique_cod_adicional
            variables_codifique_adiccional_cap[nom_var_codadicional_cap].text=cofifique_cod_adicional  

        # reiniciamos variable de control
        control_nv2=0

    # reiniciamos variables 
    cofifique_cod_adicional="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
      
    ##############################################################################################################################################################
    #   CAPITULO-EXCLUYE
    ############################################################################################################################################################## 
    siguiente,excluye_actual=fundiccionario.leer_token(siguiente,"Excluye")
    #Si hemos leido la Excluye del capítulo 
    if excluye_actual != "":
        #aumentamos el contador de excluyes
        cont_excluyes+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Excluye> 
        variables_capitulos[nom_var_cap],variables_excluyes_cap,nom_var_exc_cap = fundiccionario.asignar(variables_capitulos[nom_var_cap],variables_excluyes_cap,cont_excluyes,"Excluye")
        
        #buscamos referencias en el excluye
        lista_ref_enfermedad=manager.buscar_referencias(excluye_actual) 

        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Excluye> <Referencia_enfermedad Referencia= =ref_enfermedad[0]> 
            variables_excluyes_ref,variables_excluyes_cap,cont_ref_excluyes = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_excluyes_ref,cont_ref_excluyes,variables_excluyes_cap,nom_var_exc_cap,"enfermedad","Referencia")
            
        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Excluye> excluye_actual
            variables_excluyes_cap[nom_var_exc_cap].text=excluye_actual
    # reiniciamos variables
    excluye_actual=""
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades

    ##############################################################################################################################################################
    #   CAPITULO-EXCLUYE2
    ############################################################################################################################################################## 
    siguiente,excluye2_actual=fundiccionario.leer_token(siguiente,"Excluye2")
    #Si hemos leido la Excluye2 del capítulo
    if excluye2_actual != "":
        #aumentamos el contador de excluyes
        cont_excluyes2+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Excluye2>
        variables_capitulos[nom_var_cap],variables_excluyes2_cap,nom_var_exc2_cap = fundiccionario.asignar(variables_capitulos[nom_var_cap],variables_excluyes2_cap,cont_excluyes2,"Excluye2")
        


        #buscamos referencias en el excluye
        lista_ref_enfermedad=manager.buscar_referencias(excluye2_actual) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:    
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Excluye2> <Referencia_enfermedad Referencia= =ref_enfermedad[0]>  
            variables_excluyes2_ref,variables_excluyes2_cap,cont_ref_excluyes2 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_excluyes2_ref,cont_ref_excluyes2,variables_excluyes2_cap,nom_var_exc2_cap,"enfermedad","Referencia")
                       
        else:     
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Excluye2> excluye2_actual
            variables_excluyes2_cap[nom_var_exc2_cap].text=excluye2_actual
    # reiniciamos variables
    excluye2_actual=""
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades

    ##############################################################################################################################################################
    #   CAPITULO-SECCION
    ############################################################################################################################################################## 
    siguiente,seccion_actual=fundiccionario.leer_token(siguiente,"Seccion")
    #Si hemos leido la Seccion del capítulo
    if seccion_actual != "":
        
        #aumentamos el contador de secciones
        cont_secciones+=1
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> 
        variables_capitulos[nom_var_cap],variables_secciones,nom_var_secc,seccion_actual,cont_secciones =  fundiccionario.asignar_contenido(variables_capitulos[nom_var_cap],variables_secciones,seccion_actual,cont_secciones, "Seccion","Titulo")               
        
 
        siguiente,seccion_descripcion=fundiccionario.leer_token(siguiente,"Seccion-Descripcion")       
        #Si hemos leido la descripcion de la Seccion del capítulo 
        if seccion_descripcion != "":
            # #aumentamos el contador de secciones           
            # cont_secciones+=1
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Descripcion>
            variables_des_secciones,nom_var_des_sec,seccion_descripcion,cont_des_secciones = fundiccionario.asignar_especificacion(variables_secciones[nom_var_secc],variables_des_secciones,seccion_descripcion,cont_des_secciones,"Descripcion")

            # reiniciamos variable 
            seccion_descripcion=""
    # reiniciamos variable        
    seccion_actual="" 

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-NOTA
    ############################################################################################################################################################## 
    siguiente,nota_actual=fundiccionario.leer_token(siguiente,"Nota")
    #Si hemos leido la nota de la sección 
    if nota_actual != "":                
        #aumentamos el contador de notas de seccion 
        cont_secc_notas+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Nota> nota_actual
        variables_secc_notas,nom_var_secc_notas,nota_actual,cont_secc_notas = fundiccionario.asignar_especificacion(variables_secciones[nom_var_secc],variables_secc_notas,nota_actual,cont_secc_notas,"Nota")
        
        # reiniciamos variable 
        nota_actual = ""

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0
    ############################################################################################################################################################## 
    #Si lo siquiente que leemos es Enfermedad de nivel 0
    if "Enfermedad_nivel0" in siguiente['class']:
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0>
        cont_enfnv0,non_var_enf_nv0,variables_enfnv0,cod_nivel0,variables_secciones[nom_var_secc] = fundiccionario.asignar_elemento_nivel(cont_enfnv0,variables_enfnv0,"Enfermedad-Nivel0",cod_nivel0,0,siguiente,variables_secciones[nom_var_secc])
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0 Codigo=cod_nivel[0]> siguiente.text     
        siguiente,variables_enfnv0,non_var_enf_nv0,control_nv0 =fundiccionario.asignar_codigo(siguiente, non_var_enf_nv0, variables_enfnv0,control_nv0,cod_nivel0,noactualizado)
  
        siguiente,en0_descripcion=fundiccionario.leer_token(siguiente,"Enfermedad_nivel0-Descripcion")
        #Si hemos leido la descripcción de la Enfermedad
        if en0_descripcion != "":
            #aumentamos el contador de descripcción
            cont_enfnv0+=1

            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Descripcion> en0_descripcion </Descripcion>
            variables_des_enfnv0,nom_var_des_en0,en0_descripcion,cont_enfnv0 = fundiccionario.asignar_especificacion_consubtitulo(variables_enfnv0[non_var_enf_nv0],variables_des_enfnv0,en0_descripcion,cont_enfnv0,"Descripcion","Enfermedad-Nivel0")
                       
            #reiniciamos variable
            en0_descripcion=""
    
    #Si lo siquiente que leemos es Enfermedad actualizada de nivel 0 
    if "Enfermedad_nivel0-actualizacion" in siguiente['class']:
        #aumentamos el contador de enfermedad de nivel 0
        cont_enfnv0+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0>
        cont_enfnv0,non_var_enf_nv0,variables_enfnv0,cod_nivel0,variables_secciones[nom_var_secc]= fundiccionario.asignar_elemento_nivel(cont_enfnv0,variables_enfnv0,"Enfermedad-Nivel0",cod_nivel0,0,siguiente,variables_secciones[nom_var_secc])
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0 Codigo=cod_nivel[0] Actualizado="cierto" > siguiente.text  
        siguiente,variables_enfnv0,non_var_enf_nv0,control_nv0 = fundiccionario.asignar_codigo(siguiente, non_var_enf_nv0, variables_enfnv0,control_nv0,cod_nivel0,actualizado)
       
       

        #Si lo siquiente que leemos es la descripccion de Enfermedad de nivel 0
        while "Enfermedad_nivel0-actualizacion-Descripcion" in siguiente['class'] or "Enfermedad_nivel0-Descripcion" in siguiente['class']: 
            en0_descripcion+=siguiente.text  #añadimos contenido del texto a la descripcion del nivel 0
            siguiente = siguiente.find_next()   #  #seguimos pasando al siguiente proximo 
            # si estamos en parte que pertenece al Pie de página
            while "Pie-de-pagina" in siguiente['class']: 
                siguiente = siguiente.find_next()    #seguimos pasando al siguiente proximo
            
        if en0_descripcion != "":
            #aumentamos el contador de enfermedades de nivel 0
            cont_enfnv0+=1
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0 Actualizado="cierto> <Descripcion> en0_descripcion </Descripcion>
            variables_des_enfnv0,nom_var_des_en0,en0_descripcion,cont_enfnv0 = fundiccionario.asignar_especificacion_consubtitulo(variables_enfnv0[non_var_enf_nv0],variables_des_enfnv0,en0_descripcion,cont_enfnv0,"Descripcion","Enfermedad-Nivel0")
            
            #reiniciamos variable
            en0_descripcion=""
    

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-NOTA
    ############################################################################################################################################################## 
    siguiente,nota_actual=fundiccionario.leer_token(siguiente,"Nota")
    #Si hemos leido la nota de la enfermedad de nivel 0 
    if nota_actual != "":
        #aumentamos el contador de notas de enfermedades de nivel 0                
        cont_enfn0_notas+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Nota> nota_actual
        variables_enfn0_notas,nom_var_enfn0_notas,nota_actual,cont_enfn0_notas = fundiccionario.asignar_especificacion(variables_enfnv0[non_var_enf_nv0],variables_enfn0_notas,nota_actual,cont_enfn0_notas,"Nota")
               
        # reiniciamos variable
        nota_actual = ""

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-EXTENSIONCARACTER
    ##############################################################################################################################################################   
    siguiente,exten_actual=fundiccionario.leer_tokencondescripcionext(siguiente,"extension-caracter")
    #Si hemos leido la extensión de caracter
    if exten_actual != "":
        #aumentamos el contador de extensiones de caracter de enfermedades de nivel 0                
        cont_enfn0_extcar+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Extension-Caracter> exten_actual </Extension-Caracter>
        variables_enfn0_ext_car,nom_var_enfn0_extcar,exten_actual,cont_enfn0_extcar = fundiccionario.asignar_especificacion(variables_enfnv0[non_var_enf_nv0],variables_enfn0_ext_car,exten_actual,cont_enfn0_extcar,"Extension-Caracter")
                
        #reiniciamos variable
        exten_actual = ""

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-INCLUYE
    ############################################################################################################################################################## 
    siguiente,incluye_actual=fundiccionario.leer_token(siguiente,"Incluye")
    #Si hemos leido el incluye de la enfermedad de nivel 0 
    if incluye_actual != "" and control_nv0 == 1:                
        #aumentamos el contador de incluyes de enfermedades de nivel 0                
        cont_incluyes_enf+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <Incluye>
        variables_enfnv0[non_var_enf_nv0],variables_incluyes_enf,nom_var_inc_enf0 = fundiccionario.asignar(variables_enfnv0[non_var_enf_nv0],variables_incluyes_enf,cont_incluyes_enf,"Incluye")
        
             
        #buscamos referencias en el incluye
        lista_ref_enfermedad=manager.buscar_referencias(incluye_actual) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <Incluye>  <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad>
            variables_incluyes_ref,variables_incluyes_enf,cont_ref_incluyes_enf = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_incluyes_ref,cont_ref_incluyes_enf,variables_incluyes_enf,nom_var_inc_enf0,"enfermedad","Referencia")
            
        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Incluye> incluye_actual
            if incluye_actual is not None:
                variables_incluyes_enf[nom_var_inc_enf0].text=incluye_actual  
        # reiniciamos variable
        control_nv0=0
    # reiniciamos variables
    incluye_actual="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
    


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-EXCLUYE
    ############################################################################################################################################################## 
    siguiente,excluye_actual=fundiccionario.leer_token(siguiente,"Excluye")
    #Si hemos leido el Excluye de la enfermedad de nivel 0 
    if excluye_actual != "" and control_nv0 == 1:
        #aumentamos el contador de excluyes de enfermedades de nivel 0
        cont_excluyes_enf+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <Excluye>  
        variables_enfnv0[non_var_enf_nv0],variables_excluyes_enf,nom_var_exc_enf = fundiccionario.asignar(variables_enfnv0[non_var_enf_nv0],variables_excluyes_enf,cont_excluyes_enf,"Excluye")
        

        #buscamos referencias en el excluye
        lista_ref_enfermedad=manager.buscar_referencias(excluye_actual) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:    
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">  <Seccion> <EnfernedadNivel0> <Excluye>  <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad>
            variables_excluyes_enf_ref,variables_excluyes_enf,cont_ref_excluyes_enf0 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_excluyes_enf_ref,cont_ref_excluyes_enf0,variables_excluyes_enf,nom_var_exc_enf,"enfermedad","Referencia")

        else:   
             #aumentamos el contador de excluyes de enfermedades de nivel 0   
            cont_excluyes_enf+=1
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <Excluye> excluye_actual
            variables_excluyes_enf,nom_var_exc_enf,excluye_actual,cont_excluyes_enf = fundiccionario.asignar_especificacion(raiz,variables_excluyes_enf,excluye_actual,cont_excluyes_enf,"Excluye")
            
        # reiniciamos variable
        control_nv0=0
    # reiniciamos variables    
    excluye_actual=""
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-EXCLUYE2
    ##############################################################################################################################################################
    siguiente,excluye2_actual=fundiccionario.leer_token(siguiente,"Excluye2")
    #Si hemos leido la Excluye2 de la enfermedad de nivel 0 
    if excluye2_actual != "" and control_nv0 == 1:
        #aumentamos el contador de excluyes2 de enfermedades de nivel 0
        cont_excluyes2_enf+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">  <Seccion> <EnfernedadNivel0> <Excluye2> 
        variables_enfnv0[non_var_enf_nv0],variables_excluyes2_enf,nom_var_exc2_enf = fundiccionario.asignar(variables_enfnv0[non_var_enf_nv0],variables_excluyes2_enf,cont_excluyes2_enf,"Excluye2")
        

        #buscamos referencias en el excluye
        lista_ref_enfermedad=manager.buscar_referencias(excluye2_actual) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:    
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <Excluye2> <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad>
            variables_excluyes2_enf_ref,variables_excluyes2_enf,cont_ref_excluyes2_enf= fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_excluyes2_enf_ref,cont_ref_excluyes2_enf,variables_excluyes2_enf,nom_var_exc2_enf,"enfermedad","Referencia")

        else:
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <Excluye2> excluye2_actual   
            variables_excluyes2_enf[nom_var_exc2_enf].text=excluye2_actual
        # reiniciamos variable
        control_nv0=0
    # reiniciamos variables
    excluye2_actual=""
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-CODIFIQUE_PRIMERO
    ############################################################################################################################################################## 
    siguiente,codifique_primero=fundiccionario.leer_tokencondescripcionext(siguiente,"Codifique-primero")
    #Si hemos leido el codifique primero de la enfermedad del nivel 0
    if codifique_primero != "" and control_nv0 == 1:                
        
        #aumentamos el contador de codifique primero de enfermedades de nivel 0                           
        cont_codifique_enf0+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0><Codifique-primero>
        variables_enfnv0[non_var_enf_nv0],variables_codifique_enf,nom_var_codpri_enf0 = fundiccionario.asignar(variables_enfnv0[non_var_enf_nv0],variables_codifique_enf,cont_codifique_enf0,"Codifique_Primero")        
        

        #buscamos referencias en el codifique primero
        lista_ref_enfermedad=manager.buscar_referencias(codifique_primero) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   

            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <Codifique_Primero>  <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad> 
            variables_codifique_ref,variables_codifique_enf,cont_ref_codpri_enf0 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_codifique_ref,cont_ref_codpri_enf0,variables_codifique_enf,nom_var_codpri_enf0,"enfermedad","Referencia")

        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">  <Seccion> <EnfernedadNivel0><Codifique-primero> codifique_primero
            variables_codifique_enf[nom_var_codpri_enf0].text=codifique_primero  
        # reiniciamos variable
        control_nv0=0
    # reiniciamos variable
    codifique_primero="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
        


    

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-UTILICE_CODIGO_ADICIONAL
    ##############################################################################################################################################################     
    siguiente,cofifique_cod_adicional=fundiccionario.leer_tokencondescripcion(siguiente,"Utilice-codigo-adicional")
    #Si hemos leido el Utilice codigo adicional de enfermedades de nivel 0  
    if cofifique_cod_adicional != "" and control_nv0 == 1:                
        #aumentamos el contador de Utilice codigo adicional de enfermedades de nivel 0                           
        cont_codifique_adiccional_enf0+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0><Utilice-codigo-adicional>
        variables_enfnv0[non_var_enf_nv0],variables_codifique_adiccional_enf0,nom_var_codadicional_enf0 = fundiccionario.asignar(variables_enfnv0[non_var_enf_nv0],variables_codifique_adiccional_enf0,cont_codifique_adiccional_enf0,"Utilice_Codigo_adicional")
        


        #buscamos referencias en el Utilice codigo adicional
        lista_ref_enfermedad=manager.buscar_referencias(cofifique_cod_adicional) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Codifique_Primero>  <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad> 
            variables_codifiqueadi_ref0,variables_codifique_adiccional_enf0,cont_ref_codadi_enf0 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_codifiqueadi_ref0,cont_ref_codadi_enf0,variables_codifique_adiccional_enf0,nom_var_codadicional_enf0,"enfermedad","Referencia")
            
        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Utilice-codigo-adicional> cofifique_cod_adicional
            variables_codifique_adiccional_enf0[nom_var_codadicional_enf0].text=cofifique_cod_adicional  
        # reiniciamos variable
        control_nv2=0
    # reiniciamos variables
    cofifique_cod_adicional="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
    








    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1
    ##############################################################################################################################################################  
    #Si lo siquiente que leemos es Enfermedad de nivel 1
    if "Enfermedad_nivel1" in siguiente['class']:
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1>
        cont_enfnv1,non_var_enf_nv1,variables_enfnv1,cod_nivel1,variables_enfnv0[non_var_enf_nv0] = fundiccionario.asignar_elemento_nivel(cont_enfnv1,variables_enfnv1,"Enfermedad-Nivel1",cod_nivel1,1,siguiente,variables_enfnv0[non_var_enf_nv0])
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1 Codigo=cod_nivel[0]> siguiente.text     
        siguiente,variables_enfnv1,non_var_enf_nv1,control_nv1 = fundiccionario.asignar_codigo(siguiente, non_var_enf_nv1, variables_enfnv1,control_nv1,cod_nivel1,noactualizado)

        siguiente,en1_descripcion=fundiccionario.leer_token(siguiente,"Enfermedad_nivel1-Descripcion")

        #Si hemos leido la descripcción de la Enfermedad
        if en1_descripcion != "":
            #aumentamos el contador de enfermedad nivel 1
            cont_enfnv1+=1

            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0>  <Enfermedad-Nivel1>  <Descripcion> en1_descripcion </Descripcion>
            variables_des_enfnv1,nom_var_des_en1,en1_descripcion,cont_enfnv1 = fundiccionario.asignar_especificacion_consubtitulo(variables_enfnv1[non_var_enf_nv1],variables_des_enfnv1,en1_descripcion,cont_enfnv1,"Descripcion","Enfermedad-Nivel1")
            
            
            #reiniciamos variable
            en1_descripcion=""
        

    #Si lo siquiente que leemos es Enfermedad actualizada de nivel 1
    if "Enfermedad_nivel1-actualizacion" in siguiente['class']:
        #aumentamos el contador de enfermedad de nivel 1
        cont_enfnv1+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1>
        cont_enfnv1,non_var_enf_nv1,variables_enfnv1,cod_nivel1,variables_enfnv0[non_var_enf_nv0]= fundiccionario.asignar_elemento_nivel(cont_enfnv1,variables_enfnv1,"Enfermedad-Nivel1",cod_nivel1,1,siguiente,variables_enfnv0[non_var_enf_nv0])
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1 Actualizado="cierto" Codigo=cod_nivel[0]> siguiente.text   
        siguiente,variables_enfnv1,non_var_enf_nv1,control_nv1 = fundiccionario.asignar_codigo(siguiente, non_var_enf_nv1, variables_enfnv1,control_nv1,cod_nivel1,actualizado)

        #Si lo siquiente que leemos es la descripccion de Enfermedad de nivel 1
        while "Enfermedad_nivel1-actualizacion-Descripcion" in siguiente['class'] or "Enfermedad_nivel1-Descripcion" in siguiente['class']: 
            en0_descripcion+=siguiente.text #añadimos contenido del texto a la descripcion de enfermedad del nivel 1
            siguiente = siguiente.find_next()   #seguimos pasando al siguiente proximo
            # si estamos en parte que pertenece al Pie de página
            while "Pie-de-pagina" in siguiente['class']:
                siguiente = siguiente.find_next() #seguimos pasando al siguiente proximo
           
           
        if en1_descripcion != "":
            #aumentamos el contador de enfermedades de nivel 1
            cont_enfnv1+=1
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1 Actualizado="cierto> <Descripcion> en1_descripcion </Descripcion>
            variables_des_enfnv1,nom_var_des_en1,en1_descripcion,cont_enfnv1 = fundiccionario.asignar_especificacion_consubtitulo(variables_enfnv1[non_var_enf_nv1],variables_des_enfnv1,en1_descripcion,cont_enfnv1,"Descripcion","Enfermedad-Nivel1")
            
            #reiniciamos variable
            en1_descripcion=""
            # activamos variable de que ya estamos em nivel1
            control_nv1=1





    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-NOTA
    ############################################################################################################################################################## 
    siguiente,cofifique_cod_adicional=fundiccionario.leer_token(siguiente,"Nota")
    #Si hemos leido la nota de la enfermedad de nivel 1 
    if nota_actual != "":
        #aumentamos el contador de notas de enfermedades de nivel 1
        cont_enfn1_notas+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Nota> nota_actual
        variables_enfn1_notas,nom_var_enfn1_notas,nota_actual,cont_enfn1_notas =  asignar_especificacion(variables_enfnv1[non_var_enf_nv1],variables_enfn1_notas,nota_actual,cont_enfn1_notas,"Nota")
        
        #reiniciamos variable
        nota_actual = ""

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-EXTENSIONCARACTER
    ############################################################################################################################################################## 
    siguiente,exten_actual=fundiccionario.leer_tokencondescripcionext(siguiente,"extension-caracter")
    #Si hemos leido la extensiones de caracter de la enfermedad de nivel 1
    if exten_actual != "":
        #aumentamos el contador de extensiones de caracter de enfermedades de nivel 1
        cont_enfn1_extcar+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion>  <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Extension-Caracter> exten_actual </Extension-Caracter>
        variables_enfn1_ext_car,nom_var_enfn1_extcar,exten_actual,cont_enfn1_extcar = fundiccionario.asignar_especificacion(variables_enfnv1[non_var_enf_nv1],variables_enfn1_ext_car,exten_actual,cont_enfn1_extcar,"Extension-Caracter")
   
        #reiniciamos variable
        exten_actual = ""



    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-INCLUYE
    ############################################################################################################################################################## 
    siguiente,incluye_actual=fundiccionario.leer_token(siguiente,"Incluye")
    #Si hemos leido el incluye de la enfermedad de nivel 1 
    if incluye_actual != "" and control_nv0 == 1 and incluye_actual is not None:
        #aumentamos el contador de incluyes de enfermedades de nivel 1
        cont_incluyes_enf1+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1><Incluye>
        variables_enfnv1[non_var_enf_nv1],variables_incluyes_enf1,nom_var_inc_enf1 = fundiccionario.asignar(variables_enfnv1[non_var_enf_nv1],variables_incluyes_enf1,cont_incluyes_enf1,"Incluye")
        

        #buscamos referencias en el incluye
        lista_ref_enfermedad=manager.buscar_referencias(incluye_actual)
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Incluye>  <EnfernedadNivel0> <EnfernedadNivel1> <Incluye>  <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad> 
            variables_incluyes_ref,variables_incluyes_enf1,cont_ref_incluyes_enf1 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_incluyes_ref,cont_ref_incluyes_enf1,variables_incluyes_enf1,nom_var_inc_enf1,"enfermedad","Referencia")
   
        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Incluye> incluye_actual
            variables_incluyes_enf1[nom_var_inc_enf1].text=incluye_actual  
        # reiniciamos variable
        control_nv1=0
    # reiniciamos variables
    incluye_actual="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
    


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-EXCLUYE
    ############################################################################################################################################################## 
    siguiente,excluye_actual=fundiccionario.leer_token(siguiente,"Excluye")
    #Si hemos leido la Excluye de la enfermedad de nivel 1
    if excluye_actual != "" and control_nv0 == 1:
        #aumentamos el contador de Utilice codigo adicional de enfermedades de nivel 1
        cont_excluyes_enf1+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Excluye> 
        variables_enfnv1[non_var_enf_nv1],variables_excluyes_enf1,nom_var_exc_enf1 = fundiccionario.asignar(variables_enfnv1[non_var_enf_nv1],variables_excluyes_enf1,cont_excluyes_enf1,"Excluye")
        

        #buscamos referencias en el excluye
        lista_ref_enfermedad=manager.buscar_referencias(excluye_actual)
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:    
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Excluye> <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad> 
            variables_excluyes_enf1_ref,variables_excluyes_enf1,cont_ref_excluyes_enf1 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_excluyes_enf1_ref,cont_ref_excluyes_enf1,variables_excluyes_enf1,nom_var_exc_enf1,"enfermedad","Referencia")
         
        else:
            #aumentamos el contador de Utilice codigo adicional de enfermedades de nivel 1
            cont_excluyes_enf1+=1

            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Excluye> excluye_actual    
            variables_excluyes_enf1,nom_var_exc_enf1,excluye_actual,cont_excluyes_enf1 = fundiccionario.asignar_especificacion(variables_enfnv1[non_var_enf_nv1],variables_excluyes_enf1,excluye_actual,cont_excluyes_enf1,"Excluye")
            
        # reiniciamos variable
        control_nv1=0
    # reiniciamos variables
    excluye_actual=""
    lista_ref_enfermedad.clear()


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-EXCLUYE2
    ############################################################################################################################################################## 
    siguiente,excluye2_actual=fundiccionario.leer_token(siguiente,"Excluye2")
    #Si hemos leido la Excluye2 del capítulo 
    if excluye2_actual != "" and control_nv0 == 1:
        #aumentamos el contador de excluyes2 de enfermedades de nivel 1
        cont_excluyes2_enf1+=1
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Excluye2> 
        variables_enfnv1[non_var_enf_nv1],variables_excluyes2_enf1,nom_var_exc2_enf1 = fundiccionario.asignar(variables_enfnv1[non_var_enf_nv1],variables_excluyes2_enf1,cont_excluyes2_enf1,"Excluye2")
        

        #buscamos referencias en el excluye2
        lista_ref_enfermedad=manager.buscar_referencias(excluye2_actual) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:    
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Excluye2> <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad>
            variables_excluyes2_enf1_ref,variables_excluyes2_enf1,cont_ref_excluyes2_enf1 =fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_excluyes2_enf1_ref,cont_ref_excluyes2_enf1,variables_excluyes2_enf1,nom_var_exc2_enf1,"enfermedad","Referencia")
        
        else:     
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Excluye2> excluye2_actual   
            variables_excluyes2_enf1[nom_var_exc2_enf1].text=excluye2_actual
        # reiniciamos variable    
        control_nv1=0
    # reiniciamos variables
    excluye2_actual=""
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades



    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-CODIFIQUE_PRIMERO
    ############################################################################################################################################################## 
    siguiente,codifique_primero=fundiccionario.leer_tokencondescripcionext(siguiente,"Codifique-primero")
    #Si hemos leido el codifique primero de la enfermedad de nivel 1   
    if codifique_primero != "" and control_nv1 == 1:
        # aumentamos el contador de codifique primero de enfermedades de nivel 1   
        cont_codifique_enf1+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Codifique-primero>
        variables_enfnv1[non_var_enf_nv1],variables_codifique_enf1,nom_var_codpri_enf1 = fundiccionario.asignar(variables_enfnv1[non_var_enf_nv1],variables_codifique_enf1,cont_codifique_enf1,"Codifique_Primero")
        


        #buscamos referencias en el incluye
        lista_ref_enfermedad=manager.buscar_referencias(codifique_primero) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:

            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">  <Seccion> <EnfernedadNivel0> <EnfernedadNivel1>  <Codifique_Primero>  <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad>    
            variables_codifique_ref1,variables_codifique_enf1,cont_ref_codpri_enf1 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_codifique_ref1,cont_ref_codpri_enf1,variables_codifique_enf1,nom_var_codpri_enf1,"enfermedad","Referencia")
            
        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Codifique-primero> codifique_primero
            variables_codifique_enf1[nom_var_codpri_enf1].text=codifique_primero  
        # reiniciamos variable
        control_nv1=0
    # reiniciamos variables
    codifique_primero="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
    


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-UTILICE_CODIGO_ADICIONAL
    ############################################################################################################################################################## 
    siguiente,cofifique_cod_adicional=fundiccionario.leer_tokencondescripcion(siguiente,"Utilice-codigo-adicional")
    #Si hemos leido el incluye de la enfermedad de nivel 1
    if cofifique_cod_adicional != "" and control_nv1 == 1:
        #aumentamos el contador de Utilice codigo adicional de enfermedades de nivel 1
        cont_codifique_adiccional_enf1+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Utilice-codigo-adicional>
        variables_enfnv1[non_var_enf_nv1],variables_codifique_adiccional_enf1,nom_var_codadicional_enf1 = fundiccionario.asignar(variables_enfnv1[non_var_enf_nv1],variables_codifique_adiccional_enf1,cont_codifique_adiccional_enf1,"Utilice_Codigo_adicional")
        

        #buscamos referencias en Utilice codigo adicional
        lista_ref_enfermedad=manager.buscar_referencias(cofifique_cod_adicional) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Codifique_Primero> <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad> 
            variables_codifiqueadi_ref1,variables_codifique_adiccional_enf1,cont_ref_codadi_enf1 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_codifiqueadi_ref1,cont_ref_codadi_enf1,variables_codifique_adiccional_enf1,nom_var_codadicional_enf1,"enfermedad","Referencia")

        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Codifique_Primero> codifique_primero
            variables_codifique_adiccional_enf1[nom_var_codadicional_enf1].text=cofifique_cod_adicional
        # reiniciamos variable
        control_nv2=0
    # reiniciamos variables
    cofifique_cod_adicional=""
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
 

   


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-ENFERMEDADNIVEL2
    ############################################################################################################################################################## 
    #Si lo siquiente que leemos es Enfermedad de nivel 2
    if "Enfermedad_nivel2" in siguiente['class']:
       
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Enfermedad-Nivel2>
        cont_enfnv2,non_var_enf_nv2,variables_enfnv2,cod_nivel2,variables_enfnv1[non_var_enf_nv1] = fundiccionario.asignar_elemento_nivel(cont_enfnv2,variables_enfnv2,"Enfermedad-Nivel2",cod_nivel2,2,siguiente,variables_enfnv1[non_var_enf_nv1])
   
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Enfermedad-Nivel2 Codigo=cod_nivel[0]> siguiente.text
        siguiente,variables_enfnv2,non_var_enf_nv2,control_nv = fundiccionario.asignar_codigo(siguiente, non_var_enf_nv2, variables_enfnv2,control_nv2,cod_nivel2,noactualizado)
             
        siguiente,en2_descripcion,cont_finalizar = fundiccionario.leer_token_confinalizacion(siguiente,"Enfermedad_nivel2-Descripcion",cont_finalizar,final)  
        #reiniciamos variable
        cont_finalizar=0

        #Si hemos leido la descripcción de la Enfermedad de nivel 2
        if en2_descripcion != "":
            #aumentamos el contador de enfermedad nivel 2
            cont_enfnv2+=1
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Enfermedad-Nivel2> <Descripcion> en2_descripcion </Descripcion>
            variables_des_enfnv2,nom_var_des_en2,en2_descripcion,cont_enfnv2 = fundiccionario.asignar_especificacion_consubtitulo(variables_enfnv2[non_var_enf_nv2],variables_des_enfnv2,en2_descripcion,cont_enfnv2,"Descripcion","Enfermedad-Nivel2")

            #reiniciamos variable
            en2_descripcion=""
        # activamos variable de que ya estamos em nivel 2
        control_nv2=1  
    
    #Si lo siquiente que leemos es Enfermedad actualizada de nivel 2
    if "Enfermedad_nivel2-actualizacion" in siguiente['class']:
        #aumentamos el contador de enfermedad de nivel 2
        cont_enfnv2+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Enfermedad-Nivel2>
        cont_enfnv2,non_var_enf_nv2,variables_enfnv2,cod_nivel2,variables_enfnv1[non_var_enf_nv1] = fundiccionario.asignar_elemento_nivel(cont_enfnv2,variables_enfnv2,"Enfermedad-Nivel2",cod_nivel2,2,siguiente,variables_enfnv1[non_var_enf_nv1])

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Enfermedad-Nivel2 Actualizado="cierto" Codigo=cod_nivel[0]> siguiente.text   
        siguiente,variables_enfnv2,non_var_enf_nv2,control_nv = fundiccionario.asignar_codigo(siguiente, non_var_enf_nv2, variables_enfnv2,control_nv2,cod_nivel2,actualizado)
    
        #Si lo siquiente que leemos es la descripccion de Enfermedad de nivel 1
        while "Enfermedad_nivel2-actualizacion-Descripcion" in siguiente['class'] or "Enfermedad_nivel2-Descripcion" in siguiente['class']: 
            en2_descripcion+=siguiente.text #añadimos contenido del texto a la descripcion de enfermedad del nivel 2
            siguiente = siguiente.find_next() #seguimos pasando al siguiente proximo
            # si estamos en parte que pertenece al Pie de página
            while "Pie-de-pagina" in siguiente['class']:
                siguiente = siguiente.find_next() #seguimos pasando al siguiente proximo
           
        if en2_descripcion != "":
             #aumentamos el contador de enfermedades de nivel 2
            cont_enfnv2+=1

             #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel0> <Enfermedad-Nivel2 Actualizado="cierto> <Descripcion> en2_descripcion </Descripcion>
            variables_des_enfnv2,nom_var_des_en2,en2_descripcion,cont_enfnv2 = fundiccionario.asignar_especificacion_consubtitulo(variables_enfnv2[non_var_enf_nv2],variables_des_enfnv2,en2_descripcion,cont_enfnv2,"Descripcion","Enfermedad-Nivel2")

            #reiniciamos variable
            en2_descripcion=""
        # activamos variable de que ya estamos em nivel 2   
        control_nv2=1

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-ENFERMEDADNIVEL2-NOTA
    ############################################################################################################################################################## 
    siguiente,nota_actual=fundiccionario.leer_token(siguiente,"Nota")
    #Si hemos leido la nota de la enfermedad de nivel 2
    if nota_actual != "":
        #aumentamos el contador de notas de enfermedades de nivel 2
        cont_enfn2_notas+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Enfermedad-Nivel2> <Nota>
        variables_enfn2_notas,nom_var_enfn2_notas,nota_actual,cont_enfn2_notas =  fundiccionario.asignar_especificacion(variables_enfnv2[non_var_enf_nv2],variables_enfn2_notas,nota_actual,cont_enfn2_notas,"Nota") 
           
        #reiniciamos variable
        nota_actual = ""


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-ENFERMEDADNIVEL2-EXTENSION_CARACTER
    ############################################################################################################################################################## 
    siguiente,exten_actual=fundiccionario.leer_tokencondescripcion(siguiente,"extension-caracter")
    #Si hemos leido la nota de la enfermedad de nivel 2    
    if exten_actual != "":                
        #aumentamos el contador de extensiones de caracter de enfermedades de nivel 2
        cont_enfn2_extcar+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">  <Seccion>  <Seccion> <Enfermedad-Nivel0> <Enfermedad-Nivel1> <Enfermedad-Nivel2> <Extension-Caracter> exten_actual </Extension-Caracter>
        variables_enfn2_ext_car,nom_var_enfn2_extcar,exten_actual,cont_enfn2_extcar = fundiccionario.asignar_especificacion(variables_enfnv2[non_var_enf_nv2],variables_enfn2_ext_car,exten_actual,cont_enfn2_extcar,"Extension-Caracter")
        
        #reiniciamos variable
        exten_actual = ""

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-ENFERMEDADNIVEL2-INCLUYE
    ############################################################################################################################################################## 
  
    siguiente,incluye_actual=fundiccionario.leer_token(siguiente,"Incluye")
    #Si hemos leido el incluye de la emfermedad de nivel 2 
    if incluye_actual != "" and control_nv2==1:
        #aumentamos el contador de incluyes de enfermedades de nivel 2                
        cont_incluyes_enf2+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Incluye>
        variables_enfnv2[non_var_enf_nv2],variables_incluyes_enf2,nom_var_inc_enf2 = fundiccionario.asignar(variables_enfnv2[non_var_enf_nv2],variables_incluyes_enf2,cont_incluyes_enf2,"Incluye")
        
        #buscamos referencias en el incluye     
        lista_ref_enfermedad=manager.buscar_referencias(incluye_actual) 
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">  <Seccion>  <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Incluye>  <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad> 
            variables_incluyes_ref,variables_incluyes_enf2,cont_ref_incluyes_enf2 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_incluyes_ref,cont_ref_incluyes_enf1,variables_incluyes_enf2,nom_var_inc_enf2,"enfermedad","Referencia")

        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"><Seccion>  <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> incluye_actual
            variables_incluyes_enf2[nom_var_inc_enf2].text=incluye_actual  
        # reiniciamos variable
        control_nv2=0
    # reiniciamos variables   
    incluye_actual="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
    


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-ENFERMEDADNIVEL2-EXCLUYE
    ############################################################################################################################################################## 


    siguiente,excluye_actual=fundiccionario.leer_token(siguiente,"Excluye")
    #Si hemos leido la Excluye del capítulo 
    if excluye_actual != "" and control_nv2==1:
        #aumentamos el contador de Excluye de enfermedades de nivel 2
        cont_excluyes_enf2+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Excluye> 
        variables_enfnv2[non_var_enf_nv2],variables_excluyes_enf2,nom_var_exc_enf2 = fundiccionario.asignar(variables_enfnv2[non_var_enf_nv2],variables_excluyes_enf2,cont_excluyes_enf2,"Excluye")
        

        #buscamos referencias en el excluye
        lista_ref_enfermedad=manager.buscar_referencias(excluye_actual)
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:    
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Excluye> <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad> 
            variables_excluyes_enf2_ref,variables_excluyes_enf2,cont_ref_excluyes_enf2 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_excluyes_enf2_ref,cont_ref_excluyes_enf2,variables_excluyes_enf2,nom_var_exc_enf2,"enfermedad","Referencia")
            # lista_referencia,subelemento,contador_subelemento,elemento,non_referencia_elem,titulo,subtitulo
        else:   
            #aumentamos el contador de Utilice codigo adicional de enfermedades de nivel 1
            cont_excluyes_enf2+=1
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Excluye> excluye_actual
            variables_excluyes_enf2,nom_var_exc_enf2,excluye_actual,cont_excluyes_enf2 = fundiccionario.asignar_especificacion(variables_enfnv2[non_var_enf_nv2],variables_excluyes_enf2,excluye_actual,cont_excluyes_enf2,"Excluye")

        # reiniciamos variable
        control_nv2=0
    # reiniciamos variables    
    excluye_actual=""
    lista_ref_enfermedad.clear()


    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-ENFERMEDADNIVEL2-EXCLUYE2
    ############################################################################################################################################################## 

   

    siguiente,excluye2_actual=fundiccionario.leer_token(siguiente,"Excluye2")
    #Si hemos leido la Excluye2 de la Enfermedad de nivel 2
    if excluye2_actual != "" and control_nv2==1:

        cont_excluyes2_enf2+=1

        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Excluye2> 
        variables_enfnv2[non_var_enf_nv2],variables_excluyes2_enf2,nom_var_exc2_enf2 = fundiccionario.asignar(variables_enfnv2[non_var_enf_nv2],variables_excluyes2_enf2,cont_excluyes2_enf2,"Excluye2")
        
        #buscamos referencias en el excluye
        lista_ref_enfermedad=manager.buscar_referencias(excluye2_actual) 
        if len(lista_ref_enfermedad)!= 0:    #si encontramos alguna referencia
                
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Excluye2> <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad>
            variables_excluyes2_enf2_ref,variables_excluyes2_enf2,cont_ref_excluyes2_enf2 =fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_excluyes2_enf2_ref,cont_ref_excluyes2_enf2,variables_excluyes2_enf2,nom_var_exc2_enf2,"enfermedad","Referencia")
                        
        else:   
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Excluye2> excluye2_actual   
            variables_excluyes2_enf2[nom_var_exc2_enf2].text=excluye2_actual
        # reiniciamos variable    
        control_nv2=0
    # reiniciamos variables
    excluye2_actual=""
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades

    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-ENFERMEDADNIVEL2-CODIFIQUE_PRIMERO
    ############################################################################################################################################################## 

    siguiente,codifique_primero=fundiccionario.leer_tokencondescripcion(siguiente,"Codifique-primero")
    #Si hemos leido el codifique primero de la enfermedad de nivel 2
    if codifique_primero != "" and control_nv2 == 1:
        # aumentamos el contador de codifique primero de enfermedades de nivel 2
        cont_codifique_enf2+=1
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Codifique-primero>
        variables_enfnv2[non_var_enf_nv2],variables_codifique_enf2,nom_var_codpri_enf2 = fundiccionario.asignar(variables_enfnv2[non_var_enf_nv2],variables_codifique_enf2,cont_codifique_enf2,"Codifique_Primero")
        
        #buscamos referencias en el codifique primero de la enfermedad de nivel 2
        lista_ref_enfermedad=manager.buscar_referencias(codifique_primero)
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual">  <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Codifique_Primero> <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad>    
            variables_codifique_ref2,variables_codifique_enf2,cont_ref_codpri_enf2 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_codifique_ref2,cont_ref_codpri_enf2,variables_codifique_enf2,nom_var_codpri_enf2,"enfermedad","Referencia")

        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <EnfernedadNivel2> <Codifique_Primero> codifique_primero
            variables_codifique_enf2[nom_var_codpri_enf2].text=codifique_primero
        # reiniciamos variable
        control_nv2=0
    # reiniciamos variables
    codifique_primero="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
    
    ##############################################################################################################################################################
    #   CAPITULO-SECCION-ENFERMEDADNIVEL0-ENFERMEDADNIVEL1-ENFERMEDADNIVEL2-UTILICE_CODIGO_ADICIONAL
    ############################################################################################################################################################## 
    siguiente,cofifique_cod_adicional=fundiccionario.leer_tokencondescripcion(siguiente,"Utilice-codigo-adicional")
    #Si hemos leido el Utilice codigo adicional de la Enfermedad de nivel 2
    if cofifique_cod_adicional != "" and control_nv2 == 1:
        #Si hemos leido el Utilice codigo adicional de la Enfermedad de nivel 2
        cont_codifique_adiccional_enf2+=1
        
        #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1>  <EnfernedadNivel2> <Utilice-codigo-adicional>
        variables_enfnv2[non_var_enf_nv2],variables_codifique_adiccional_enf2,nom_var_codadicional_enf2 = fundiccionario.asignar(variables_enfnv2[non_var_enf_nv2],variables_codifique_adiccional_enf2,cont_codifique_adiccional_enf2,"Utilice_Codigo_adicional")
         
        #buscamos referencias en el incluye
        lista_ref_enfermedad=manager.buscar_referencias(cofifique_cod_adicional)
        #si encontramos alguna referencia
        if len(lista_ref_enfermedad)!= 0:   
            
            #Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Seccion> <EnfernedadNivel0> <EnfernedadNivel1> <Codifique_Primero> <Referencia_enfermedad Referencia="ref_enfermedad[1]"> ref_enfermedad[0] ref_enfermedad[1]</Ref_enfermedad> 
            variables_codifiqueadi_ref2,variables_codifique_adiccional_enf2,cont_ref_codadi_enf2 = fundiccionario.asignar_lista_referencia(lista_ref_enfermedad,variables_codifiqueadi_ref2,cont_ref_codadi_enf2,variables_codifique_adiccional_enf2,nom_var_codadicional_enf2,"enfermedad","Referencia")
            
        else:
            # Asignamos en el diccionario <cie10> <capitulo Titulo="capitulo_actual"> <Codifique_Primero> codifique_primero
            variables_codifique_adiccional_enf2[nom_var_codadicional_enf2].text=cofifique_cod_adicional  
        # reiniciamos variable
        control_nv2=0
    # reiniciamos variables
    cofifique_cod_adicional="" 
    lista_ref_enfermedad.clear() #limpiamos la lista de referencias de enfermedades
    #siguiente = siguiente.find_next()  

    while "Indice-Secciones" in siguiente['class']:
        siguiente = siguiente.find_next()
    while "Pie-de-pagina" in siguiente['class']:
        siguiente = siguiente.find_next()
    while "caracter" in siguiente['class']:
        siguiente = siguiente.find_next()
    
    if str(siguiente) == str(nuevo_siguiente):
        siguiente= siguiente.find_next()
        if(utltimo_siguiente>0 and str(siguiente) == str(nuevo_siguiente)):
            print(siguiente)
            print(nuevo_siguiente)
            break
        else:
            utltimo_siguiente=0
        if str(siguiente) == str(nuevo_siguiente):
            siguiente= siguiente.find_next()
            utltimo_siguiente+=1

                
    nuevo_siguiente=siguiente
        
# Creación del arbol 
tree=diccionario.ElementTree(raiz)

# Escribimos arbol en formato xml en el archivo diccionario.xml
tree.write("diccionario.xml", encoding="utf-8")

# Asignamos el tiempo final
end_time = time.time()

# Imprimimos tiempo que ha tardado
print(f"Tiempo de ejecución: {end_time - start_time} segundos")



