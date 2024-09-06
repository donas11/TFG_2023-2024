# Usar una imagen
FROM ubuntu:22.04

# Instalar python y demás cosas para descargar el .deb y dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    wget \
    fontforge \
    poppler-utils \
    ghostscript \
    libcairo2 \
    libglib2.0-0 \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libfontconfig1 \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# Creamos enlace simbolico python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Descargar el paquete .deb de pdf2htmlEX e Instalar el paquete .deb
RUN wget https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb && \
    apt install ./pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb 

# Limpiar los archivos descargados para reducir el tamaño de la imagen
RUN rm pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb
  
# Crear el entorno virtual
RUN python -m venv venv

# Copiar el archivo de requerimientos y demás archivos
COPY requirements.txt .
COPY . .

# Actualizar pip y wheel en el entorno virtual
RUN ./venv/bin/python -m pip install --upgrade pip
RUN ./venv/bin/pip install --upgrade wheel

# Instalar dependencias de Python y damos permisos al script
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Paso 00 Pasamos PDF a HTML
# url_imputfile, input_pdffile='./.CIE10ES_2018_diag_pdf_20180202LT.pdf' output_htmlfile = "./CIE10LT.html"
RUN ./venv/bin/python 00PDFtoHTML.py 

# Paso 01 Pasamos procesamos en HTML los patrones y modificamos etiquetas class
# output_htmlfile = "./CIE10LTP16EFN2.html"
RUN ./venv/bin/python 01preprocessHTML.py 

# Paso 02 Pasamos otro procesado en HTML modificando etiquetas class
#  output_htmlfile = "./CIE10LTPclasses.html"
RUN ./venv/bin/python 02preHTML.py 

# Paso 03 Pasamos HTML a XML
#  output_xmlfile = "./diccionario.xml"
RUN ./venv/bin/python 03Mod_diccionario.py 

# Paso 04 Volcamos XML en Base de Datos MongoDB
# input_xmlfile='./diccionario.xml'
CMD ["./venv/bin/python", "04exportamongo.py"] 
