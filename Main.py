import os
from src.ConnexionPostgress import ConnexionPostgress
from src.ReportExcel import ReportExcel
from src.Logger import Logger

def main():
    """Iniciar el logger"""
    logger = Logger()
    """Conectarse a la base de datos"""
    database = ConnexionPostgress()
    """Elegir si quieres crear la tabla o hacer un insert con los datos que quieras"""
    num = int(input("""Ingrese 1 para Crear tabla en base de datos, 
                    2 para hacer INSERT a la base de datos,  
                    3 para cerrar base de datos,
                    4 para crear excel,
                    """))    
    #match case
    match num:
        case num if num == 1:
            #create
            database.createTable(logger)            
        case num if num == 2:
            #insert
            database.insert(logger)           
        case num if num == 3:
            database.closeConexion(logger) 
        case num if num == 4:
            #Crear excel
            excel = ReportExcel(logger)
        case _:
            logger.setMessage("Error",'error')
            print("Error, numero incorrecto") 



if(__name__ == '__main__'):
    main()