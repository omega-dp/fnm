from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

from fnm.common.models import BaseModel
from fnm.media.enums import FileUploadStorage
from fnm.media.utils import file_generate_upload_path
from fnm.users.models import User


class Media(BaseModel):
    file = models.FileField(upload_to=file_generate_upload_path, blank=True, null=True)

    original_file_name = models.TextField()

    file_name = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=255)

    # As a specific behavior,
    # We might want to preserve media after the uploader has been deleted.
    # In case you want to delete the media too, use models.CASCADE & drop the null=True
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    upload_finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self):
        """
        We consider a file "valid" if the the datetime flag has value.
        """
        return bool(self.upload_finished_at)

    @property
    def url(self):
        if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.S3:
            return self.file.url

        return f"{settings.APP_DOMAIN}{self.file.url}"

    class Meta:
        db_table = "Media"
