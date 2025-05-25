from mongoengine import Document, StringField, DateTimeField, EmailField
from server.models import TimeStampedDocument

class User(TimeStampedDocument):
    username = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, max_length=128)
    role = StringField(required=True, choices=["user", "admin"], default="user")

    meta = {
        'collection': 'users'  # Specifies the collection name in MongoDB
    }

    @property
    def is_authenticated(self):
        return True