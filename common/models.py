from django.db import models


class CommonModel(models.Model):
    is_active = models.BooleanField(verbose_name="활성 여부", default=True)
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="갱신일", auto_now=True)

    class Meta:
        abstract = True
