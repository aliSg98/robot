import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import fitz
from PIL import Image
import os
from xhtml2pdf import pisa

class RobotSelenium():
    def __init__(self,url,url_orders,name_robot,numRobots,logger,excel):
        self.driver = self.configure_chrome_driver()
        self.url=url
        self.url_orders=url_orders
        self.name_robot=name_robot
        self.numRobots = numRobots   
        self.logger = logger
        self.excel = excel
        self.path_pdf= None

    """Abrir pagina para hacer pedidos de robots"""
    def open_browser(self):
        try: 
            self.driver.get(self.url)
            self.driver.maximize_window()
        except Exception:
            print("Error al abrir pagina de creacion de robots")  
            self.logger.setMessage("Error al abrir pagina de creacion de robots", "error") 

    """Configurar el driver, donde van las descargas"""
    def configure_chrome_driver(self):
        driverOptions = webdriver.ChromeOptions()
        # Especificar la carpeta de descargas en lugar de un archivo específico
        path = r"C:\Users\nasudre\Desktop\Robot\LOG"
        prefs = {
            "download.default_directory": path,
            "download.prompt_for_download": False,
            "directory_upgrade": True
        }
        driverOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=driverOptions)
        return driver

    """Cerrar pop up que aparece al abrir la pagina de robots"""
    def close_PopUP(self):
        try:
            #Esperar como maximo 10 segundos
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']")))
            button.click()
            time.sleep(1)
            print("Pop-up cerrado correctamente")
            self.logger.setMessage("Pop-up cerrado correctamente", "info")
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error al cerrar pop-up: {e}")

    """Crear lista datos del csv orders.csv"""
    def get_orders(self):
        path = f"C:\\Users\\nasudre\\Desktop\\Robot\\LOG\\orders.csv"
        if not os.path.isfile(path):
            self.driver.get(self.url_orders)
            
        orders_list = []
        time.sleep(3)
        try:
            with open(path, mode='r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    orders_list.append(row)
        except FileNotFoundError:
            print(f"El archivo {path} no se encontró.")
            self.logger.setMessage(f"El archivo {path} no se encontró.", "error")
        except Exception as e:
            print(f"Se produjo un error al leer el archivo CSV: {e}")
            self.logger.setMessage(f"Se produjo un error al leer el archivo CSV: {e}", "error")
        
        return orders_list

    """Rellenar formulario con datos del csv"""
    def fill_the_form(self, row, pdf_file):
        try:
            wait = WebDriverWait(self.driver, 10)             
            # Head
            head = Select(self.driver.find_element(By.XPATH,"//select[@id='head']"))
            head.select_by_value(row["Head"])  
            # Body
            radio_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio']")))
            for radio_button in radio_buttons:
                value = radio_button.get_attribute("value")
                if value == row['Body']:
                    radio_button.click()
                    break
            # legs
            legs = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter the part number for the legs']")))
            legs.send_keys(row['Legs'])
            time.sleep(1)
            # Dirección
            address = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='address']")))
            address.send_keys(row['Address'])  
            time.sleep(2)       
            # Hacer clic en el botón de enviar
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="order" and @type="submit"]'))).click()

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error en el formulario: {e}")
            self.logger.setMessage(f"Error en el formulario: {e}", "error")
            self.excel.add_update_row_data([f"{self.name_robot}{row}","FAIL","FAIL",str(pdf_file),"FAIL"])


    """Hacer screenshot del robot"""
    def get_image(self,order,pdf_file):
        try:
            # Esperar a que este presente el elemento
            wait = WebDriverWait(self.driver, 10)
            receipt_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//h3[normalize-space()='Receipt']")))
            
            # Definir la ruta para guardar la imagen
            path = f"C:\\Users\\nasudre\\Desktop\\Robot\\LOG\\"
            filename = f"{self.name_robot}{order}.png"
            file_path = path + filename
            
            # screenshot
            self.driver.save_screenshot(file_path)
            
            # Retorna captura de pantalla
            return file_path
        except TimeoutException:
            print("Time out")
            self.logger.setMessage("Time oup, screenshot", "error")
        except Exception as e:
            print(f"Error al hacer captura: {e}")
            self.logger.setMessage(f"Error al hacer captura: {e}", "error")
            self.excel.add_update_row_data([f"{self.name_robot}{order}","FAIL","FAIL",str(pdf_file),"FAIL"])

    """Hacer pdf, y meter la imagen del robot"""
    def getPdf(self,img,order):
        try:
            wait = WebDriverWait(self.driver, 10)
            receipt_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='receipt']")))
            time.sleep(1)
            # Definir la ruta para el archivo PDF
            path = f"C:\\Users\\nasudre\\Desktop\\Robot\\LOG\\"
            pdf_filename = f"{self.name_robot}{order}.pdf"
            pdf_filename_excel = f"C:\\Users\\nasudre\\Desktop\\Robot\\LOG\\{self.name_robot}{order}.pdf"
            pdf_path = path + pdf_filename

            #Abrir pdf en escritura binaria
            with open(pdf_path, "wb") as pdf_file:
                #convierte el html en pdf
                status = pisa.CreatePDF(receipt_element.get_attribute("innerHTML"), dest=pdf_file)
                print(status.err)

            # Abrir el archivo PDF y añadir la imagen
            with fitz.open(pdf_path) as pdf_document:
                first_page = pdf_document[0]
                image_rect = fitz.Rect(0, 300, 750, 600)
                first_page.insert_image(image_rect, filename=img)
                pdf_document.saveIncr()
            time.sleep(1)
            self.logger.setMessage(f"{self.name_robot}{order} creado en Selenium", "info") 
            self.excel.add_update_row_data([f"{self.name_robot}{order}","DONE","DONE",pdf_filename_excel,"DONE"])  
            time.sleep(3)
            self.path_pdf=pdf_filename_excel
            # Ordenar otro robot
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//button[@id='order-another']").click()
            time.sleep(1)
            return pdf_path
        except Exception as e:
            print(f"Error al generar el PDF: {e}")
            self.logger.setMessage(f"Error al generar el PDF: {e}", "error")
            self.excel.add_update_row_data([f"{self.name_robot}{order}","FAIL","FAIL",str(pdf_filename),"FAIL"])

    """Tarea final que llama a las demas funciones y crea el robot"""
    def createRobot(self):
        try:
            pdf_file = ""
            order_number = 0
            orders = self.get_orders()
            time.sleep(1)
            self.open_browser()
            for order_index in range(self.numRobots):                
                order = orders[order_index]
                time.sleep(1)          
                self.close_PopUP()
                time.sleep(1)
                order_number = order["Order number"]
                time.sleep(2)
                self.fill_the_form(order,pdf_file)             
                time.sleep(2)
                img = self.get_image(order_number,pdf_file)
                time.sleep(1) 
                pdf_file = self.getPdf(img,order_number)
                time.sleep(1)                
        except Exception:
            print("Error al crear el robot")
            self.logger.setMessage("Error al crear el robot", "error")
            if order_index > 0 :
                self.excel.add_update_row_data([f"{self.name_robot}{order_index}","FAIL","FAIL",str(pdf_file),"FAIL"])
        finally:
            self.driver.close()

    def getPath_pdf(self):
        return self.path_pdf
    
    
    
    
    
    