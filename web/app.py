from flask import Flask, render_template, request, redirect, url_for, jsonify, session
# from flask_sslify import SSLify
from flask_session import Session  
from pymongo import MongoClient
from config import MONGODB_URL, DATABASE_NAME,PUERTO
from decimal import Decimal
import re
import pandas as pd

client = MongoClient(MONGODB_URL, PUERTO)
db = client[DATABASE_NAME]
db.datos.create_index([('$**', 'text')])

global num_pagina
num_pagina= 1

app = Flask(__name__)
app.secret_key = "cie10"

# Configurar Flask-Session
app.config["SESSION_TYPE"] = "filesystem"  # Almacenar sesiones en el sistema de archivos 
Session(app)

# sslify = SSLify(app) # por la seguridad


# Función para consultar datos según la opción
def consultar_datos_opcion(opcion):
   if "usuario" in session:
        # Obtener todos los datos de la colección "opción" 
        if opcion =="ENFERMEDAD" :
            global num_pagina
            print("NuM pag:"+str(num_pagina))
            tam_pagina=500
            num_pagina=88
            saltos_de_pagina= (num_pagina-1)*tam_pagina
            total_de_paginas=db[opcion].count_documents({})
            print(saltos_de_pagina)
            datos = db[opcion].find().skip(saltos_de_pagina).limit(tam_pagina)
        else:
            datos = db[opcion].find()
        
        # print("datos: -")
        # print(datos)
        return list(datos)


def siguiente_codigo(codigo):
    if len(codigo)==3:
        letra_codigo=codigo[0]
        numero_codigo=int(codigo[1:])
        
        if numero_codigo < 99:
            numero_codigo +=1
        else:
            numero_codigo =0
            if letra_codigo != 'Z':
                letra_codigo = chr( ord(letra_codigo)+1)
        
        siguiente_codigo = letra_codigo + str(numero_codigo).zfill(2)
    
    else:
        letra_codigo=codigo[0]

        numero_codigo=int(codigo[1:3])
        # print("que cdoge:")
        # print(codigo[1:3])
        tam_nivel=len(str(codigo[4:])) 
        
        if (codigo[4:])=="": 
            numero_subnivel = 0
        else: 
            numero_subnivel=int(codigo[4:])
        
    
        if numero_subnivel < 99:
            numero_subnivel +=1
        else:
            numero_codigo +=1
            



        siguiente_codigo = letra_codigo + str(numero_codigo).zfill(2) +"."+ str(numero_subnivel).zfill(tam_nivel)
        # print("codigo")
        # print(codigo)
        # print("siguiente_codigo")
        # print(siguiente_codigo)

    return siguiente_codigo


def separar_referencias(codigos_referencias):
    rangos = codigos_referencias.strip("()").split('-')
    return rangos


