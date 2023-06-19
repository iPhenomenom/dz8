from mongoengine import Document, StringField, EmailField, BooleanField

class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    message_sent = BooleanField(default=False)