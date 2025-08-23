from django.db import models
from funsionariu.models import *
from Turma.models import *
from Disiplina.models import *
from Classe.models import *
from departamento.models import *


class Horas(models.Model):
	oras_hahu=models.TimeField(null=True, blank=True)
	oras_remata=models.TimeField(null=True, blank=True)
	def __str__(self):
		template = '{0.classe}'
		return f"{self.oras_hahu} - {self.oras_remata}"

class Horario_est(models.Model):
	Horas = models.ForeignKey(Horas, on_delete=models.CASCADE , null=True , blank=True)
	Loron = (
		('Segunda-Feira', 'Segunda-Feira'),
		('Tersa-Feira', 'Tersa-Feira'),
		('Kuarta-Feira', 'Kuarta-Feira'),
		('Kinta-Feira', 'Kinta-Feira'),
		('Sexta-Feira',  'Sexta-Feira'),
		('Sabadu',  'Sabadu'),
		
	)
	loron = models.CharField(max_length=20, choices=Loron, null=True)
	profesores = models.ForeignKey(Funsionariu, on_delete=models.CASCADE )
	turma = models.ForeignKey(turma, on_delete=models.CASCADE , null=True, blank=True)
	# Classe = models.ForeignKey(classe, on_delete=models.CASCADE , null=True, blank=True)
	#Departamento = models.ForeignKey(departamento, on_delete=models.SET_NULL, null=True)
	Diciplina = models.ForeignKey(diciplina, on_delete=models.CASCADE , null=True , blank=True)
	
	def __str__(self):
		template = '{0.loron}'
		return template.format(self)
	@property
	def same_times(self):
		return self.oras_hahu == self.oras_remata
