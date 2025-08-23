from django.db import models
from departamento.models import *
#from moras.models import *
#from vasinasaun.models import *

class classe(models.Model):
	#code_classe=models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	Departamento = models.ForeignKey(departamento, on_delete=models.CASCADE,null=True,related_name="ClassDepartamento")
	
	
	def __str__(self):
		template = '{0.classe}'
		return f"{self.name} - {self.Departamento}"
