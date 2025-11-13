from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class UserStampedModel(models.Model):
    """
    Adds automatic user and timestamp fields to models.
    """

    create_by = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        editable=False
    )
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True