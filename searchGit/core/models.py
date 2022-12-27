from django.db import models

class Repository(models.Model):
  repositorio = models.CharField(
    max_length=120,
    null=False,
    blank=False)