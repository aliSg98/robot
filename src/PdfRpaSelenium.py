import PyPDF4
import os

class PdfRpaSelenium:
    def __init__(self,pdfRpa,pdfSelenium):
        self.pdfRpa=pdfRpa
        self.pdfSelenium=pdfSelenium

    def pdfCombination (self):
        if not self.pdfRpa or not self.pdfSelenium:
            print("Error, Una o las dos rutas de los archivos PDF son None")
            return
        
        try:
            with open(self.pdfRpa, 'rb') as rpa_pdf, open(self.pdfSelenium, 'rb') as selenium_pdf:
                rpa_reader = PyPDF4.PdfReader(rpa_pdf)
                selenium_reader = PyPDF4.PdfReader(selenium_pdf)

                # Crea un escritor de PDF
                pdf_writer = PyPDF4.PdfWriter()

                # Añade todas las páginas del PDF de RPA
                for pg_rpa_num in range(len(rpa_reader.pages)):
                    pdf_writer.add_page(rpa_reader.pages[pg_rpa_num])

                # Añade todas las páginas del PDF de Selenium
                for pg_sel_num in range(len(selenium_reader.pages)):
                    pdf_writer.add_page(selenium_reader.pages[pg_sel_num])

                # Escribe el PDF combinado en un nuevo archivo
                path = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot_combinado.pdf"
                with open(path, 'wb') as file:
                    pdf_writer.write(path)
            print("PDFs combinados correctamente")
        except Exception:
            print("Error combinando los PDFs")