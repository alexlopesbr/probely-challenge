from django.db import models


class Finding(models.Model):
    HTTP_METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
        ('OPTIONS', 'OPTIONS'),
        ('HEAD', 'HEAD'),
    ]

    target_id = models.IntegerField(unique=True)
    definition_id = models.TextField()
    scans = models.JSONField(default=list, blank=True)
    url = models.URLField()
    path = models.URLField()
    method = models.CharField(max_length=10, choices=HTTP_METHOD_CHOICES, default='INVALID')
