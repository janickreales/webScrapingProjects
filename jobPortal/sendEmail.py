#https://realpython.com/python-send-email/  
#https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151

import sys
import time
import smtplib
import ssl
# from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


email_sender = ''
email_password = ''
email_receiver = ''

subject = f'Vacantes de empleo para {sys.argv[1]}'
body = f"""Vacantes de empleo para hoy: {time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())}

            Ver archivo adjunto
            """


# em = EmailMessage()
em = MIMEMultipart("alternative")
em['From'] = email_sender
em['To'] = email_receiver
em["Bcc"] = ''
em['Subject'] = subject
# em.set_content(body)

# Add body to email
em.attach(MIMEText(body, "plain"))


filenames = sys.argv[2].split(',')
filenames = [file for file in filenames if 'vacante' in file]
for filename in filenames:
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    em.attach(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename.split('/')[-1]}",
    )

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender,email_receiver,em.as_string())