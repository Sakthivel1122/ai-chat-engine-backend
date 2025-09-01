from mongoengine import Document, DateTimeField
import datetime

class TimeStampedDocument(Document):
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    deleted_at = DateTimeField(null=True)

    meta = {
        'abstract': True  # This prevents a collection from being created for this base class
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)
