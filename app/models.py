import os.path

from django.db import models
import uuid


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("uploads/files", filename)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FileManagementModel(BaseModel):
    name = models.CharField(max_length=80, blank=False, null=False)
    file = models.FileField(upload_to=upload_to, blank=False, null=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
