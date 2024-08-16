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
    """Conectarse a la base de datos"""
    database = ConnexionPostgress()
    database.createTable(logger)    
    """Crear robot en robotFramework"""
    robotRPA = RobotFramework(url_robot,url_orders,robot_name,params.num_robots,logger,excel,database)
    robotRPA.createRobot()
    """Crear robot en selenium"""
    robotSelenium = RobotSelenium(url_robot,url_orders,robot_selenium,params.num_robots,logger,excel,database)
    robotSelenium.createRobot()
    """Combinar pdf de las 2 versiones"""
    pdfsRpa = robotRPA.getPath_pdf()
    pdfsSelenium = robotSelenium.getPath_pdf()
    pdfCombinado = PdfRpaSelenium(pdfsRpa,pdfsSelenium,logger).pdf_combination()
    """Poner colores en el exel"""
    excel.changeColor()
    """Cerrar conexion a base de datos"""
    database.closeConexion(logger)        
    """Enviar Mail"""
    email = Email(params.email, params.xlsx, params.log,"Email con excel, y los logs").send_email()
    
    

    #opcionesMatchCase(database,logger,excel,url_robot,url_orders,robot_name)    


def opcionesMatchCase(database,logger,excel,url_robot,url_orders,robot_name,robot_selenium):    
    """Elegir si quieres crear la tabla o hacer un insert con los datos que quieras"""
    num = int(input("""Ingrese 1  para crear excel,
                    2 para añadir colores al excel,
                    3 para enviar email,
                    4 para crear robot en selenium,
                    5 para crear robot en Rpa
                    """))    
    #match case
    match num:        
        case num if num == 1:
            #Crear excel
            excel = ReportExcel(params.xlsx,logger)
        case num if num == 2:
            excel.changeColor()
        case num if num == 3:
            #Enviar email
            email = Email(params.email, params.xlsx, params.log,"Email con excel, y los logs").send_email()
        case num if num == 4:
            robotSelenium = RobotSelenium(url_robot,url_orders,robot_selenium,params.num_robots,logger,excel,database)
            robotSelenium.createRobot()
        case num if num == 5:    
            robotRPA = RobotFramework(url_robot,url_orders,robot_name,params.num_robots,logger,excel,database)
            robotRPA.createRobot()
        case _:
            logger.setMessage("Error",'error')
            print("Error, numero incorrecto") 



if(__name__ == '__main__'):
    main()