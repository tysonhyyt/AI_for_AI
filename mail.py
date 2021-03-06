import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
# import logging

# date and time
import time
from datetime import datetime


def sendReport(imagedir, processName, receiver, cc = []):
    # show the time which the email is sent
    date = datetime.now()
    filedate = date.strftime('%d.%m.%Y %H:%M:%S')
    date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    # Email Setting (Sender, Receiver, CC, Password)
    #     PATH_1= os.getcwd() +"\\setting.txt" #need to change directory to the share folder after this
    #     a =[0]*4
    #     with open(PATH_1) as f:
    #         for i in range(4):
    #             f.readline()
    #             str = f.readline()
    #             a[i] = str.strip("\n"+"\t")

    sender_email = "wid180036@siswa.um.edu.my"
    receiver_email = receiver.split(',')
    cc_email = cc.split(',')
    password = "wid3df0aef2"

    message = MIMEMultipart("mixed")
    message["Subject"] = processName + " - MSG AutoML Report Generated by Autobot"
    message["From"] = sender_email
    message["To"] = "; ".join(receiver_email)
    message["Cc"] = "; ".join(cc_email)

    # write the HTML part
    html = """    <html>
    <body>
        <p><h1><u> MSG AutoML - {processName} Process Completed </u></h1><p>
        <p><strong> Time Report Generated:  {date} </strong></p>
        <p>Dear All,</p>
        <p>&nbsp;&nbsp;&nbsp;&nbsp;The MSG AutoML process is completed.</p>
        <p>[Don't reply to this message. This is an automated email generated by Autobot.]</p>
        <p></p>
    </body>
    </html>
    """.format(date=date, processName=processName)

    filedir = os.path.dirname(imagedir)
    files = os.listdir(imagedir)
    for file in files:
        f = file
        filePath = imagedir + "\\" + file
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(filePath, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=f)
        message.attach(part)

    part1 = MIMEText(html, "html")
    message.attach(part1)

    # Create secure connection with server and send email
    smtp_server = "smtp.gmail.com"
    port = 587
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

