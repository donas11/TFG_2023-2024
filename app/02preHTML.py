from cie10 import *
from cie10 import filerwpe
from cie10 import manager
from cie10 import printer
import time
import cie10

# Asignamos el tiempo de inicio
start_time = time.time()

#archivos de entrada y salida
ruta_archivo="CIE10LTP16EFN2.html" #archivo de entrada
# ruta_archivo="prueba.html"
ruta_salida1="CIE10LTPclasses.html" #archivo de salida

# Leemos el contenido del Archivo
contenido= filerwpe.leer_archivo(ruta_archivo)
# Parcheamos el archivo a Soup
soup= filerwpe.parchear_archivo(contenido)


               
# Elementos del Fin del documento
elementos = soup.find_all(class_="FIN")

for elem in elementos:
    siguiente = elem.find_next()
    while siguiente :
        siguiente['class']="FIN"
        siguiente = siguiente.find_next()



# Elementos de Seccion
elementos = soup.find_all(class_="Seccion")

for elem in elementos:
    anterior = elem.find_previous_sibling()
    if anterior and (anterior.get_text()).isupper() and "Indice-Secciones"not in anterior['class'] and "Codifique-primero" not in anterior['class'] and  "Pie-de-pagina" not in anterior['class'] and "Nota" not in anterior['class'] and "Incluye" not in anterior['class'] and  "Excluye" not in anterior['class']  and "Excluye2" not in anterior['class']  and "Capitulo" not in anterior['class'] and "Enfermedad_nivel2" not in anterior['class'] and "Enfermedad_nivel1" not in anterior['class'] and "Enfermedad_nivel0" not in anterior['class'] and "actualizacion" not in anterior['class']: 
        anterior['class']='Seccion'


elementos = soup.find_all(class_="Seccion")

for elem in elementos:
    siguiente = elem.find_next()
    while siguiente :
        if "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()        
        if "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']  or "Excluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class']  or "actualizacion" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break  
        if (siguiente.get_text()).isupper() and "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class'] and "Excluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and  "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Seccion"
        else:
            if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class'] and "Excluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and  "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
                siguiente['class']="Seccion-Descripcion"
            
        
        siguiente = siguiente.find_next()

# Elementos de Capitulo
capitulos=soup.find_all(class_="Capitulo")

for elem in capitulos:
     siguiente = elem.find_next()
     while siguiente :
        if "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        
        if "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']  or "Excluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class']  or "actualizacion" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break  
        
        if (siguiente.get_text()).isupper() and "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class'] and "Excluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and  "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Capitulo"
        else:
            if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class'] and "Excluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and  "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
                siguiente['class']="Capitulo-Descripcion"
        
        siguiente = siguiente.find_next()

# Elementos que son asociados a Imagenes que descartaremos
images =soup.find_all('img')
for elemento in images:
    elemento.extract()
soup.prettify()

# Elementos de Pies de pagína
pies_pag=soup.find_all(class_="Pie-de-pagina")


