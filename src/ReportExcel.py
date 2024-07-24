import pandas
import os

class ReportExcel:
    """creo fichero excel con sus columnas y algunos datos"""
    def __init__(self):
        path_xlsx = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot.xlsx"

        self._columnas = pandas.DataFrame({
            "Name_robot": ["ABC8273", "ABC82763", "ABC82673"],
            "Status_creation": ["DONE","DONE","WIP"],
            "Status_pdf": ["DONE","DONE","WIP"],
            "Path_pdf": ["/users/Ali","/users/Jorge","/users/Alex"],
            "Status_final": ["DONE","DONE","WIP"]
        })
        os.makedirs(os.path.dirname(path_xlsx),exist_ok=True)
        self._columnas.to_excel(path_xlsx, sheet_name='Robot1')
        #self._excel_writer._save()

        print('Excel generado')

   