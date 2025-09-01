from mongoengine import Document, StringField, DateTimeField, EmailField
from server.models import TimeStampedDocument

class User(TimeStampedDocument):
    username = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=128, null=True)
    role = StringField(required=True, choices=["user", "admin"], default="user")
    provider = StringField(choices=["google"], null=True)
    provider_id = StringField(null=True)

    meta = {
        'collection': 'users'  # Specifies the collection name in MongoDB
    }

    @property
    def is_authenticated(self):
        return True
