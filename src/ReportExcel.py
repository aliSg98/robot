import pandas
import os
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

class ReportExcel:
    """creo fichero excel con sus columnas y algunos datos, y añado colores"""
    def __init__(self,logger):
        self._path_xlsx = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot.xlsx"

        self._columnas = pandas.DataFrame({
            "Name_robot": ["ABC8273", "ABC82763", "ABC82673","AHJD77"],
            "Status_creation": ["DONE","DONE","WIP","FAIL"],
            "Status_pdf": ["DONE","DONE","WIP","FAIL"],
            "Path_pdf": ["/users/Ali","/users/Jorge","/users/Alex","users/Pedro"],
            "Status_final": ["DONE","DONE","WIP","Fail"]
        })
        os.makedirs(os.path.dirname(self._path_xlsx),exist_ok=True)
        self._columnas.to_excel(self._path_xlsx, index = False, sheet_name='Robot1')
        
        #Cargar el fichero excel con openpyxl
        open_wb = load_workbook(self._path_xlsx)
        res = open_wb.active

        #Definir color azul
        color = PatternFill(start_color="ADD8E6",end_color="ADD8E6",fill_type="solid")

        #solo cojo los encabezados de la primera fila
        for col in res[1]:
            col.fill = color
        #guardar excel con el nuevo color
        open_wb.save(self._path_xlsx)

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
        open_wb.save(self._path_xlsx)
        logger.setMessage("Excel generado",'info')
        print('Excel generado')
