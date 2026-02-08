from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
import string

class FileTransfer(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    code = models.CharField(max_length=6, unique=True, editable=False)
    expires_at = models.DateTimeField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                code = ''.join(random.choices(string.digits, k=6))
                if not FileTransfer.objects.filter(code=code).exists():
                    self.code = code
                    break
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.name} ({self.code})"
