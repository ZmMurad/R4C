import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_notification(recipient_email, message):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMPT_PORT',default=587)
    smtp_username = os.getenv('SMPT_USERNAME')
    smtp_password = os.getenv('SMPT_PASSWORD')


    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Subject'] = 'Уведомление о наличии робота'


    body = message
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Авторизация на сервере
        server.login(smtp_username, smtp_password)

        # Отправка сообщения
        server.sendmail(smtp_username, recipient_email, msg.as_string())

        # Закрытие соединения
        server.quit()

        logging.warning(f"Уведомление отправлено на {recipient_email}")
    except Exception as e:
        logging.warning(f"Ошибка отправки уведомления: {str(e)}")
