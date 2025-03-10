import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from decouple import config
import ssl
import os
from dotenv import load_dotenv

class Email:
    def __init__(self, receiver_email, excel_file, log_file, subject):
        self.receiver_email = receiver_email
        self.excel_file = excel_file
        self.log_file = log_file
        self.subject = subject



    def send_email(self):
        load_dotenv(r"C:\Users\nasudre\Desktop\Robot\ENV\.env")
        sender_email = 'alisopra98@gmail.com'
        password = os.getenv('PASSWORD_EMAIL')
        body = "Log y excel adjuntos"
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        #Crear el mensaje
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = self.receiver_email
        message['Subject'] = self.subject

        #Mensaje
        message.attach(MIMEText(body, 'plain'))

        #Adjuntar archivos
        logAdd = MIMEBase('application', "octet-stream")
        logAdd.set_payload(open(self.log_file, "r").read())
        encoders.encode_base64(logAdd)
        logAdd.add_header('Content-Disposition', 'attachment', filename="log.txt")
        message.attach(logAdd)

        excelAdd = MIMEBase('application', "octet-stream")
        excelAdd.set_payload(open(self.excel_file, "rb").read())
        encoders.encode_base64(excelAdd)
        excelAdd.add_header('Content-Disposition', 'attachment', filename="Robot.xlsx")
        message.attach(excelAdd)

        #Enviar correo
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)       
            server.starttls()
            server.login(sender_email,password)
            server.sendmail(sender_email, self.receiver_email, message.as_string())
            print("Email enviado")
        except Exception as e:
            print(f"Error al enviar correo: {e}")
        finally:
            server.quit()