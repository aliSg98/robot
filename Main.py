import os
from src.ConnexionPostgress import ConnexionPostgress
from src.ReportExcel import ReportExcel
from src.Logger import Logger
from dotenv import load_dotenv
from src.Email import Email
from src.RobotSelenium import RobotSelenium

def main():    
    """Iniciar el logger"""
    logger = Logger()
    """Conectarse a la base de datos"""
    database = ConnexionPostgress()

    path_xlsx = r"C:\Users\nasudre\Desktop\Robot\LOG\Robot.xlsx"

    excel = ReportExcel(path_xlsx,logger)    

    opcionesMatchCase(database,logger,excel)    


def opcionesMatchCase(database,logger,excel):    
    """Elegir si quieres crear la tabla o hacer un insert con los datos que quieras"""
    num = int(input("""Ingrese 1 para Crear tabla en base de datos, 
                    2 para hacer INSERT a la base de datos,  
                    3 para cerrar base de datos,
                    4 para crear excel,
                    5 para añadir datos al excel,
                    6 para añadir colores al excel,
                    7 para enviar email,
                    8 para crear robot en selenium,
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
                "Name_robot": ["AFF665"],
                "Status_creation": ["Fail"],
                "Status_pdf": ["DONE"],
                "Path_pdf": ["/users/admin"],
                "Status_final": ["wip"]
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
            email = Email("nur-ali.sudre@soprasteria.com", r"C:\Users\nasudre\Desktop\Robot\LOG\Robot.xlsx",r"C:\Users\nasudre\Desktop\Robot\LOG\log.txt","Email con excel, y los logs").send_email()
        case num if num == 8:
            robot = RobotSelenium()
            
        case _:
            logger.setMessage("Error",'error')
            print("Error, numero incorrecto") 


if(__name__ == '__main__'):
    main()