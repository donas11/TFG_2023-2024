from PyPDF2 import PdfReader, PdfWriter
import urllib.request
import subprocess
import time


# Asignamos el tiempo de inicio
start_time = time.time()

# Funcion de llamada a Libreria pdf2htmlEX en el sistema
def convert_pdf_to_html(input_file, output_file):
    subprocess.call(['/usr/local/bin/pdf2htmlEX', input_file, output_file])

# Variables de url,archivos de entrada o salida, numero de la pagina que nos interesa
url_pdffile='https://www.sanidad.gob.es/estadEstudios/estadisticas/normalizacion/CIE10/CIE10ES_2018_diag_pdf_20180202.pdf'
output_pdffile='./.CIE10ES_2018_diag_pdf_20180202LT.pdf'
input_pdffilem='./.CIE10ES_2018_diag_pdf_20180202LT.pdf'
output_htmlfile = "./CIE10LT.html"
page_num=658

# Abrimos archivo
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

# Convertimos PDF a HTML
convert_pdf_to_html(input_pdffilem, output_htmlfile)

# Asignamos el tiempo final
end_time = time.time()

# Imprimimos tiempo que ha tardado
print(f"Tiempo de ejecución: {end_time - start_time} segundos")