# Función para buscar en la base de datos según un texto dado
def buscar_en_base_de_datos(coleccion,texto):
    if "usuario" in session:
        # Buscar en la colección "datos" que contienen el texto proporcionado en algún campo
        colleciones= ["ENFERMEDAD","SECCION","ENFERMEDAD_EXCLUYE","ENFERMEDAD_EXCLUYE_ENFERMEDAD","ENFERMEDAD_EXCLUYE_SECCION"]
        resultados_final=list()
        resultados2=[]
        if coleccion == "between":    
            rangos= separar_referencias(texto)
            print(rangos)
            if len(rangos)==2:
                colection = colleciones[0]
                # busqueda_entre = re.compile(f"^[{rangos[0]}-{rangos[1]}][0-9]+$")
                # resultados = db[colection].find({ "Codigo_Enfermedad": { "$regex": busqueda_entre} } )
                codigo_actual =rangos[0]
                while codigo_actual!= rangos[1] :
                    busqueda= r''+codigo_actual+''
                    resultados_temp = db[colection].find({ "Codigo": busqueda })
                    # print(resultados_temp)
                    for elem  in resultados_temp:
                        resultados_final.append(elem)
                    codigo_actual = siguiente_codigo(codigo_actual)
                    # print(codigo_actual)
                    # print(rangos[1])
                if codigo_actual == rangos[1]:
                    busqueda= r''+codigo_actual+''
                    resultados_temp = db[colection].find({ "Codigo": busqueda })
                    # print("IF resultados_temp")
                    # print(resultados_temp)
                    for elem  in resultados_temp:
                        resultados_final.append(elem)

                    # busqueda= r''+rangos[0]+''
                    # resultados_temp = db[colection].find({ "Codigo": busqueda })
                    # busqueda= r''+rangos[1]+''
                    # resultados_temp2= db[colection].find({ "Codigo": busqueda })
                # resultados=list(resultados_temp)+list(resultados_temp2)
        if coleccion == "enfermedad":
            if texto :
                colection = colleciones[0] 
                guion_punto = r'\.-'
                guion = r'\-'
                coma = r'\,'
                tiene_guion_punto= re.findall(guion_punto,texto)
                tiene_coma= re.findall(coma,texto)
                tiene_guion= re.findall(guion,texto)
                if tiene_guion!= [] or tiene_coma!= [] or tiene_guion_punto!= []:
                    if len(tiene_guion_punto)>0:
                        # texto= re.sub(tiene_guion_punto,"",texto)
                        texto= texto[:-2]
                        busqueda= r''+texto+''
                        resultados = db[colection].find({ "Codigo": busqueda })
                        for resultado in resultados:
                            resultados_final.append(resultado)
                    if len(tiene_coma)>0:    
                        codigos_texto=texto.split(',')
                        # print(codigos_texto)
                        for codigo_texto in codigos_texto:
                            # print("===============Busqueda:"+codigo_texto+":")
                            codigo_texto= re.sub(r'\s+', '', codigo_texto)
                            busqueda= r''+codigo_texto+''
                            resultados = db[colection].find({ "Codigo": busqueda })
                            for resultado in resultados:
                                # print(resultado)
                                resultados_final.append(resultado)
                    if len(tiene_guion)>0:
                        codigo_a_buscar= texto[:-1]
                        busqueda= r''+codigo_a_buscar+''
                        resultados = db[colection].find({ "Codigo": busqueda })
                        for resultado in resultados:
                            resultados_final.append(resultado) 
                            # print(resultados_final)
                    # for resultado in resultados:
                    #     resultados_final.append(resultado)
                    # resultados2=""

                else:
                    espacio = r'\s+'
                    tiene_espacio= re.findall(espacio,texto)
                    if len(tiene_espacio) >0:
                        codigos_texto=texto.split(' ')
                        for codigo_texto in codigos_texto:
                            busqueda= r''+codigo_texto+''
                            resultados = db[colection].find({ "Codigo": busqueda })
                            for resultado in resultados:
                                resultados_final.append(resultado)
                    else:    
                        busqueda= r''+texto+''
                        resultados = db[colection].find({ "Codigo": busqueda })
                        for resultado in resultados:
                            resultados_final.append(resultado)
                        resultados2=""
        if coleccion == "nombreenfermedad":
            colection = colleciones[0]
            
            busqueda= r''+texto+''
            resultados = db[colection].find({ "Nombre":{"$regex": busqueda}})
            for resultado in resultados:
                resultados_final.append(resultado)
            resultados2=""        
        if coleccion == "excluyeenfermedad":
            colection = colleciones[3]
            busqueda= r''+texto+''
            resultados = db[colection].find({ "Codigo_Enfermedad": busqueda })
            for resultado in resultados:
                resultados_final.append(resultado)
            colection = colleciones[4]
            resultados2 = db[colection].find({ "Codigo_Enfermedad": busqueda })
        # print("list(resultados)")    
        # print(list(resultados_final))
        return list(resultados_final),list(resultados2)

 
@app.route('/')
def index():
    
    return '¡Hola, mundo!'


    

@app.route('/politicacookies')
def politicacookies():
    return 'Esta página solo guarda Cookie tecnica para la sesión activa'


    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        if usuario == "cie10" and clave == "cie10":
            session["usuario"] = usuario
            return redirect(url_for("dashboard"))
        else:
            return "Credenciales incorrectas. Inténtalo de nuevo."
    return render_template("login.html")



@app.route("/logout") 
def logout():
    session.pop("usuario", None)  # Eliminar el usuario de la sesión
    return redirect(url_for("login"))
    

