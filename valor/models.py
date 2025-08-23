from django.db import models
from estudante.models import *
from Disiplina.models import * 

class  Periode(models.Model):
	nome_periode = models.CharField(max_length=100)
	is_active = models.BooleanField(default=False, null=True, blank=True)
	
	def __str__(self):
		template =  '{0.nome_periode}' 
		return template.format(self)
 
class valor_est(models.Model):
	Tinan_periode = models.ForeignKey(Ano, on_delete=models.CASCADE)
	periode = models.ForeignKey(Periode, on_delete=models.CASCADE)
	estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
	Turma = models.ForeignKey(turma, on_delete=models.CASCADE)
	Diciplina = models.ForeignKey(diciplina, on_delete=models.CASCADE , null=True , blank=True)
	valor_final = models.IntegerField() 
	por_extenso=models.CharField(max_length=32, null=True)
	is_approved = models.BooleanField(default=False, null=True, blank=True)

	def __str__(self):
		template = '{0.estudante}'
		return f"{self.estudante}" 



class Clasificasao_valor(models.Model):
	estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
	periode = models.ForeignKey(Periode, on_delete=models.CASCADE)
	Klasse = models.ForeignKey(classe, on_delete=models.CASCADE)
	clasificasao = models.IntegerField()
	No_clasificasao = models.IntegerField()
	Comportamento =models.TextField(max_length=100)
	Aplicasao_assiduidade = models.TextField(max_length=100)
	Higene=models.TextField(max_length=32, null=True)
	Justificasao =models.IntegerField()
	Injustificasao =models.IntegerField()
	
	def __str__(self):
		template = '{0.valor_estudante}'
		return f"{self.estudante}  - {self.periode}- {self.clasificasao} - {self.Comportamento}"


