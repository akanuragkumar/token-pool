import uuid as uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TokenPool(models.Model):
    """Token Pool model"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    assigned_to = models.BooleanField(default=False)
    expiry_time = models.DateTimeField(null=True)
    refresh_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'token_pool_collection'
        verbose_name = _('Token Pool Collection')
        verbose_name_plural = _('Token Pool Collections')

    def __str__(self):
        return self.uuid.__str__()
