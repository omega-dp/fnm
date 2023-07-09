from datetime import datetime
from fnm.common.fields import DateTimeTzField
from fnm.utils.time_utils import local_now

from django.db import models


class BaseModel(models.Model):
    created_at = DateTimeTzField("update_at", default=local_now(), editable=False)
    updated_at = DateTimeTzField("update_at", default=local_now(), editable=False)

    class Meta:
        abstract = True