# Ruta para mostrar datos según la opción seleccionada 
@app.route("/datos/<opcion>",methods=["GET", "POST"])
def mostrar_datos(opcion):
    if "usuario" in session:
        # obtener los datos según la opción seleccionada
        datos = consultar_datos_opcion(opcion)
        # Convierte los datos en texto HTML para enviarlos de vuelta al cliente
        if opcion =="ENFERMEDAD" :
            return redirect(url_for("get_table"))
        if not datos:  
            html =" No se han encontrado datos"
        else:
                
                html = "<table border='1'>"
                html +=" <tr>"
                if opcion =="SECCION":
                    html +="<th>ID</th>"
                if opcion =="ENFERMEDAD" :
                    html +="<th>Código</th>"
                html +="<th>Nombre</th>"
                html +=" <th>Aclaracion</th>"
                html += "</tr>"
                for dato in datos:
                        html +=" <tr>"
                        if opcion =="SECCION" :
                            html +="<td>{}</td>".format(dato['ID'])
                        if opcion =="ENFERMEDAD" :
                            html +="<td>{}</td>".format(dato['Codigo'])
                        html +="<td>{}</td>".format(dato['Nombre'])
                        html +=" <td>{}</td>".format(dato['Aclaracion'])
                        html += "</tr>"
        return html

# Ruta para realizar una búsqueda en la base de datos
@app.route("/busqueda",methods=["GET", "POST"])
def busqueda():
    html = ""
    if "usuario" in session:
        resultados=""
        resultados2=""
        enfermedad = request.args.get("enfermedad")
        # realizamos la búsqueda en la base de datos
        if enfermedad is not None and enfermedad!= "":
            resultados = buscar_en_base_de_datos("enfermedad",enfermedad)
            if not resultados or resultados == "":  
                html =" No se han encontrado datos"
            else:
                html = "<table border='1'>"
                html +=" <tr>"
                html +="<th>Código</th>"
                html +="<th>Nombre</th>"
                html +=" <th>Aclaracion</th>"
                html += "</tr>"
                # print(resultados)
                for resultado in resultados:
                    for result  in resultado:
                        if result !=[]:
                        # print(resultado['Codigo'])
                            html +=" <tr>"
                            # html +="<th>{}</th>".format(resultado[0]['Codigo'])
                            # html +="<th>{}</th>".format(resultado[0]['Codigo'])
                            # html +="<th>{}</th>".format(resultado[0]['Nombre'])
                            # html +=" <th>{}</th>".format(resultado[0]['Aclaracion'])
                            html +="<td>{}</td>".format(result['Codigo'])
                            html +="<td>{}</td>".format(result['Nombre'])
                            html +=" <td>{}</td>".format(result['Aclaracion'])
                            html += "</tr>"



        enfermedad_excluye =request.args.get("excluyeenfermedad") 
        if enfermedad_excluye is not None and enfermedad_excluye != "":
            resultados,resultados2 = buscar_en_base_de_datos("excluyeenfermedad",enfermedad_excluye)
            if not resultados or resultados == "":  
                html =" No se han encontrado datos"
            else: 
                html = "<table border='1'>"
                html +=" <tr>"
                html +="<th>Código Enfermedad</th>"
                html +=" <th>Códigos Excluye</th>"
                html += "</tr>"
                for resultado in resultados:
                    html +=" <tr>"
                    # html +='<th><a onclick="buscarCodigo("\''+resultado['Codigo_Enfermedad']+'\'"); return false; ">{}</a></th>'.format(resultado['Codigo_Enfermedad'])
                    
                    html +='<th><button id="Codigo" onclick="buscarCodigo(this)" value="'+resultado['Codigo_Enfermedad']+'">{}</button></th>'.format(resultado['Codigo_Enfermedad'])
                    sinparentesis = format(resultado['CodRef_Enfermedad']).strip("()")
                    # html +="<th>{}</th>"
                    html +='<th><button id="Codigo" onclick="buscarCodigo(this)" value="'+sinparentesis+'">'+sinparentesis+'</button></th>'
                    html += "</tr>"
                for resultado in resultados2:
                    enfermedades_en_rango=buscar_en_base_de_datos("between",resultado['ID_Seccion'])
                    for enfermedad_en_rango in enfermedades_en_rango:
                        if enfermedad_en_rango != []:
                            for elem_enf_rango in enfermedad_en_rango:
                                # print("enfermedad_en_rango")
                                # print(enfermedad_en_rango)
                                html +=" <tr>"
                                # html +="<th>{}</th>".format(resultado['Codigo_Enfermedad'])
                                html +='<th><button id="Codigo" onclick="buscarCodigo(this)" value="'+resultado['Codigo_Enfermedad']+'">{}</button></th>'.format(resultado['Codigo_Enfermedad'])
                            
                                html +='<th><button id="Codigo" onclick="buscarCodigo(this)" value="'+elem_enf_rango['Codigo']+'">{}</button></th>'.format(elem_enf_rango['Codigo'])
                                # html +='<th><button id="Codigo" onclick="buscarCodigo(this)" value="'+enfermedad_en_rango['Codigo']+'">{}</button></th>'.format(enfermedad_en_rango['Codigo'])
                                # html +=" <tr>"
                                # html +='<th><button id="Codigo" onclick="buscarCodigo(this)" value="'+resultado['Codigo_Enfermedad']+'">{}</button></th>'.format(resultado['Codigo_Enfermedad'])
                                
                                # # html +='<th><button id="Codigo" onclick="buscarCodigo(this)" value="'+enfermedad_en_rango[1]['Codigo']+'">{}</button></th>'.format(enfermedad_en_rango[1]['Codigo'])
                                # html +='<th><button id="Codigo" onclick="buscarCodigo(this)" value="'+enfermedad_en_rango['Codigo']+'">{}</button></th>'.format(enfermedad_en_rango['Codigo'])
                                
                            # html +="<th>{}</th>".format(enfermedad_en_rango[0]['Codigo'])
                                html += "</tr>"
                        # html +=" <tr>"
                        # html +="<th>{}</th>".format(resultado['Codigo_Enfermedad'])
                        # html +="<th>{}</th>".format(resultado['ID_Seccion'])
                        # html += "</tr>"

        
        # Convierte los resultados en texto HTML para enviarlos de vuelta al cliente

        
        nombre_enfermedad=  request.args.get("nombreenfermedad") 
        if nombre_enfermedad is not None and nombre_enfermedad!= "":
            resultados=""
            resultados2=""
            resultados = buscar_en_base_de_datos("nombreenfermedad",nombre_enfermedad)
            # print(resultados)
            if not resultados or resultados == "":  
                html =" No se han encontrado datos"
            else:
                html = "<table border='1'>"
                html +=" <tr>"
                html +="<th>Código</th>"
                html +="<th>Nombre</th>"
                html +=" <th>Aclaracion</th>"
                html += "</tr>"
                for resultado in resultados:
                    for result  in resultado:
                        if result !=[]:
                            html +=" <tr>"
                            html +="<td>{}</td>".format(result['Codigo'])
                            html +="<td>{}</td>".format(result['Nombre'])
                            html +=" <td>{}</td>".format(result['Aclaracion'])
                            html += "</tr>"
        if html is None:
            html =" No se han encontrado datos"
            
        return html
    


