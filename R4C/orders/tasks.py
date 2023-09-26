# tasks.py in your "orders" app
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os
import smtplib
from R4C.celery import app
from datetime import datetime, timedelta
from orders.models import Order
from robots.models import Robot
from orders.utils import send_notification

@app.task
def check_robot_availability():
    # Определите начальную и конечную даты для поиска роботов

    # Получите заказы, которые ожидают проверки
    orders = Order.objects.all()
    for order in orders:
        model, version = order.robot_serial.split('-')
        # Проверьте наличие робота в базе данных
        robot_exists = Robot.objects.filter(model=model, version=version).exists()
        logging.warning(robot_exists)
        if robot_exists:
            # Отправьте уведомление на email Customer о появлении робота
            text=f"""Добрый день!
Недавно вы интересовались нашим роботом модели {model}, версии {version}.
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"""
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = os.getenv('SMPT_PORT',default=587)
            smtp_username = os.getenv('SMPT_USERNAME')
            smtp_password = os.getenv('SMPT_PASSWORD')


            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = order.customer.email
            msg['Subject'] = 'Уведомление о наличии робота'


            body = text
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()

                # Авторизация на сервере
                server.login(smtp_username, smtp_password)

                # Отправка сообщения
                server.sendmail(smtp_username, order.customer.email, msg.as_string())

                # Закрытие соединения
                server.quit()

                logging.warning(f"Уведомление отправлено на {order.customer.email}")
            except Exception as e:
                logging.warning(f"Ошибка отправки уведомления: {str(e)}")

            # Удалите заказ из таблицы Order
            order.delete()
        else:
            # Отметьте заказ как проверенный
            order.save()
