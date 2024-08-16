from PyPDF2 import PdfWriter, PdfReader
import os

class PdfRpaSelenium:
    def __init__(self, pdfRpa, pdfSelenium):
        self.pdfRpa = pdfRpa
        self.pdfSelenium = pdfSelenium

    """Combinar los pdf de la version de RPA, y selenium"""
    def pdf_combination(self):
        if not self.pdfRpa or not self.pdfSelenium:
            print("Error, una o las dos rutas de los archivos PDF son None")
            return
        
        try:
            pdf_path = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot_final.pdf"
            pdf_writer = PdfWriter()

            # Añadir las páginas de los PDFs de RPA y Selenium
            self.add_pdf_to_writer(pdf_writer, self.pdfRpa)
            self.add_pdf_to_writer(pdf_writer, self.pdfSelenium)

            with open(pdf_path, 'wb') as file:
                pdf_writer.write(file)

            print("PDFs combinados correctamente")

        except Exception as e:
            print(f"Error combinando los PDFs: {str(e)}")
            
    """Añadir las páginas de los PDFs de RPA y Selenium"""
    def add_pdf_to_writer(self, pdf_writer, pdf_list):
        for pdf_file in pdf_list:
            if not os.path.exists(pdf_file):
                print(f"Error: El archivo {pdf_file} no existe")
                continue
            try:
                with open(pdf_file, 'rb') as pdf:
                    reader = PdfReader(pdf)
                    if len(reader.pages) == 0:
                        print(f"El archivo {pdf_file} no contiene páginas")
                        continue
                    for page in reader.pages:
                        pdf_writer.add_page(page)
            except Exception as e:
                print(f"Error leyendo {pdf_file}: {str(e)}")
                continue
