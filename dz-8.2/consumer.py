import pika
from mongoengine import connect
from contact import Contact
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


connect('mydb')

def send_email(to_email):
    from_email = "your_email@gmail.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Тема письма"

    body = "Содержание письма"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def callback(ch, method, properties, body):

    contact_id = body.decode()


    contact = Contact.objects(id=contact_id).first()

    if contact is not None:

        send_email(contact.email)


        contact.message_sent = True
        contact.save()


    ch.basic_ack(delivery_tag=method.delivery_tag)

# Создаем подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Объявляем очередь, которую будет слушать consumer
channel.queue_declare(queue='email_queue')

# Настраиваем consumer
channel.basic_consume(queue='email_queue', on_message_callback=callback)

# Начинаем слушать очередь
channel.start_consuming()
