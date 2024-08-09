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
                rpa_reader = PyPDF4.PdfFileReader(rpa_pdf)
                selenium_reader = PyPDF4.PdfFileReader(selenium_pdf)

                # Escritor de PDF
                pdf_writer = PyPDF4.PdfFileWriter()

                # Añade todas las páginas del PDF de RPA
                for pg_rpa_num in range(rpa_reader.getNumPages()):
                    pdf_writer.addPage(rpa_reader.getPage(pg_rpa_num))

                # Añade todas las páginas del PDF de Selenium
                for pg_sel_num in range(selenium_reader.getNumPages()):
                    pdf_writer.addPage(selenium_reader.getPage(pg_sel_num))

                # Escribe el PDF combinado en un nuevo pdf
                path = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot_final.pdf"
                with open(path, 'wb') as file:
                    pdf_writer.write(file) 
            print("PDFs combinados correctamente")
        except Exception:
            print(f"Error combinando los PDFs ")