@app.route("/dashboard",methods=["GET", "POST"])
def dashboard():
    if "usuario" in session:
        # Aquí puedes realizar consultas a la base de datos y enviar los datos a la plantilla
        # data = db["mi_coleccion"].find()
        data = db["ENFERMEDAD"].find()
        return render_template("dashboard.html", data=data)
    return redirect(url_for("login"))



   
@app.route('/get_table', methods=['GET'])
def get_table():
    page = int(request.args.get('page', 1))
    per_page = 500  # Número de resultados por página
    total = db["ENFERMEDAD"].count_documents({})  # Total de documentos
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0) # Calcular el número total de páginas
    
    # Obtener parámetros de paginación de la solicitud
    page = int(request.args.get('page', 1))
    per_page = 500  # Mostrar 500 resultados por página

    # Calcular el número de documentos a saltar
    skip = (page - 1) * per_page

    # Obtener los documentos con limitación y paginación
    projection = {'_id': 0, 'Codigo': 1, 'Nombre': 1, 'Aclaracion': 1}
    enfermedades = list(db["ENFERMEDAD"].find({}, projection).skip(skip).limit(per_page))
    # enfermedades = list((db["ENFERMEDAD"].find()).limit(500))
    # Convertir los resultados en un DataFrame de pandas
    df = pd.DataFrame(enfermedades)
    
    # Convertir el DataFrame a HTML
    html_table = df.to_html(escape=False, classes='table table-striped', index=False)

    max_page_links = 13  # Número máximo de enlaces de página a mostrar
    start_page = max(1, page - max_page_links // 2)
    end_page = min(total_pages, start_page + max_page_links - 1)
    if end_page - start_page + 1 < max_page_links:
        start_page = max(1, end_page - max_page_links + 1)
    
    # Renderizar una plantilla HTML con la tabla junto con los controles de paginación
    return render_template(
        'get_table.html',
        table=html_table,
        page=page,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page
    )
    

   



if __name__ == "__main__":
    app.run(debug=True)