from django.db import models
from custom.models import *
from Turma.models import *  
from departamento.models import *
from Classe.models import *
from Ano.models import *
from django.contrib.auth.models import User
 

from django.db import models


class Estudante(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	Ano_Resisto =  models.ForeignKey(Ano, on_delete=models.SET_NULL,null=True,related_name="TinanR",verbose_name='Ano')
	data_resisto = models.DateField()
	emis = models.CharField(max_length=15, null=True, blank=True)
	naran = models.CharField(max_length=50, null=True, blank=True)
	Data_moris = models.DateField()
	SEXO = (
		('Mane', 'Mane'),
		('Feto', 'Feto'),
	)
	Sexo = models.CharField(max_length=20, choices=SEXO, null=True)
	village = models.ForeignKey(Village, on_delete=models.CASCADE,null=True,related_name="village")
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE,null=True,related_name="AdministrativePost")
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE,null=True,related_name="Municipality")
	aldeia = models.ForeignKey(Aldeia, on_delete=models.CASCADE, null=True,blank=True)
	naran_aman = models.CharField(max_length=50, null=True, blank=True)
	naran_inan = models.CharField(max_length=50, null=True, blank=True)
	nu_telefone = models.CharField(max_length=50, null=True, blank=True)
	image = models.ImageField(upload_to='estudante/', null=True , blank=True)
	have_classes=models.BooleanField(default=False,null=True, blank=True)
	

	def __str__(self):
		template = '{0.naran} '
		return template.format(self)


class DetailEst(models.Model):
	Ano_Academinco =  models.ForeignKey(Ano, on_delete=models.SET_NULL,null=True,related_name="TinanA",verbose_name='Ano')
	estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
	Turma = models.ForeignKey(turma, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	is_aprovadu = models.BooleanField(default=False,null=True, blank=True)
	is_reprovadu = models.BooleanField(default=False,null=True, blank=True)

	def __str__(self):
		template = '{0.estudante.naran},{0.Turma.Turma} '
		return template.format(self)
