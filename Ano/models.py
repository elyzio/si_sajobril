from django.db import models

class Ano(models.Model):
    ano = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
      return self.ano