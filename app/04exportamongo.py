import xml.etree.ElementTree as diccinario
from pymongo import MongoClient
from cie10 import manager
from config import MONGODB_URL, DATABASE_NAME,PUERTO
import time
import os

# Asignamos el tiempo de inicio        
start_time = time.time()


# print(MONGODB_URL)
# print(PUERTO)
# Conexión a la base de datos de MongoDB
client = MongoClient(MONGODB_URL, PUERTO)
db = client[DATABASE_NAME]

collection_secciones = db['SECCION']  # SECCION(ID,Nombre,Aclaracion) ✅ 
collection_enfermedades = db['ENFERMEDAD']  #  ENFERMEDAD(Codigo,Nombre, Aclaracion) ✅ 

collection_enfermedad_excluye = db['ENFERMEDAD_EXCLUYE'] #  ENFERMEDAD_EXCLUYE(ID,tipo,DESCRIPCION) ✅

collection_enfermedad_excluye_enfermedad = db['ENFERMEDAD_EXCLUYE_ENFERMEDAD'] # ENFERMEDAD_REFERENCIA_ENFERMEDAD(ID_excluye,Codigo_Enfermedad,CodRef_Enfermedad) ✅
collection_enfermedad_excluye_seccion = db['ENFERMEDAD_EXCLUYE_SECCION'] # ENFERMEDAD_REFERENCIA_SECCION(ID_excluye,Codigo_Enfermedad,ID_Seccion)  ✅



# Ruta al archivo XML
xml_file = 'diccionario.xml'

# Parsear el archivo XML
tree = diccinario.parse(xml_file)
root = tree.getroot()

# Variables temporales para sección 
id_seccion=0
nombre_seccion=''
aclaracion_seccion=''

# Variables temporales para incluyes y excluyes 
id_excluye_enf=0
id_excluye_sec=0
descripcion_enf_excluye=''

# Variables temporales para decir de que tipo es
tipo1=1
tipo2=2

# Variables temporales para enfermedad de nivel 0 
codigo_enfermedadn0=''
nombre_enfermedadn0=''
aclaracion_enfermedadn0=''
descripcion_enfermedadn0=''

# Variables temporales para enfermedad de nivel 1
codigo_enfermedadn1=''
nombre_enfermedadn1=''
aclaracion_enfermedadn1=''
descripcion_enfermedadn1=''

# Variables temporales para enfermedad de nivel 2
codigo_enfermedadn2=''
nombre_enfermedadn2=''
aclaracion_enfermedadn2=''
descripcion_enfermedadn2=''



