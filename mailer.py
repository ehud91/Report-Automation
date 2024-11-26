import logging
import os
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s", level=logging.INFO
)

SMPT_SERVER = os.environ.get("SMTP_SERVER")
PORT = os.environ.get("EMAIL_PORT")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

def send_email(to_email: str, subject: str, attachmet_name: str):
    """
    Send an email an attachment to the specified recipient.
    
    Args:
        to_email (str): The recipient's email address.
        subject (str): The subject of the email.
        attachment_name (str): The filename of the attachment.
    
    Note:
        This function assumes that the SMTP server requires TLS encryption.
    
    Raises:
        smtplib.SMTPException: If there is an issue with sending the email.
    """

    message = MIMEMultipart()
    message["From"] = EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    body = "Hi, there\n\nPlese find attached your report.\n\nThanks"

    message.attach(MIMEText(body, "plain"))

    with open(attachmet_name, "rb") as file:
        part = MIMEBase(
            "application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"            
        )
        part.set_payload(file.read())
    
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachmet_name}",
    )

    logging.info(f"Attaching {attachmet_name} to the email")
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP(SMPT_SERVER, PORT) as server:
        logging.info(f"Sending email to {to_email}")
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, text)
        logging.info(f"Successfully sent the email to {to_email}")
