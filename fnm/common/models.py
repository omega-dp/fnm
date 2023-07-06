from datetime import datetime

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
