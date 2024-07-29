import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
from reportlab.pdfgen import canvas
from PIL import Image
import os

class RobotSelenium():
    def __init__(self,url,url_orders,name_robot,logger):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.url=url
        self.url_orders=url_orders
        self.name_robot=name_robot
        self.logger=logger        

    def open_robot_order_website(self):        
        self.driver.get(self.url)

    def get_orders(self):
        path_archivo = r"C:\Users\nasudre\Desktop\Robot\LOG\orders.csv"
        if(os.path.exists(path_archivo)):
            with open(path_archivo, 'r') as csvfichero:
                orders = csv.DictReader(csvfichero) 
                orders_list = []               
                for row in orders:
                    orders_list.append(row)
            return orders_list
        else:
            self.driver.get(self.url_orders)     
            time.sleep(2)     
        

    def close_popup(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
            ).click()
        except TimeoutException:
            print("Ningun pop aparecio")

    def fill_the_form(self, order):
        try:
            Select(self.driver.find_element(By.ID, 'head')).select_by_visible_text(order['Head'])

            body_options = self.driver.find_elements(By.NAME,"body")
            for option in body_options:
                if option.get_attribute('value') == order['Body']:
                    option.click()
                    break

            legs = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter the part number for the legs']")
            legs.clear()
            legs.send_keys(order['Legs'])

            address = self.driver.find_element(By.ID, 'address')
            address.clear()
            address.send_keys(order['Address'])

            self.driver.find_element(By.XPATH, '//*[@id="order" and @type="submit"]').click()

        except Exception as e:
            print(f"Error al completar el formulario: {e}")

    def screenshot_robot(self, order_number):
        screenshot_path = f"C:\\Users\\nasudre\\Desktop\\Robot\\LOG"+f"\\Robot-{order_number}.png"
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path

    def store_receipt_as_pdf(self, order_number):
        pdf_path = f"C:\\Users\\nasudre\\Desktop\\Robot\\LOG"+f"\\Robot-{order_number}.pdf"
        c = canvas.Canvas(pdf_path)
        receipt_html = self.driver.find_element(By.ID, 'receipt').get_attribute('outerHTML')
        c.drawString(100, 750, receipt_html)
        c.save()
        return pdf_path

    def embed_screenshot_to_pdf(self, screenshot, order_number):
        pdf_path = f"C:\\Users\\nasudre\\Desktop\\Robot\\LOG"+f"\\Robot-{order_number}.pdf"
        c = canvas.Canvas(pdf_path)
        c.drawImage(screenshot, 15, 15, width=500, height=750)
        c.save()

    def click_other_robot(self):
        self.driver.find_element(By.XPATH, '//*[@id="order-another" and @type="submit"]').click()

    def create_robot(self):
        url_robot=os.getenv('URL_ROBOT')
        url_orders = os.getenv('URL_ORDERS')
        self.open_robot_order_website(url_robot)
        orders = self.get_orders(url_orders)
        self.close_popup()
        close = 0        
        order_index = 0
        num_robot = 1
        total_orders = len(orders)

        while order_index < total_orders and num_robot > 0 and num_robot < total_orders:
            if close== 1:
                self.close_popup()
            order = orders[order_index]
            self.fill_the_form(order)
            time.sleep(3)
            order_number = order["Order number"]
            self.screenshot_robot(order_number)
            time.sleep(2)
            pdf_file = self.store_receipt_as_pdf(order_number)
            time.sleep(1)
            screenshot = self.screenshot_robot(order_number)
            self.embed_screenshot_to_pdf(screenshot, pdf_file, order_number)
            time.sleep(2)
            if num_robot > 1:
                self.click_other_robot()
                time.sleep(2)
                close = 1
                order_index +=1
                num_robot = num_robot - 1
            order_index +=1
            num_robot = num_robot - 1
            continue      
        self.driver.quit()
