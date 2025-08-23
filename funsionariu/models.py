from django.db import models
from custom.models import * 
from Ano.models import *
from Turma.models import *
from django.contrib.auth.models import User


# Create your models here. 
class DepFun(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	def __str__(self) :
		template = '{0.name}'
		return template.format(self)


class Funsionariu(models.Model):
	user =  models.OneToOneField(User, on_delete=models.CASCADE,null=True,related_name="userFunsionarius")
	codeP=models.CharField(max_length=10,blank=True, null=True, verbose_name="Codigu professores")
	naran = models.CharField(max_length=200, null=True)
	SEXO = (
		('Mane', 'Mane'),
		('Feto', 'Feto'),
	)
	Sexo = models.CharField(max_length=20, choices=SEXO, null=True)
	aldeia = models.ForeignKey(Aldeia, on_delete=models.CASCADE,null=True,blank=True)
	village = models.ForeignKey(Village, on_delete=models.CASCADE,null=True,related_name="VVillage")
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE,null=True,related_name="AAdministrativePost")
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE,null=True,related_name="MMunicipality")
	hela_fatin = models.CharField(max_length=50, null=True, blank=True)
	data_moris = models.DateField(null=True, blank=True)
	fatin_moris = models.CharField(max_length=50, null=True, blank=True)
	departamento = models.ForeignKey(DepFun, on_delete=models.CASCADE,null=True, blank=True)
	email = models.CharField(max_length=200, null=True)
	nu_telefone = models.CharField(max_length=200, null=True)
	Estatus = (
		('Permanente', 'Permanente'),
		('Kontratadu', 'Kontratadu'),
		('Voluntario', 'Voluntario'),
	)
	estatus = models.CharField(max_length=20, choices=Estatus,null=True, blank=True)
	Nivel_Estudu = (
		('Secundario', 'Secundario'),
		('Diploma 1', 'Diploma 1'),
		('Diploma 2', 'Diploma 2'),
		('Diploma 3', 'Diploma 3'),
		('Lisensiatura', 'Lisensiatura'),
		('Masterado', 'Masterado'),
		('Doutoramento', 'Doutoramento'),
		('Finalista', 'Finalista'),
		
	)
	nivel_estudu = models.CharField(max_length=20, choices=Nivel_Estudu, null=True)
	area_estudu = models.CharField(max_length=50, null=True, blank=True)
	pozisaun=models.CharField(max_length=50, null=True, blank=True)
	Estadu_civil = (
		('Klosan', 'Klosan'),
		('Kazadu', 'Kazadu'),
		('Berlakiadu', 'Berlakeadu'),
		('Relijiozu', 'Relijiozu'),
	)
	estadu_civil = models.CharField(max_length=20, choices=Estadu_civil,null=True, blank=True)
	image = models.ImageField(upload_to='funsionariu', null=True,blank=True)
	# tipu_f = models.CharField(choices=[('Dir','Diretor'),('Fun','Funsionariu'),('EIP','Ekipa Implementasaun Programa')],max_length=30,null=True,blank=True)
	user_created =  models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	

	def __str__(self):
		template = '{0.naran} '
		return template.format(self)

class UserFunsionariu(models.Model):
	user =  models.OneToOneField(User, on_delete=models.CASCADE,null=True,related_name="userFunsionariu")
	funsionariu = models.OneToOneField(Funsionariu,on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	user_created =  models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.funsionariu} {0.user}'
		return template.format(self)
	
class FunsionarioTurma(models.Model):
	funsionario = models.ForeignKey(Funsionariu, on_delete=models.CASCADE, related_name="Funsionario")
	ano = models.ForeignKey(Ano, on_delete=models.CASCADE, null=True, related_name="AnoFunTurma")
	turma = models.ForeignKey(turma, on_delete=models.CASCADE, null=True, related_name="TurmaFun")

	def __str__(self):
		template = '{0.funsionario} -> {0.ano} -> {0.turma}'
		return template.format(self)


