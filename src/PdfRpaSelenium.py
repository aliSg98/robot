import PyPDF4
import os

class PdfRpaSelenium:
    def __init__(self,pdfRpa,pdfSelenium):
        self.pdfRpa=pdfRpa
        self.pdfSelenium=pdfSelenium

    """Crear pdf vacio"""
    def empty_pdf(self, path):
        # Crear un PDF vacío
        pdf_writer = PyPDF4.PdfFileWriter()
        pdf_writer.addBlankPage(width=595, height=842)  #Tamaño A4 

        with open(path, 'wb') as file:
            pdf_writer.write(file)
        print(f"PDF vacío creado")

    """Meter los pdf de las 2 versiones en 1 sola"""
    def pdf_combination(self):
        # Comprobar si los arrays están vacíos
        if not self.pdfRpa or not self.pdfSelenium:
            print("Error, una o las dos rutas de los archivos PDF son None")
            return
        
        try:
            # Ruta del PDF
            pdf_path = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot_final.pdf"
            self.empty_pdf(pdf_path)

            # Escritor de PDF para el archivo combinado
            pdf_writer = PyPDF4.PdfFileWriter()

            # Añadir las páginas de los PDFs de RPA
            self.add_pdf_to_writer(pdf_writer, self.pdfRpa)

            # Añadir las páginas de los PDFs de Selenium
            self.add_pdf_to_writer(pdf_writer, self.pdfSelenium)

            # Escribir el PDF combinado
            with open(pdf_path, 'wb') as file:
                pdf_writer.write(file)

            print("PDFs combinados correctamente")

        except Exception as e:
            print(f"Error combinando los PDFs: {str(e)}")

    """Añadir paginas al pdf"""
    def add_pdf_to_writer(self,pdf_writer,pdf_list):
        for pdf_file in pdf_list:
            if not os.path.exists(pdf_file):
                print(f"Error: El archivo {pdf_file} no existe")
                continue
            try:
                with open(pdf_file, 'rb') as pdf:
                    reader = PyPDF4.PdfFileReader(pdf)
                    # Verificar si el archivo contiene páginas
                    if reader.getNumPages() == 0:
                        print(f"El archivo {pdf_file} no contiene páginas")
                        continue
                    for page_num in range(reader.getNumPages()):
                        pdf_writer.addPage(reader.getPage(page_num))
            except Exception as e:
                print(f"Error leyendo {pdf_file}: {str(e)}")
                continue