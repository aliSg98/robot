import os
from src.ConnexionPostgress import ConnexionPostgress
from src.ReportExcel import ReportExcel
from src.Logger import Logger
from dotenv import load_dotenv

def main():    
    cargarEnv()
    """Iniciar el logger"""
    logger = Logger()
    """Conectarse a la base de datos"""
    database = ConnexionPostgress()

    opcionesMatchCase(database,logger)    


def opcionesMatchCase(database,logger):
    path_xlsx = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot.xlsx"
    """Elegir si quieres crear la tabla o hacer un insert con los datos que quieras"""
    num = int(input("""Ingrese 1 para Crear tabla en base de datos, 
                    2 para hacer INSERT a la base de datos,  
                    3 para cerrar base de datos,
                    4 para crear excel vacio,
                    5 para añadir datos al excel,
                    6 crear robot en RobotSelenium,
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
        case num if num == 5:
            datos ={
                "Name_robot": ["ABC8273", "ABC82763", "ABC82673","AHJD77"],
                "Status_creation": ["DONE","DONE","WIP","FAIL"],
                "Status_pdf": ["DONE","DONE","WIP","FAIL"],
                "Path_pdf": ["/users/Ali","/users/Jorge","/users/Alex","users/Pedro"],
                "Status_final": ["DONE","DONE","WIP","Fail"]
            }
            ReportExcel.addColums(path_xlsx,'Robot1',datos)
        case _:
            logger.setMessage("Error",'error')
            print("Error, numero incorrecto") 

def cargarEnv():
    load_dotenv(r"C:\Users\nasudre\Desktop\Robot\ENV\.env")
    global url_robot,url_orders
    url_robot = os.getenv('URL_ROBOT')
    url_orders = os.getenv('URL_ORDERS')

if(__name__ == '__main__'):
    main()