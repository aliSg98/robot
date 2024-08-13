import PyPDF4
import os

class PdfRpaSelenium:
    def __init__(self,pdfRpa,pdfSelenium):
        self.pdfRpa=pdfRpa
        self.pdfSelenium=pdfSelenium

    """Meter los pdf de las 2 versiones en 1 sola"""
    def pdfCombination (self):
        #Comprobar si los arrays estan vacios
        if not self.pdfRpa or not self.pdfSelenium:
            print("Error, una o las dos rutas de los archivos PDF son None")
            return
        try:
            #Escritor de PDF
            pdf_writer = PyPDF4.PdfFileWriter()

            #Recorre los PDFs de los robots de RPA y los añade al escritor
            for pdf_1 in self.pdfRpa:
                try:
                    with open(pdf_1, 'rb') as rpa_pdf:
                        rpa_reader = PyPDF4.PdfFileReader(rpa_pdf)
                        for pg_rpa_num in range(rpa_reader.getNumPages()):
                            pdf_writer.addPage(rpa_reader.getPage(pg_rpa_num))
                except Exception as e:
                    print(f"Error leyendo {pdf_1}: {str(e)}")
                    continue

            # Recorre los PDFs de los robots de selenium y los añade al escritor
            for pdf_2 in self.pdfSelenium:
                try:
                    with open(pdf_2, 'rb') as selenium_pdf:
                        selenium_reader = PyPDF4.PdfFileReader(selenium_pdf)
                        for pg_sel_num in range(selenium_reader.getNumPages()):
                            pdf_writer.addPage(selenium_reader.getPage(pg_sel_num))
                except Exception as e:
                    print(f"Error leyendo {pdf_2}: {str(e)}")
                    continue

            # Escribe el PDF combinado
            path = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot_final.pdf"
            with open(path, 'wb') as file:
                pdf_writer.write(file)

            print("PDFs combinados correctamente")
            
        except Exception as e:
            print(f"Error combinando los PDFs: {str(e)}")