for elem in pies_pag:
    anterior = elem.find_previous_sibling()
    if anterior is not None:
        if "Pie-de-pagina" not in anterior['class'] and str(anterior.get_text())=="Lista Tabular Enfermedades":
            anterior['class']="Pie-de-pagina"
            anterior = anterior.find_previous_sibling()
            if anterior is not None:
                if "Pie-de-pagina" not in anterior['class'] and str(anterior.get_text())=="1472":
                    anterior['class']="Pie-de-pagina"
                    
    siguiente = elem.find_next()
    while siguiente :
        if "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next() 
            if siguiente:
                proximo= siguiente.find_next()
            if proximo:
                tercero=proximo.find_next()
            if not siguiente or not proximo or not tercero or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']  or "Excluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class']  or "actualizacion" in siguiente['class'] or "FIN" in siguiente['class']:
                break 
            if "Pie-de-pagina" in siguiente['class'] and "Pie-de-pagina" in tercero['class']:
                if "Indice-Secciones"not in proximo['class'] and "Codifique-primero" not in proximo['class'] and  "Incluye" not in proximo['class'] and "Nota" not in proximo['class'] and "Excluye" not in proximo['class']  and "Excluye2" not in proximo['class']  and "Capitulo" not in proximo['class'] and "Seccion" not in proximo['class'] and "Enfermedad_nivel2" not in proximo['class'] and "Enfermedad_nivel1" not in proximo['class'] and "Enfermedad_nivel0" not in proximo['class'] and "actualizacion" not in siguiente['class']: 
                    proximo['class']="Pie-de-pagina"
                    # añado
            if "Pie-de-pagina" not in siguiente['class'] and siguiente.get_text().isupper() and "Indice-Secciones"not in proximo['class'] and "Codifique-primero" not in proximo['class'] and  "Incluye" not in proximo['class'] and "Nota" not in proximo['class'] and "Excluye" not in proximo['class']  and "Excluye2" not in proximo['class']  and "Capitulo" not in proximo['class'] and "Seccion" not in proximo['class'] and "Enfermedad_nivel2" not in proximo['class'] and "Enfermedad_nivel1" not in proximo['class'] and "Enfermedad_nivel0" not in proximo['class'] and "actualizacion" not in siguiente['class']:
                siguiente['class']="Pie-de-pagina"
                    # Termino añadir
        else:
            if siguiente:
                proximo= siguiente.find_next()
            if not siguiente or not proximo or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']  or "Excluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class']  or "actualizacion" in siguiente['class']:
                break
            if "Pie-de-pagina" in elem['class'] and "Pie-de-pagina" in proximo['class']:
                if "Indice-Secciones"not in proximo['class'] and "Codifique-primero" not in proximo['class'] and  "Incluye" not in proximo['class'] and "Nota" not in proximo['class'] and "Excluye" not in proximo['class']  and "Excluye2" not in proximo['class']  and "Capitulo" not in proximo['class'] and "Seccion" not in proximo['class'] and "Enfermedad_nivel2" not in proximo['class'] and "Enfermedad_nivel1" not in proximo['class'] and "Enfermedad_nivel0" not in proximo['class'] and "actualizacion" not in siguiente['class']: 
                    siguiente['class']="Pie-de-pagina"
        
        siguiente = siguiente.find_next()







# Elementos de Incluyes
incluyes=soup.find_all(class_="Incluye")
for elem in incluyes:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next() 
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']  or "Excluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class']  or "actualizacion" in siguiente['class'] or "FIN" in siguiente['class']:
            break 
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Excluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Incluye"
        
        siguiente = siguiente.find_next()





# Elementos de Notas
indice_secciones=soup.find_all(class_="Nota")
for elem in indice_secciones:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or  "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class'] or "Incluye" in siguiente['class']  or "Excluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']: 
            # print("sale del bucle")
            break  
        if "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Incluye" not in siguiente['class'] and "Excluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Nota"
            # print(siguiente)
        
        siguiente = siguiente.find_next()



# Elementos de Excluyes
excluyes=soup.find_all(class_="Excluye")
for elem in excluyes:
    #  print(str(elem)+"\n")
     siguiente = elem.find_next()
     while siguiente : 
        # if siguiente and "Pie-de-pagina"  in siguiente['class']:
        #     import ipdb; ipdb.set_trace();
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next() 
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or  "Nota" in siguiente['class']  or "Incluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Excluye"
            # print(siguiente)
            # print("sale del bucle")
        
        siguiente = siguiente.find_next()



# Elementos de Excluyes2
excluyes_dos=soup.find_all(class_="Excluye2")
for elem in excluyes_dos:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']   or "Excluye" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break  
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class']  and "Excluye" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Excluye2"
        
        siguiente = siguiente.find_next()


# Elementos de Enfermedad_Nivel0
Enfermedadn0=soup.find_all(class_="Enfermedad_nivel0")
for elem in Enfermedadn0:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or  "Nota" in siguiente['class']  or "Incluye" in siguiente['class']   or "Excluye" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Excluye2" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break  
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class']  and "Excluye" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Excluye2" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Enfermedad_nivel0-Descripcion"
        
        siguiente = siguiente.find_next()


# Elementos de Enfermedad_Nivel1
Enfermedadn1=soup.find_all(class_="Enfermedad_nivel1")

for elem in Enfermedadn1:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']   or "Excluye" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class']  or "Excluye2" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class'] :
            break  
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class']  and "Excluye" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "Excluye2" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Enfermedad_nivel1-Descripcion"
        siguiente = siguiente.find_next()


# Elementos de Enfermedad_Nivel2
Enfermedadn2=soup.find_all(class_="Enfermedad_nivel2")
for elem in Enfermedadn2:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class'] or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']   or "Excluye" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class'] or "Enfermedad_nivel2" in siguiente['class'] or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class']  or "Excluye2" in siguiente['class'] or "actualizacion" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break  
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class']  and "Excluye" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "Excluye2" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Enfermedad_nivel2-Descripcion"
        
        siguiente = siguiente.find_next()




