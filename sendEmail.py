import os
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def main():
        user='alexwind96@gmail.com'
        passwd='alecsandru'
                
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = user
        msg['Subject'] = 'Unauthorised login attempt at home!'

        body = 'An unknown user tried to authenticate at your home device, check attachment below'
               
        msg.attach(MIMEText(body,'plain'))
               
        list_of_files = glob.glob('/home/pi/FacialRecognition/Emails/*.jpg') #*=everythin that is .jpg
        latest_file = max(list_of_files, key=os.path.getctime)

        attachment = open(latest_file,'rb')
        file = MIMEBase('application', 'octet-stream')
        file.set_payload((attachment).read())
        encoders.encode_base64(file)
        file.add_header('Content-Disposition', "attachment; filename= "+ latest_file)

        msg.attach(file)
        Message = msg.as_string()

        print(latest_file)
        srv = smtplib.SMTP('smtp.gmail.com', 587)
        srv.starttls()
        srv.login(user,passwd)
                
                
        srv.sendmail(user, user, Message)
        srv.quit()
