from robocorp.tasks import task
from RPA.Excel.Files import Files
from robocorp import browser

from RPA.HTTP import HTTP

@task
def robot_python():
    """Insert the sales data for the week and export it as a PDF"""
    browser.configure(
        slowmo=100,
    )
    createExcel()
    
"""Creacion excel"""
def createExcel():
    lib = Files()
    lib.create_workbook(path=r"C:\Users\nasudre\Desktop\Robot\robot\output\robot.xlsx", fmt="xlsx")
    Worksheet_Data = {
    "Name_robot": ["ABC8273", "ABC82763", "ABC82673"],
    "Status_creation": ["DONE","DONE","WIP"],
    "Status_pdf": ["DONE","DONE","WIP"],
    "Path_pdf": ["/users/Ali","/users/Jorge","/users/Alex"],
    "Status_final": ["DONE","DONE","WIP"]
    }    
    lib.create_worksheet(name="robot.xlsx",content=Worksheet_Data,header=True)
    lib.save_workbook()