# Por cada uno de los elementos del XML, guardarmos en MongoDB
for capitulo_elem in root.findall('capitulo'):
    # ################################################################################
    #                   CAPITULO
    # ################################################################################
       
    # ################################################################################
    #                   CAPITULO-SECCION
    # ################################################################################             
    for seccion_elem in capitulo_elem.findall('Seccion'):
        
        # ID_Seccion nuevo (ID_SECCION)
        id_seccion+=1
        #Leemos el título del capítulo (NOMBRE)
        nombre_seccion=seccion_elem.get('Titulo')
        #Leemos toda la descripcion de la seccion (ACLARACIÓN)
        if seccion_elem.text is not None:
            aclaracion_seccion +=seccion_elem.text      
        for descripcion_elem in seccion_elem.findall('Seccion-Descripcion'):
            aclaracion_seccion += descripcion_elem.find('Seccion-Descripcion').text
        
        #Leemos toda la Nota de la sección (ACLARACIÓN)
        for nota_elem in seccion_elem.findall('Nota'):
            aclaracion_seccion += nota_elem.text

        # Formateamos la inserción SECCION(ID,Nombre,Aclaracion)
        data_seccion={
            'ID': id_seccion,
            'Nombre': nombre_seccion,
            'Aclaracion': aclaracion_seccion
        }
        # Insertamos en MONGODB en db['SECCION'] 
        collection_secciones.insert_one(data_seccion)
               
        # ################################################################################
        #                   CAPITULO-SECCION-ENFERMEDAD_NIVEL0
        # ################################################################################   
        
        # ENFERMEDAD(Codigo,Nombre, Aclaracion)
        for enfermedadn0_elem in seccion_elem.findall('Enfermedad-Nivel0'):
            
            # Codigo de Enfermedad (Codigo)
            codigo_enfermedadn0 = enfermedadn0_elem.get('Codigo')
            if codigo_enfermedadn0 is not None:
                # (NOMBRE)
                nombre_enfermedadn0 +=str(enfermedadn0_elem.text)

                #Leemos toda la descripcion de Enfermedad (ACLARACIÓN)
                for descripcion_elem in enfermedadn0_elem.findall('Descripcion'):
                    if descripcion_elem.find('Descripcion') is not None:
                        aclaracion_enfermedadn0 += descripcion_elem.find('Descripcion').text

                #Leemos toda la Nota de la enfermedad (ACLARACIÓN)
                for nota_elem in enfermedadn0_elem.findall('Nota'):
                    if nota_elem.text is not None:
                        aclaracion_enfermedadn0 += nota_elem.text

                #Leemos todas las todos los Codifique_Primero (ACLARACIÓN)
                for codifique_elem in enfermedadn0_elem.findall('Codifique_Primero'):
                    if codifique_elem.find('Codifique_Primero') is not None:
                        aclaracion_enfermedadn0 += codifique_elem.find('Codifique_Primero').text
                    #Leemos todas las todas las Referencias  (ACLARACIÓN)
                    for referencias in codifique_elem.findall('Referencia_enfermedad'):
                        if referencias.find('Referencia_enfermedad') is not None:
                            aclaracion_enfermedadn0 += referencias.find('Referencia_enfermedad').text

                #Leemos todas las todos los Utilice_Codigo_adicional (ACLARACIÓN)
                for codadicional_elem in enfermedadn0_elem.findall('Utilice_Codigo_adicional'):
                    if codadicional_elem.find('Utilice_Codigo_adicional') is not None:
                        aclaracion_enfermedadn0 += codadicional_elem.find('Utilice_Codigo_adicional').text
                    #Leemos todas las todas las Referencias (ACLARACIÓN)
                    for referencias in codadicional_elem.findall('Referencia_enfermedad'):
                        if referencias.find('Referencia_enfermedad') is not None:
                            aclaracion_enfermedadn0 += referencias.find('Referencia_enfermedad').text

                for incluye_elem in enfermedadn0_elem.findall('Incluye'):
                    #Leemos toda la descripcion del incluye (DESCRIPCIION)
                    if incluye_elem.text is not None:
                        aclaracion_enfermedadn0+=  str(incluye_elem.text)

                    for descripcion_elem in incluye_elem.findall('Descripcion'):
                        if descripcion_elem.text is not None:
                            aclaracion_enfermedadn0+=  descripcion_elem.text
                            if descripcion_elem.find('Descripcion').text is not None:
                                aclaracion_enfermedadn0+= descripcion_elem.find('Descripcion').text

                # Formateamos la inserción ENFERMEDAD(Codigo,Nombre, Aclaracion)
                data_enfermedad_nivel0={
                    'Codigo':codigo_enfermedadn0,
                    'Nombre':nombre_enfermedadn0, 
                    'Aclaracion':aclaracion_enfermedadn0
                }
                # Insertamos en db['ENFERMEDAD']
                collection_enfermedades.insert_one(data_enfermedad_nivel0)
                # reiniciamos variable
                nombre_enfermedadn0=""
                aclaracion_enfermedadn0=""
                
                # --------------------------------------------------------
                # ENFERMEDAD_NIVEL0-EXCLUYE
                # --------------------------------------------------------
                #Leemos todos los Excluye
                for excluye_elem in enfermedadn0_elem.findall('Excluye'):
                    # ID_excluye nuevo  (ID_EXCLUYE)
                    id_excluye_enf+=1
                    #Leemos toda la descripcion del Excluye (ACLARACIÓN)
                    for descripcion_elem in excluye_elem.findall('Descripcion'):
                        descripcion_enf_excluye+= descripcion_elem.find('Descripcion').text
                    # Formateamos la inserción ENFERMEDAD_EXCLUYE(ID,tipo,DESCRIPCION)
                    data_enf_excluye={
                        'ID':id_excluye_enf,
                        'tipo ':tipo1, 
                        'DESCRIPCION':descripcion_enf_excluye 
                    }
                    #Insertamos en MONGODB en db['ENFERMEDAD_EXCLUYE'] 
                    collection_enfermedad_excluye.insert_one(data_enf_excluye)

                    for referencias_enfermedad in excluye_elem.findall('Referencia_enfermedad'):
                        # Leemos la referencia del Excluye (Codigo_Enfermedad)
                        codigo_ref_enfermedad = referencias_enfermedad.get('Referencia')
                        # Comprobamos si la referencia es de una Enfermedad o una Seccion
                        tiporeferencia=manager.tipo_referencia(codigo_ref_enfermedad)
                        if tiporeferencia==1:
                            # Formateamos la inserción ENFERMEDAD_REFERENCIA_ENFERMEDAD(ID_excluye,Codigo_Enfermedad,CodRef_Enfermedad)
                            data_enf_excluye_enfermedad={
                                'ID_excluye':id_excluye_enf,
                                'Codigo_Enfermedad':codigo_enfermedadn0,
                                'CodRef_Enfermedad':codigo_ref_enfermedad
                            }
                            #Insertamos en MONGODB en db['ENFERMEDAD_REFERENCIA_ENFERMEDAD']
                            collection_enfermedad_excluye_enfermedad.insert_one(data_enf_excluye_enfermedad)        
                        if tiporeferencia==2:
                            # Formateamos la inserción  ENFERMEDAD_REFERENCIA_SECCION(ID_excluye,Codigo_Enfermedad,ID_Seccion)
                            data_enf_excluye_seccion={
                                'ID_excluye':id_excluye_enf,
                                'Codigo_Enfermedad':codigo_enfermedadn0, 
                                'ID_Seccion':codigo_ref_enfermedad
                            }
                            #Insertamos en MONGODB
                            collection_enfermedad_excluye_seccion.insert_one(data_enf_excluye_seccion)
                        # reiniciamos variable
                        descripcion_enf_excluye=""

                # --------------------------------------------------------
                # ENFERMEDAD_NIVEL0-EXCLUYE2
                # --------------------------------------------------------
                #Leemos todos los Excluye
                for excluye_elem in enfermedadn0_elem.findall('Excluye2'):
                    # ID_excluye nuevo  (ID_EXCLUYE)
                    id_excluye_enf+=1
                    #Leemos toda la descripcion del Excluye (ACLARACIÓN)
                    for descripcion_elem in excluye_elem.findall('Descripcion'):
                        descripcion_enf_excluye+= descripcion_elem.find('Descripcion').text
                    # Formateamos la inserción ENFERMEDAD_EXCLUYE(ID,tipo,DESCRIPCION)
                    data_enf_excluye={
                        'ID':id_excluye_enf,
                        'tipo ':tipo2, 
                        'DESCRIPCION':descripcion_enf_excluye 
                    }
                    #Insertamos en MONGODB en db['ENFERMEDAD_EXCLUYE'] 
                    collection_enfermedad_excluye.insert_one(data_enf_excluye)     

                    for referencias_enfermedad in excluye_elem.findall('Referencia_enfermedad'):
                        # Leemos la referencia del Excluye (Codigo_Enfermedad)
                        codigo_ref_enfermedad = referencias_enfermedad.get('Referencia')
                        # Comprobamos si la referencia es de una Enfermedad o una Seccion
                        tiporeferencia=manager.tipo_referencia(codigo_ref_enfermedad)
                        if tiporeferencia==1:
                            # Formateamos la inserción ENFERMEDAD_REFERENCIA_ENFERMEDAD(ID_excluye,Codigo_Enfermedad,CodRef_Enfermedad)
                            data_enf_excluye_enfermedad={
                                'ID_excluye':id_excluye_enf,
                                'Codigo_Enfermedad':codigo_enfermedadn0,
                                'CodRef_Enfermedad':codigo_ref_enfermedad 
                            }
                            #Insertamos en MONGODB en db['ENFERMEDAD_REFERENCIA_ENFERMEDAD']
                            collection_enfermedad_excluye_enfermedad.insert_one(data_enf_excluye_enfermedad)        
                        if tiporeferencia==2:
                            # Formateamos la inserción  ENFERMEDAD_REFERENCIA_SECCION(ID_excluye,Codigo_Enfermedad,ID_Seccion)
                            data_enf_excluye_seccion={
                                'ID_excluye':id_excluye_enf,
                                'Codigo_Enfermedad':codigo_enfermedadn0, 
                                'ID_Seccion':codigo_ref_enfermedad  
                            }
                            # print(codigo_ref_enfermedad)
                            #Insertamos en MONGODB
                            collection_enfermedad_excluye_seccion.insert_one(data_enf_excluye_seccion)
                        # reiniciamos variable
                        descripcion_enf_excluye=""
                
                
                # ################################################################################
                #                   CAPITULO-SECCION-ENFERMEDAD_NIVEL0-ENFERMEDAD_NIVEL1
                # ################################################################################   
                
                # ENFERMEDAD(Codigo,Nombre, Aclaracion)
                for enfermedadn1_elem in enfermedadn0_elem.findall('Enfermedad-Nivel1'):
                    # Codigo de Enfermedad (Codigo)
                    codigo_enfermedadn1 = enfermedadn1_elem.get('Codigo')
                    # (NOMBRE)
                    if codigo_enfermedadn1 is not None:
                        nombre_enfermedadn1 +=str(enfermedadn1_elem.text)

                        #Leemos toda la descripcion de Enfermedad (ACLARACIÓN)
                        for descripcion_elem in enfermedadn1_elem.findall('Descripcion'):
                            if descripcion_elem.text is not None:
                                aclaracion_enfermedadn1 += descripcion_elem.text

                        #Leemos toda la Nota de la enfermedad (ACLARACIÓN)
                        for nota_elem in enfermedadn1_elem.findall('Nota'):
                            if nota_elem.text is not None:
                                aclaracion_enfermedadn1 += nota_elem.text


                        #Leemos todas las todos los Codifique_Primero (ACLARACIÓN)
                        for codifique_elem in enfermedadn1_elem.findall('Codifique_Primero'):
                            if codifique_elem.find('Codifique_Primero') is not None:
                                aclaracion_enfermedadn1 += codifique_elem.find('Codifique_Primero').text
                            #Leemos todas las todas las Referencias  (ACLARACIÓN)
                            for referencias in codifique_elem.findall('Referencia_enfermedad'):
                                if referencias.find('Referencia_enfermedad') is not None:
                                    aclaracion_enfermedadn1 += referencias.find('Referencia_enfermedad').text

                        #Leemos todas las todos los Utilice_Codigo_adicional (ACLARACIÓN)
                        for codadicional_elem in enfermedadn1_elem.findall('Utilice_Codigo_adicional'):
                            if codadicional_elem.find('Utilice_Codigo_adicional') is not None:
                                aclaracion_enfermedadn1 += codadicional_elem.find('Utilice_Codigo_adicional').text
                            #Leemos todas las todas las Referencias (ACLARACIÓN)
                            for referencias in codadicional_elem.findall('Referencia_enfermedad'):
                                if referencias.find('Referencia_enfermedad') is not None:
                                    aclaracion_enfermedadn1 += referencias.find('Referencia_enfermedad').text

                        for incluye_elem in enfermedadn1_elem.findall('Incluye'):
                            aclaracion_enfermedadn1+=  incluye_elem.text

                            for descripcion_elem in incluye_elem.findall('Descripcion'):
                                aclaracion_enfermedadn1+=  descripcion_elem.text

                        # Formateamos la inserción ENFERMEDAD(Codigo,Nombre, Aclaracion)
                        data_enfermedad_nivel1={
                            'Codigo':codigo_enfermedadn1,
                            'Nombre':nombre_enfermedadn1, 
                            'Aclaracion':aclaracion_enfermedadn1
                        }
                        # Insertamos en db['ENFERMEDAD']
                        collection_enfermedades.insert_one(data_enfermedad_nivel1)
                        # reiniciamos variable
                        nombre_enfermedadn1=""
                        aclaracion_enfermedadn1=""
                        
                        # --------------------------------------------------------
                        # ENFERMEDAD_NIVEL1-EXCLUYE
                        # --------------------------------------------------------
                        #Leemos todos los Excluye
                        for excluye_elem in enfermedadn1_elem.findall('Excluye'):
                            # ID_excluye nuevo  (ID_EXCLUYE)
                            id_excluye_enf+=1
                            #Leemos toda la descripcion del Excluye (ACLARACIÓN)
                            for descripcion_elem in excluye_elem.findall('Descripcion'):
                                descripcion_enf_excluye+= descripcion_elem.find('Descripcion').text
                            # Formateamos la inserción ENFERMEDAD_EXCLUYE(ID,tipo,DESCRIPCION)
                            data_enf_excluye={
                                'ID':id_excluye_enf,
                                'tipo ':tipo1, 
                                'DESCRIPCION':descripcion_enf_excluye 
                            }
                            #Insertamos en MONGODB en db['ENFERMEDAD_EXCLUYE'] 
                            collection_enfermedad_excluye.insert_one(data_enf_excluye)     

                            for referencias_enfermedad in excluye_elem.findall('Referencia_enfermedad'):
                                # Leemos la referencia del Excluye (Codigo_Enfermedad)
                                codigo_ref_enfermedad = referencias_enfermedad.get('Referencia')
                                # Comprobamos si la referencia es de una Enfermedad o una Seccion
                                tiporeferencia=manager.tipo_referencia(codigo_ref_enfermedad)
                                if tiporeferencia==1:
                                    # Formateamos la inserción ENFERMEDAD_REFERENCIA_ENFERMEDAD(ID_excluye,Codigo_Enfermedad,CodRef_Enfermedad)
                                    data_enf_excluye_enfermedad={
                                        'ID_excluye':id_excluye_enf,
                                        'Codigo_Enfermedad':codigo_enfermedadn1,
                                        'CodRef_Enfermedad':codigo_ref_enfermedad
                                    }
                                    #Insertamos en MONGODB en db['ENFERMEDAD_REFERENCIA_ENFERMEDAD']
                                    collection_enfermedad_excluye_enfermedad.insert_one(data_enf_excluye_enfermedad)        
                                if tiporeferencia==2:
                                    # Formateamos la inserción  ENFERMEDAD_REFERENCIA_SECCION(ID_excluye,Codigo_Enfermedad,ID_Seccion)
                                    data_enf_excluye_seccion={
                                        'ID_excluye':id_excluye_enf,
                                        'Codigo_Enfermedad':codigo_enfermedadn1, 
                                        'ID_Seccion':codigo_ref_enfermedad  
                                    }
                                    # print(codigo_ref_enfermedad)
                                    #Insertamos en MONGODB
                                    collection_enfermedad_excluye_seccion.insert_one(data_enf_excluye_seccion)
                                # reiniciamos variable
                                descripcion_enf_excluye=""

                        # --------------------------------------------------------
                        # ENFERMEDAD_NIVEL1-EXCLUYE2
                        # --------------------------------------------------------
                        #Leemos todos los Excluye
                        for excluye_elem in enfermedadn1_elem.findall('Excluye2'):
                            # ID_excluye nuevo  (ID_EXCLUYE)
                            id_excluye_enf+=1
                            #Leemos toda la descripcion del Excluye (ACLARACIÓN)
                            for descripcion_elem in excluye_elem.findall('Descripcion'):
                                descripcion_enf_excluye+= descripcion_elem.find('Descripcion').text
                            # Formateamos la inserción ENFERMEDAD_EXCLUYE(ID,tipo,DESCRIPCION)
                            data_enf_excluye={
                                'ID':id_excluye_enf,
                                'tipo ':tipo2, 
                                'DESCRIPCION':descripcion_enf_excluye 
                            }
                            #Insertamos en MONGODB en db['ENFERMEDAD_EXCLUYE'] 
                            collection_enfermedad_excluye.insert_one(data_enf_excluye)     

                            for referencias_enfermedad in excluye_elem.findall('Referencia_enfermedad'):
                                # Leemos la referencia del Excluye (Codigo_Enfermedad)
                                codigo_ref_enfermedad = referencias_enfermedad.get('Referencia')
                                # Comprobamos si la referencia es de una Enfermedad o una Seccion
                                tiporeferencia=manager.tipo_referencia(codigo_ref_enfermedad)
                                if tiporeferencia==1:
                                    # Formateamos la inserción ENFERMEDAD_REFERENCIA_ENFERMEDAD(ID_excluye,Codigo_Enfermedad,CodRef_Enfermedad)
                                    data_enf_excluye_enfermedad={
                                        'ID_excluye':id_excluye_enf,
                                        'Codigo_Enfermedad':codigo_enfermedadn1,
                                        'CodRef_Enfermedad':codigo_ref_enfermedad
                                    }
                                    #Insertamos en MONGODB en db['ENFERMEDAD_REFERENCIA_ENFERMEDAD']
                                    collection_enfermedad_excluye_enfermedad.insert_one(data_enf_excluye_enfermedad)        
                                if tiporeferencia==2:
                                    # Formateamos la inserción  ENFERMEDAD_REFERENCIA_SECCION(ID_excluye,Codigo_Enfermedad,ID_Seccion)
                                    data_enf_excluye_seccion={
                                        'ID_excluye':id_excluye_enf,
                                        'Codigo_Enfermedad':codigo_enfermedadn1, 
                                        'ID_Seccion':codigo_ref_enfermedad  
                                    }
                                    # print(codigo_ref_enfermedad)
                                    #Insertamos en MONGODB
                                    collection_enfermedad_excluye_seccion.insert_one(data_enf_excluye_seccion)
                                # reiniciamos variable
                                descripcion_enf_excluye=""

                        

                        # ################################################################################
                        #     CAPITULO-SECCION-ENFERMEDAD_NIVEL0-ENFERMEDAD_NIVEL1-ENFERMEDAD_NIVEL2
                        # ################################################################################     
                        # ENFERMEDAD(Codigo,Nombre, Aclaracion)
                        for enfermedadn2_elem in enfermedadn1_elem.findall('Enfermedad-Nivel2'):
                            # Codigo de Enfermedad (Codigo)
                            codigo_enfermedadn2 = enfermedadn2_elem.get('Codigo')
                            # (NOMBRE)
                            if codigo_enfermedadn2 is not None:
                                nombre_enfermedadn2 +=str(enfermedadn2_elem.text)

                                #Leemos toda la descripcion de Enfermedad (ACLARACIÓN)
                                for descripcion_elem in enfermedadn2_elem.findall('Descripcion'):
                                    if descripcion_elem.find('Descripcion') is not None:
                                        aclaracion_enfermedadn2 += descripcion_elem.find('Descripcion').text

                                #Leemos toda la Nota de la enfermedad (ACLARACIÓN)
                                for nota_elem in enfermedadn2_elem.findall('Nota'):
                                    aclaracion_enfermedadn2 += nota_elem.text

                                #Leemos todas las todos los Codifique_Primero (ACLARACIÓN)
                                for codifique_elem in enfermedadn2_elem.findall('Codifique_Primero'):
                                    if codifique_elem.find('Codifique_Primero') is not None:
                                        aclaracion_enfermedadn2 += codifique_elem.find('Codifique_Primero').text
                                    #Leemos todas las todas las Referencias  (ACLARACIÓN)
                                    for referencias in codifique_elem.findall('Referencia_enfermedad'):
                                        if referencias.find('Referencia_enfermedad') is not None:    
                                            aclaracion_enfermedadn2 += referencias.find('Referencia_enfermedad').text

                                #Leemos todas las todos los Utilice_Codigo_adicional (ACLARACIÓN)
                                for codadicional_elem in enfermedadn2_elem.findall('Utilice_Codigo_adicional'):
                                    aclaracion_enfermedadn2 += codadicional_elem.find('Utilice_Codigo_adicional').text
                                    #Leemos todas las todas las Referencias (ACLARACIÓN)
                                    for referencias in codadicional_elem.findall('Referencia_enfermedad'):
                                            aclaracion_enfermedadn2 += referencias.find('Referencia_enfermedad').text
                                
                                for incluye_elem in enfermedadn2_elem.findall('Incluye'):
                                    #Leemos toda la descripcion del incluye (DESCRIPCIION)
                                    if incluye_elem.text is not None:
                                        aclaracion_enfermedadn2+= str(incluye_elem.text)

                                    for descripcion_elem in incluye_elem.findall('Descripcion'):
                                        aclaracion_enfermedadn2+=  descripcion_elem.text
                                        aclaracion_enfermedadn2+= descripcion_elem.find('Descripcion').text

                                # Formateamos la inserción ENFERMEDAD(Codigo,Nombre, Aclaracion)
                                data_enfermedad_nivel2={
                                    'Codigo':codigo_enfermedadn2,
                                    'Nombre':nombre_enfermedadn2, 
                                    'Aclaracion':aclaracion_enfermedadn2
                                }
                                # Insertamos en db['ENFERMEDAD']
                                collection_enfermedades.insert_one(data_enfermedad_nivel2)
                                # reiniciamos variables
                                nombre_enfermedadn2=""
                                aclaracion_enfermedadn2=""
                                
                                # --------------------------------------------------------
                                # ENFERMEDAD_NIVEL2-EXCLUYE
                                # --------------------------------------------------------
                                #Leemos todos los Excluye
                                for excluye_elem in enfermedadn2_elem.findall('Excluye'):
                                    # ID_excluye nuevo  (ID_EXCLUYE)
                                    id_excluye_enf+=1
                                    #Leemos toda la descripcion del Excluye (ACLARACIÓN)
                                    for descripcion_elem in excluye_elem.findall('Descripcion'):
                                        descripcion_enf_excluye+= descripcion_elem.find('Descripcion').text
                                    # Formateamos la inserción ENFERMEDAD_EXCLUYE(ID,tipo,DESCRIPCION)
                                    data_enf_excluye={
                                        'ID':id_excluye_enf,
                                        'tipo ':tipo1, 
                                        'DESCRIPCION':descripcion_enf_excluye 
                                    }
                                    #Insertamos en MONGODB en db['ENFERMEDAD_EXCLUYE'] 
                                    collection_enfermedad_excluye.insert_one(data_enf_excluye)     

                                    for referencias_enfermedad in excluye_elem.findall('Referencia_enfermedad'):
                                        # Leemos la referencia del Excluye (Codigo_Enfermedad)
                                        codigo_ref_enfermedad = referencias_enfermedad.get('Referencia')
                                        # Comprobamos si la referencia es de una Enfermedad o una Seccion
                                        tiporeferencia=manager.tipo_referencia(codigo_ref_enfermedad)
                                        if tiporeferencia==1:
                                            # Formateamos la inserción ENFERMEDAD_REFERENCIA_ENFERMEDAD(ID_excluye,Codigo_Enfermedad,CodRef_Enfermedad)
                                            data_enf_excluye_enfermedad={
                                                'ID_excluye':id_excluye_enf,
                                                'Codigo_Enfermedad':codigo_enfermedadn2,
                                                'CodRef_Enfermedad':codigo_ref_enfermedad
                                            }
                                            #Insertamos en MONGODB en db['ENFERMEDAD_REFERENCIA_ENFERMEDAD']
                                            collection_enfermedad_excluye_enfermedad.insert_one(data_enf_excluye_enfermedad)        
                                        if tiporeferencia==2:
                                            # Formateamos la inserción  ENFERMEDAD_REFERENCIA_SECCION(ID_excluye,Codigo_Enfermedad,ID_Seccion)
                                            data_enf_excluye_seccion={
                                                'ID_excluye':id_excluye_enf,
                                                'Codigo_Enfermedad':codigo_enfermedadn2, 
                                                'ID_Seccion':codigo_ref_enfermedad     
                                            }
                                            # print(codigo_ref_enfermedad)
                                            #Insertamos en MONGODB
                                            collection_enfermedad_excluye_seccion.insert_one(data_enf_excluye_seccion)
                                        # reiniciamos variable
                                        descripcion_enf_excluye=""

                                # --------------------------------------------------------
                                # ENFERMEDAD_NIVEL2-EXCLUYE2
                                # --------------------------------------------------------
                                #Leemos todos los Excluye
                                for excluye_elem in enfermedadn2_elem.findall('Excluye2'):
                                    # ID_excluye nuevo  (ID_EXCLUYE)
                                    id_excluye_enf+=1
                                    #Leemos toda la descripcion del Excluye (ACLARACIÓN)
                                    for descripcion_elem in excluye_elem.findall('Descripcion'):
                                        descripcion_enf_excluye+= descripcion_elem.find('Descripcion').text
                                    # Formateamos la inserción ENFERMEDAD_EXCLUYE(ID,tipo,DESCRIPCION)
                                    data_enf_excluye={
                                        'ID':id_excluye_enf,
                                        'tipo ':tipo2, 
                                        'DESCRIPCION':descripcion_enf_excluye 
                                    }
                                    #Insertamos en MONGODB en db['ENFERMEDAD_EXCLUYE'] 
                                    collection_enfermedad_excluye.insert_one(data_enf_excluye)     

                                    for referencias_enfermedad in excluye_elem.findall('Referencia_enfermedad'):
                                        # Leemos la referencia del Excluye (Codigo_Enfermedad)
                                        codigo_ref_enfermedad = referencias_enfermedad.get('Referencia')
                                        # Comprobamos si la referencia es de una Enfermedad o una Seccion
                                        tiporeferencia=manager.tipo_referencia(codigo_ref_enfermedad)
                                        if tiporeferencia==1:
                                            # Formateamos la inserción ENFERMEDAD_REFERENCIA_ENFERMEDAD(ID_excluye,Codigo_Enfermedad,CodRef_Enfermedad)
                                            data_enf_excluye_enfermedad={
                                                'ID_excluye':id_excluye_enf,
                                                'Codigo_Enfermedad':codigo_enfermedadn2,
                                                'CodRef_Enfermedad':codigo_ref_enfermedad
                                            }
                                            #Insertamos en MONGODB en db['ENFERMEDAD_REFERENCIA_ENFERMEDAD']
                                            collection_enfermedad_excluye_enfermedad.insert_one(data_enf_excluye_enfermedad)        
                                        if tiporeferencia==2:
                                            # Formateamos la inserción  ENFERMEDAD_REFERENCIA_SECCION(ID_excluye,Codigo_Enfermedad,ID_Seccion)
                                            data_enf_excluye_seccion={
                                                'ID_excluye':id_excluye_enf,
                                                'Codigo_Enfermedad':codigo_enfermedadn2, 
                                                'ID_Seccion':codigo_ref_enfermedad   
                                            }
                                            # print(codigo_ref_enfermedad)
                                            #Insertamos en MONGODB
                                            collection_enfermedad_excluye_seccion.insert_one(data_enf_excluye_seccion)
                                        # reiniciamos variable
                                        descripcion_enf_excluye=""
                    
                    
        
        #reiniciamos variables 
        nombre_seccion=''
        aclaracion_seccion=''


# Asignamos el tiempo final
end_time = time.time()

# Imprimimos tiempo que ha tardado
print(f"Tiempo de ejecución: {end_time - start_time} segundos")

















