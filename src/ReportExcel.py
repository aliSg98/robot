import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

class ReportExcel:
    """crear fichero excel"""
    def __init__(self, path_xlsx, logger):
        self.path_xlsx = path_xlsx
        try:
            self.df = pd.read_excel(self.path_xlsx)  # Intenta leer el archivo existente
        except FileNotFoundError:
            self.df = pd.DataFrame()  # Si no existe, crea un DataFrame vacío
        self.logger = logger
       

    
    def changeColor(self):
        #Cargar el fichero excel con openpyxl
        open_wb = load_workbook(self.path_xlsx)
        res = open_wb.active
        
        #Definir color azul
        color = PatternFill(start_color="ADD8E6",end_color="ADD8E6",fill_type="solid")

        #solo cojo los encabezados de la primera fila
        for col in res[1]:
            col.fill = color
        #guardar excel con el nuevo color
        open_wb.save(self.path_xlsx)

        """Cambiar color segun sea wip -> amarillo, done --> verde, fail --> rojo"""
        color_wip = PatternFill(start_color="FFFF00",end_color="FFFF00",fill_type="solid")
        color_done = PatternFill(start_color="00FF00",end_color="00FF00",fill_type="solid")
        color_fail = PatternFill(start_color="FF0000",end_color="FF0000",fill_type="solid")

        #columans que me interesa cambiar el color
        c = [2,3,5]
        for columna in res.iter_rows(min_row=2,max_row=res.max_row):
            for col in c:
                #openpyxl usa indices base 1
                celda=columna[col-1]
                #paso a minusculas para que me coja independientemente sea mayus o minus
                cell_value = str(celda.value).strip().lower()
                if cell_value in ['wip']: celda.fill = color_wip
                elif cell_value in ['done']: celda.fill = color_done
                elif cell_value in ['fail']: celda.fill = color_fail
        open_wb.save(self.path_xlsx)
        self.logger.setMessage("Excel generado con colores",'info')

    def create_excel(self, data):
        self.df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(self.path_xlsx),exist_ok=True)
        self.df.to_excel(self.path_xlsx, index=False, sheet_name='Robot1')


    def add_data(self, new_data):
        try:
            old_df = pd.read_excel(self.path_xlsx)
            new_df = pd.DataFrame(new_data)
            self.df = pd.concat([old_df, new_df], ignore_index=True)            
        except FileNotFoundError:
            self.df = pd.DataFrame(new_data)
            self.logger.setMessage("Excel no encontrado",'info')
        self.df.to_excel(self.path_xlsx, index=False, sheet_name='Robot1')
               

           
            

        