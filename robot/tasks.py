from robocorp.tasks import task
from robocorp import browser, vault
from RPA.HTTP import HTTP
from RPA.Tables import Tables
import csv
from RPA.PDF import PDF
from RPA.Archive import Archive

@task
def robot_python():
    """Crear robot, crear pdf, hacer captura, crear pdf final con la captura dentro"""
    browser.configure(
        slowmo=100,
    )
    open_robot_order_website()
    orders = get_orders()
    close_annoying_modal()    
    for order in orders:
        fill_the_form(order)
        order_number = order["Order number"]
        break
    screenshot_robot(order_number)
    pdf_file = store_receipt_as_pdf(order_number)
    screenshot = screenshot_robot(order_number)
    embed_screenshot_to_pdf(screenshot, pdf_file, order_number)

"""Abrir pagina para hacer pedidos de robots"""
def open_robot_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

"""Crear lista de diccionarios con los datos del csv orders.csv"""
def get_orders():
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

    archivo = "orders.csv"
    """Read csv"""
    orders_list = []
    with open(archivo, 'r') as csvfichero:
            orders = csv.DictReader(csvfichero)                
            for row in orders:
                orders_list.append(row)

    return orders_list

"""Cerrar pop up"""
def close_annoying_modal():
    page = browser.page()
    page.click("button:text('OK')")

"""Rellenar formulario con datos del csv"""
def fill_the_form(orders):
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

"""Hago screenshot del robot"""
def screenshot_robot(order_number):
    page = browser.page()
    page.screenshot(path=r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.png")
    screenshot = r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.png"
    return screenshot

"""Creo pdf"""
def store_receipt_as_pdf(order_number):
    page = browser.page()
    results_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(results_html, r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.pdf")
    pdf_final = r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.pdf"
    return pdf_final

"""Meto screenshot en pdf"""
def embed_screenshot_to_pdf(screenshot, pdf_file, order_number):
    pdf = PDF()
    pdf.open_pdf(pdf_file)
    pdf.add_watermark_image_to_pdf(
        image_path = screenshot,
        source_path = pdf_file,
        output_path=r"C:\Users\nasudre\Desktop\Robot\LOG"+f"\Robot-{order_number}.pdf"

    )
    pdf.close_all_pdfs()
