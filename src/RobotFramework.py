from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
import csv
from RPA.PDF import PDF
from RPA.Archive import Archive
from RPA.Browser import Browser
import time
import sys
import os
from dotenv import load_dotenv
class RobotFramework():
    def __init__(self,url,url_orders,name_robot,numRobots,logger,excel):
        self.url=url
        self.url_orders = url_orders
        self.name_robot = name_robot
        self.numRobots = numRobots   
        self.logger = logger 
        self.excel = excel
        self.path_pdf = None

    """Crear robot, crear pdf, hacer captura, crear pdf final con la captura dentro"""
    def createRobot(self):        
        browser.configure(
            slowmo=100,
        )
        try:
            self.open_robot_order_website()
            orders = self.get_orders()  
            order_number = 0
            pdf_file = ""
            for order_index in range(self.numRobots):
                order = orders[order_index]
                time.sleep(1)
                self.close_popup()
                time.sleep(1)
                self.fill_the_form(order)
                time.sleep(1)
                order_number = order["Order number"]
                time.sleep(3)
                self.screenshot_robot(order_number,pdf_file)
                time.sleep(2)
                pdf_file = self.store_receipt_as_pdf(order_number,pdf_file)
                time.sleep(1)
                screenshot = self.screenshot_robot(order_number,pdf_file)
                time.sleep(1)                
                self.embed_screenshot_to_pdf(screenshot, pdf_file, order_number)
                time.sleep(1)                                
        except Exception:
                print("Error al crear el robot")
                self.logger.setMessage("Error al crear el robot", "error")
                self.excel.add_update_row_data([f"Robot_{order_number}","FAIL","FAIL",str(pdf_file),"FAIL"])
        
    """Abrir pagina para hacer pedidos de robots"""
    def open_robot_order_website(self):
        try:            
            browser.goto(self.url)
            self.logger.setMessage("Abriendo pagina de creacion de robots", "info")
        except Exception:
            print("Error al abrir pagina de creacion de robots")
            self.logger.setMessage("Error al abrir pagina de creacion de robots", "error")

    """Crear lista de diccionarios con los datos del csv orders.csv"""
    def get_orders(self):
        http = HTTP()
        path_archivo = r"C:\Users\nasudre\Desktop\Robot\LOG\orders.csv"
        http.download(url=self.url_orders, overwrite=True, target_file = path_archivo)

        archivo = path_archivo
        self.logger.setMessage("Archivo orders.csv descargado correctamente", "info")
        """Read csv"""
        orders_list = []
        with open(archivo, 'r') as csvfichero:
                orders = csv.DictReader(csvfichero)                
                for row in orders:
                    orders_list.append(row)

        return orders_list

    """Cerrar pop up"""
    def close_popup(self):
        try:
            page = browser.page()
            page.click("button:text('OK')")
        except Exception as exception:
            print(f"Error al cerrar pop up{exception}")   
            self.logger.setMessage("Error al cerrar pop up", "error")

    """Rellenar formulario con datos del csv"""
    def fill_the_form(self,orders):
        try:
            """orders es una lista de diccionarios"""
            page = browser.page()
            page.select_option("#head",orders['Head'])
            
            """body"""
            botones = page.locator("input[type='radio']")
            for boton in botones.all():
                """ver el valor del boton actual"""
                opcion = boton.evaluate("element => element.value")
                if opcion == orders["Body"]:
                    boton.click()
                    break
            
            """Legs"""
            page.fill("xpath=//input[@placeholder='Enter the part number for the legs']", orders['Legs'])
            """Address"""
            page.fill("#address", orders["Address"])
            time.sleep(3)

            page.click('//*[@id="order" and @type="submit"]')
        
        except Exception as exception:
            print(f"Error al completar el formulario{exception}")
            self.logger.setMessage("Error al completar el formulario", "error")

    """Hago screenshot del robot"""
    def screenshot_robot(self,order_number,pdf_file):
        try:
            page = browser.page()
            page.screenshot(path=r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\{self.name_robot}{order_number}.png")
            time.sleep(2)
            screenshot = r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\{self.name_robot}{order_number}.png"
            self.logger.setMessage("Captura del robot hecha", "info")
            return screenshot
        except Exception:
            print("Error al hacer screenshot del robot")
            self.logger.setMessage("Error al hacer screenshot del robot", "error")
            self.excel.add_update_row_data([f"Robot_{order_number}","FAIL","FAIL",str(pdf_file),"FAIL"])

    """Creo pdf"""
    def store_receipt_as_pdf(self,order_number,pdf_file):
        try:
            page = browser.page()
            time.sleep(3)
            results_html = page.locator("#receipt").inner_html()
            pdf = PDF()
            pdf.html_to_pdf(results_html, r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\{self.name_robot}{order_number}.pdf")
            pdf_final = r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\{self.name_robot}{order_number}.pdf"
            self.logger.setMessage("Pdf creado", "info")
            return pdf_final
        except Exception:
            print("Error al crear pdf")
            self.logger.setMessage("Error al crear pdf", "error")
            self.excel.add_update_row_data([f"Robot_{order_number}","FAIL","FAIL",str(pdf_file),"FAIL"])

    """Meto screenshot en pdf"""
    def embed_screenshot_to_pdf(self,screenshot, pdf_file, order_number):
        try:
            pdf = PDF()
            pdf.open_pdf(pdf_file)
            pdf.add_watermark_image_to_pdf(
                image_path = screenshot,
                source_path = pdf_file,
                output_path=r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\{self.name_robot}{order_number}.pdf"

            )
            self.logger.setMessage("Imagen introducida en pdf", "info")            
            time.sleep(3)
            self.path_pdf=pdf_file
            time.sleep(1)
            self.logger.setMessage(f"Robot_{order_number} creado en RPA", "info") 
            self.excel.add_update_row_data([f"Robot_{order_number}","DONE","DONE",str(pdf_file),"DONE"])
            pdf.close_all_pdfs()
            self.click_other_robot()
        except Exception:
            print("Error al introducir imagen en pdf")
            self.logger.setMessage("Error al introducir imagen en pdf", "error")
            self.excel.add_update_row_data([f"Robot_{order_number}","FAIL","FAIL",str(pdf_file),"FAIL"])

    def click_other_robot(self):
        page = browser.page()
        try:
            page.click('//*[@id="order-another" and @type="submit"]')
            self.logger.setMessage("Creando otro robot", "info")
        except Exception:
            print("Error al hacer click para crear otro robot")
            self.logger.setMessage("Error al hacer click para crear otro robot", "error")

    def getPath_pdf(self):
        return self.path_pdf
