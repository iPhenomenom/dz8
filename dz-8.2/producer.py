import pika
from faker import Faker
from mongoengine import connect
from contact import Contact


connect('mydb')

fake = Faker()

# Создаем подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='email_queue')

# Генерируем 100 фейковых контактов
for _ in range(100):
    fake_contact = Contact(full_name=fake.name(), email=fake.email())

    fake_contact.save()

    # Отправляем ID контакта в очередь RabbitMQ
    channel.basic_publish(exchange='', routing_key='email_queue', body=str(fake_contact.id))

# Закрываем подключение
connection.close()
