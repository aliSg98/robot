import os
from src.ConnexionPostgress import ConnexionPostgress
from src.ReportExcel import ReportExcel
from src.Logger import Logger

def main():
    """Conectarse a la base de datos"""
    database = ConnexionPostgress()
    """Elegir si quieres crear la tabla o hacer un insert con los datos que quieras"""
    num = int(input("""Ingrese 1 para Crear tabla en base de datos, 
                    2 para hacer INSERT a la base de datos,  
                    3 para crear excel,
                    """))    
    #match case
    match num:
        case num if num == 1:
            #create
            database.createTable()   
            database.closeConexion()           
        case num if num == 2:
            #insert
            database.insert()
            database.closeConexion()              
        case num if num == 3:
            #Crear excel
            excel = ReportExcel()
        case _:
            print("Error") 



if(__name__ == '__main__'):
    main()