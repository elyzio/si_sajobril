from django.db import models
from Classe.models import *
#from moras.models import *
#from vasinasaun.models import * 

class turma(models.Model):
	# code_turma=models.CharField(max_length=15)
	Turma = models.CharField(max_length=15)
	classe = models.ForeignKey(classe, on_delete=models.CASCADE,null=True,related_name="TurmaClass")
	
	def __str__(self):
		template = '{0.Turma}, {0.classe}'
		return f"{self.Turma},{self.classe} "
