import sys
import os
from src.ConnexionPostgress import ConnexionPostgress
from src.ReportExcel import ReportExcel
from src.Logger import Logger
from dotenv import load_dotenv
from src.Email import Email
from src.RobotSelenium import RobotSelenium
from src.RobotFramework import RobotFramework
from src.PdfRpaSelenium import PdfRpaSelenium
from ParamsRobot import params
#Agregar directorio de paquetes
sys.path.append(r'C:\Users\nasudre\AppData\Local\Programs\Python\Python310\Lib\site-packages')
def main():  
    """Cargar .env"""
    load_dotenv(r"C:\Users\nasudre\Desktop\Robot\ENV\.env")
    robot_name = os.getenv('ROBOT_NAME')
    robot_selenium = os.getenv('ROBOT_NAME_SELENIUM')
    url_robot = os.getenv('URL_ROBOT')
    url_orders = os.getenv('URL_ORDERS')

    """Iniciar el logger"""
    logger = Logger()
    """Excel"""
    excel = ReportExcel(params.xlsx,logger)    
    #excel.add_data(datos)
    #excel.add_update_row_data(['Pepas','DONE','Fail','/users/ali','FAIL'])
    """Crear robot en selenium"""
    robotSelenium = RobotSelenium(url_robot,url_orders,robot_selenium,params.num_robots,logger,excel)
    robotSelenium.createRobot()
    """Crear robot en robotFramework"""
    robotRPA = RobotFramework(url_robot,url_orders,robot_name,params.num_robots,logger,excel)
    robotRPA.createRobot()
    """Combinar pdf de las 2 versiones"""
    pdfCombinado = PdfRpaSelenium(robotSelenium.getPath_pdf(),robotRPA.getPath_pdf()).pdfCombination()

    excel.changeColor()
    """Conectarse a la base de datos"""
    database = ConnexionPostgress()
    database.createTable(logger)
    database.closeConexion(logger)    
    
    """Mail"""
    #email = Email(params.email, params.xlsx, params.log,"Email con excel, y los logs").send_email()
    
    

    #opcionesMatchCase(database,logger,excel,url_robot,url_orders,robot_name)    


def opcionesMatchCase(database,logger,excel,url_robot,url_orders,robot_name):    
    """Elegir si quieres crear la tabla o hacer un insert con los datos que quieras"""
    num = int(input("""Ingrese 1 para Crear tabla en base de datos, 
                    2 para hacer INSERT a la base de datos,  
                    3 para cerrar base de datos,
                    4 para crear excel,
                    5 para añadir datos al excel,
                    6 para añadir colores al excel,
                    7 para enviar email,
                    8 para crear robot en selenium,
                    9 para crear robot en Rpa
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
            datos ={
                    "Name_robot": [],
                    "Status_creation": [],
                    "Status_pdf": [],
                    "Path_pdf": [],
                    "Status_final": []
                }
            excel.create_excel(datos)

        case num if num == 5:
            datos ={
                "Name_robot": ["Acc665"],
                "Status_creation": ["WIP"],
                "Status_pdf": ["WIP"],
                "Path_pdf": ["/users/ali"],
                "Status_final": ["WIP"]
            }
            excel.add_data(datos)
        case num if num == 6:
            excel.changeColor()
        case num if num == 7:
            #Enviar email
            email = Email(params.email, params.xlsx, params.log,"Email con excel, y los logs").send_email()
        case num if num == 8:
            robotSelenium = RobotSelenium(url_robot,url_orders,robot_name,params.num_robots,logger).createRobot()
        case num if num == 9:    
            robotRPA = RobotFramework(url_robot,url_orders,robot_name,params.num_robots,logger).createRobot()
        case _:
            logger.setMessage("Error",'error')
            print("Error, numero incorrecto") 



if(__name__ == '__main__'):
    main()