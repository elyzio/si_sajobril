from django.db import models

class departamento(models.Model):
	nome_departamento = models.CharField(max_length=100)
	
	def __str__(self):
		template =  '{0.nome_departamento}'
		return template.format(self)
