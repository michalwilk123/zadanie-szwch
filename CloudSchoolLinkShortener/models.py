import secrets

from django.db import models


class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=2048)
    hash = models.CharField(max_length=8, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = secrets.token_urlsafe(8)
        super().save(*args, **kwargs)
