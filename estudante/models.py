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


class TransferStudent(models.Model):
	TRANSFER_TYPE = (
		('IN', 'Transfer In'),
		('OUT', 'Transfer Out'),
	)
	
	STATUS_CHOICES = (
		('PENDING', 'Pending'),
		('APPROVED', 'Approved'),
		('REJECTED', 'Rejected'),
	)
	
	estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='transfers')
	transfer_type = models.CharField(max_length=3, choices=TRANSFER_TYPE)
	from_school = models.CharField(max_length=100, null=True, blank=True)
	to_school = models.CharField(max_length=100, null=True, blank=True)
	from_turma = models.ForeignKey(turma, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_from')
	to_turma = models.ForeignKey(turma, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_to')
	transfer_date = models.DateField()
	request_date = models.DateTimeField(auto_now_add=True)
	reason = models.TextField(null=True, blank=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
	approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_transfers')
	approval_date = models.DateTimeField(null=True, blank=True)
	notes = models.TextField(null=True, blank=True)
	
	def __str__(self):
		return f"{self.estudante.naran} - {self.get_transfer_type_display()} ({self.status})"
