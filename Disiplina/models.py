from django.db import models
#from aimoruk.models import *
#from moras.models import *
#from vasinasaun.models import *

class diciplina(models.Model):
	code_dics = models.CharField(max_length=15, null=True, blank=True, verbose_name="codigo de disiplina")
	Diciplina = models.CharField(max_length=100, null=True, blank=True)
	
	
	def __str__(self):
		template = '{0.Diciplina}'
		return template.format(self)