# Elementos de Enfermedad_Nivel0 Actualizados
Enfermedadn0=soup.find_all(class_="Enfermedad_nivel0-actualizacion")
for elem in Enfermedadn0:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or  "Nota" in siguiente['class']  or "Incluye" in siguiente['class']   or "Excluye" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class']  or "Excluye2" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break  
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class']  and "Excluye" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Excluye2" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Enfermedad_nivel0-actualizacion-Descripcion"
        
        siguiente = siguiente.find_next()


# Elementos de Enfermedad_Nivel1 Actualizados
Enfermedadn1=soup.find_all(class_="Enfermedad_nivel1-actualizacion")
for elem in Enfermedadn1:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class']  or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']   or "Excluye" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class']  or "Excluye2" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break  
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class']  and "Excluye" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "Excluye2" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Enfermedad_nivel1-actualizacion-Descripcion"
            
        siguiente = siguiente.find_next()


# Elementos de Enfermedad_Nivel2 Actualizados
Enfermedadn2=soup.find_all(class_="Enfermedad_nivel2-actualizacion")
for elem in Enfermedadn2:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and  "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Codifique-primero" in siguiente['class'] or "Nota" in siguiente['class']  or "Incluye" in siguiente['class']   or "Excluye" in siguiente['class']   or "Capitulo" in siguiente['class']  or "Seccion" in siguiente['class'] or "Enfermedad_nivel2" in siguiente['class'] or "Enfermedad_nivel1" in siguiente['class']  or "Enfermedad_nivel0" in siguiente['class']  or "Excluye2" in siguiente['class'] or "actualizacion" in siguiente['class'] or "caracter" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']:
            break  
        if "Indice-Secciones"not in siguiente['class'] and "Codifique-primero" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Nota" not in siguiente['class'] and "Incluye" not in siguiente['class']  and "Excluye" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "Excluye2" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Enfermedad_nivel2-actualizacion-Descripcion"
        
        siguiente = siguiente.find_next()



# Elementos de Codifique primero
codifiques_primero=soup.find_all(class_="Codifique-primero")

for elem in codifiques_primero:
     siguiente = elem.find_next()
     while siguiente :
        while siguiente and "Pie-de-pagina" in siguiente['class']:
            siguiente = siguiente.find_next()
        if not siguiente or "Indice-Secciones" in siguiente['class'] or "Nota" in siguiente['class']  or "Incluye" in siguiente['class'] or "Excluye" in siguiente['class']   or "Excluye2" in siguiente['class']   or "Capitulo" in siguiente['class'] or "Seccion" in siguiente['class']  or "Enfermedad_nivel2" in siguiente['class']  or "Enfermedad_nivel1" in siguiente['class'] or "Enfermedad_nivel0" in siguiente['class'] or "caracter" in siguiente['class']  or "actualizacion" in siguiente['class'] or "FIN" in siguiente['class'] or "actualizacion" in siguiente['class']: 
            break  
        if "Nota" not in siguiente['class'] and  "Pie-de-pagina" not in siguiente['class'] and "Incluye" not in siguiente['class'] and "Excluye" not in siguiente['class']  and "Excluye2" not in siguiente['class']  and "Capitulo" not in siguiente['class'] and "Seccion" not in siguiente['class'] and "Enfermedad_nivel2" not in siguiente['class'] and "Enfermedad_nivel1" not in siguiente['class'] and "Enfermedad_nivel0" not in siguiente['class'] and "actualizacion" not in siguiente['class']: 
            siguiente['class']="Codifique-primero-Descripcion"
        
        siguiente = siguiente.find_next()





# Elementos de Excluye  # fs3 fc1
elementos_exc = soup.find_all(class_="fs3 fc1")

for elem in elementos_exc:
    padre = elem.find_parent()
    if padre and "Excluye2" in padre['class']: 
        elem['class']='Excluye2-Descripcion'
    if padre and "Excluye" in padre['class']: 
        elem['class']='Excluye-Descripcion'

# Elementos de Actualizado # fc1 sc4
# elementos_modificados = soup.find_all(class_="fc1 sc4")

# Guardamos archivo
filerwpe.archivar_completo(str(soup),ruta_salida1)







# Asignamos el tiempo final
end_time = time.time()

# Imprimimos tiempo que ha tardado
print(f"Tiempo de ejecución: {end_time - start_time} segundos")





