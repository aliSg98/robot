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


@task
def robot_python():
    """Crear robot, crear pdf, hacer captura, crear pdf final con la captura dentro"""
    browser.configure(
        slowmo=100,
    )
    load_dotenv(r"C:\Users\nasudre\Desktop\Robot\ENV\.env")
    log = importLogger()
    open_robot_order_website(log)
    orders = get_orders(log)
    close_popup(log)
    close = 0        
    order_index = 0
    #poner aqui el numero de robots que queremos
    num_robot = 1
    total_orders = len(orders)
    try:
        while order_index < total_orders and num_robot > 0 and num_robot < total_orders:
            if close== 1:
                close_popup(log)
            order = orders[order_index]
            fill_the_form(order,log)
            time.sleep(3)
            order_number = order["Order number"]
            screenshot_robot(order_number,log)
            time.sleep(2)
            pdf_file = store_receipt_as_pdf(order_number,log)
            time.sleep(1)
            screenshot = screenshot_robot(order_number,log)
            embed_screenshot_to_pdf(screenshot, pdf_file, order_number,log)
            time.sleep(2)
            if num_robot > 1:
                click_other_robot(log)
                time.sleep(2)
                close = 1
                order_index +=1
                num_robot = num_robot - 1
            order_index +=1
            num_robot = num_robot - 1
            log.setMessage(f"Robot {order_number} creado", "info")
            continue           
    except Exception as exception:
            print(exception)
            log.setMessage("Error al crear el robot", "error")


"""Abrir pagina para hacer pedidos de robots"""
def open_robot_order_website(log):
    try:            
        browser.goto(os.getenv('URL_ROBOT'))
        log.setMessage("Abriendo pagina de creacion de robots", "info")
    except Exception:
        print("Error al abrir pagina de creacion de robots")
        log.setMessage("Error al abrir pagina de creacion de robots", "error")

"""Crear lista de diccionarios con los datos del csv orders.csv"""
def get_orders(log):
    http = HTTP()
    path_archivo = r"C:\Users\nasudre\Desktop\Robot\LOG\orders.csv"
    http.download(url=os.getenv('URL_ORDERS'), overwrite=True, target_file = path_archivo)

    archivo = path_archivo
    log.setMessage("Archivo orders.csv descargado correctamente", "info")
    """Read csv"""
    orders_list = []
    with open(archivo, 'r') as csvfichero:
            orders = csv.DictReader(csvfichero)                
            for row in orders:
                orders_list.append(row)

    return orders_list

"""Cerrar pop up"""
def close_popup(log):
    try:
        page = browser.page()
        page.click("button:text('OK')")
    except Exception as exception:
        print(f"Error al cerrar pop up{exception}")   
        log.setMessage("Error al cerrar pop up", "error")

"""Rellenar formulario con datos del csv"""
def fill_the_form(orders,log):
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

        return page.click('//*[@id="order" and @type="submit"]')
    
    except Exception as exception:
        print(f"Error al completar el formulario{exception}")
        log.setMessage("Error al completar el formulario", "error")

"""Hago screenshot del robot"""
def screenshot_robot(order_number,log):
    try:
        page = browser.page()
        page.screenshot(path=r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.png")
        screenshot = r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.png"
        log.setMessage("Captura del robot hecha", "info")
        return screenshot
    except Exception:
        print("Error al hacer screenshot del robot")
        log.setMessage("Error al hacer screenshot del robot", "error")

"""Creo pdf"""
def store_receipt_as_pdf(order_number,log):
    try:
        page = browser.page()
        time.sleep(3)
        results_html = page.locator("#receipt").inner_html()
        pdf = PDF()
        pdf.html_to_pdf(results_html, r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.pdf")
        pdf_final = r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.pdf"
        log.setMessage("Pdf creado", "info")
        return pdf_final
    except Exception:
        print("Error al crear pdf")
        log.setMessage("Error al crear pdf", "error")

"""Meto screenshot en pdf"""
def embed_screenshot_to_pdf(screenshot, pdf_file, order_number, log):
    try:
        pdf = PDF()
        pdf.open_pdf(pdf_file)
        pdf.add_watermark_image_to_pdf(
            image_path = screenshot,
            source_path = pdf_file,
            output_path=r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.pdf"

        )
        log.setMessage("Imagen introducida en pdf", "info")
        pdf.close_all_pdfs()
    except Exception:
        print("Error al introducir imagen en pdf")
        log.setMessage("Error al introducir imagen en pdf", "error")

def click_other_robot(log):
    page = browser.page()
    try:
        page.click('//*[@id="order-another" and @type="submit"]')
        log.setMessage("Creando otro robot", "info")
    except Exception:
        print("Error al hacer click para crear otro robot")
        log.setMessage("Error al hacer click para crear otro robot", "error")   


def importLogger():
    #path_src = r"C:\Users\nasudre\Desktop\Robot\src"
    carpeta_src = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(carpeta_src)
    from src import Logger
    log = Logger.Logger()
    return log

