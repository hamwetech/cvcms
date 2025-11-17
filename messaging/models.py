from django.db import models

from system.models import TimeStampMixin


class SMSLog(TimeStampMixin):
    phone = models.CharField(max_length=30)
    message = models.TextField()
    api_url = models.TextField()
    response_text = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)  # True = success

    class Meta:
        db_table = 'sms_log'
        verbose_name_plural = 'SMS Messaging'


    def __str__(self):
        return f"{self.phone} - {self.created_at}"
