# Usar una imagen
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv

    # Creamos enlace simbolico python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Crear el entorno virtual
RUN python -m venv venv

# Copiar requirements y instalarlos
COPY ./requirements.txt requirements.txt

# Actualizar pip y wheel en el entorno virtual
RUN ./venv/bin/python -m pip install --upgrade pip
RUN ./venv/bin/pip install --upgrade wheel

RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt
# Copiar todo el código fuente de la aplicación
COPY . .

# Definir la variable de entorno
ENV FLASK_APP=app.py

# Exponer el puerto para Flask
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
ENTRYPOINT ["./venv/bin/python", "-m", "flask"]
CMD ["run", "--host=0.0.0.0"]
