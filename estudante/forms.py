from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from .models import *
from custom.models import *

class DateInput(forms.DateInput):
	input_type = 'date'

class est_Form(forms.ModelForm): 
	data_resisto = forms.DateField(label='data_resisto', widget=DateInput())
	Data_moris = forms.DateField(label='Data_moris', widget=DateInput())
	class Meta:
		model = Estudante
		fields = ['image','Ano_Resisto','data_resisto','emis','naran','Data_moris','municipality',\
		'administrativepost','village','aldeia','Sexo','naran_aman','naran_inan',\
		'nu_telefone']
		
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['municipality'].queryset = Municipality.objects.all()
		self.fields['administrativepost'].queryset = AdministrativePost.objects.none()
		self.fields['village'].queryset = Village.objects.none()
		self.fields['aldeia'].queryset = Aldeia.objects.none()
		if 'municipality' in self.data:
			try:
				municipality = int(self.data.get('municipality'))
				self.fields['administrativepost'].queryset = AdministrativePost.objects.filter(municipality__id=municipality).order_by('name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk:
			self.fields['administrativepost'].queryset = self.instance.municipality.administrativepost_set.order_by('name')

		if 'administrativepost' in self.data:
			try:
				administrativepost = int(self.data.get('administrativepost'))
				self.fields['village'].queryset = Village.objects.filter(administrativepost__id=administrativepost).order_by('name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk:
			self.fields['village'].queryset = self.instance.administrativepost.village_set.order_by('name')

		if 'village' in self.data:
			try:
				village = int(self.data.get('village'))
				self.fields['aldeia'].queryset = Aldeia.objects.filter(village__id=village).order_by('name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk:
			self.fields['aldeia'].queryset = self.instance.village.aldeia_set.order_by('name')

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('Ano_Resisto', css_class='form-group col-md-4 mb-0'),
				Column('data_resisto', css_class='form-group col-md-4 mb-0'),
				Column('emis', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
				),
			
			Row(
				Column('naran', css_class='form-group col-md-6 mb-0'),
				Column('municipality', css_class='form-group col-md-3 mb-0'),
				Column('administrativepost', css_class='form-group col-md-3 mb-0'),
				
				css_class='form-row'
				),
			Row(
				Column('village', css_class='form-group col-md-3 mb-0'),
				Column('aldeia', css_class='form-group col-md-3 mb-0'),
				Column('Data_moris', css_class='form-group col-md-3 mb-0'),
				Column('Sexo', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
				),
			Row(
				Column('naran_aman', css_class='form-group col-md-5 mb-0'),
				Column('naran_inan', css_class='form-group col-md-4 mb-0'),
				Column('nu_telefone', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'

				),
		
			
			Row(
				Column('image', css_class='form-group col-md-12 mb-0', onchange="myFunction()"),
				),
			
			HTML(""" <center> <img id='output' width='200' /> </center> """),
			HTML(
				""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML(
				"""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)

class est_classe_Form(forms.ModelForm):
	class Meta:
		model = DetailEst
		fields = ['Ano_Academinco','Turma']
		labels = {
			"Ano_Academinco":"Tinan Akademiku "
		}
		
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				
				
				Column('Ano_Academinco', css_class='form-group col-md-4 mb-0'),
				
				Column('Turma', css_class='form-group col-md-4 mb-0'),
			),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)


class InternalTransferForm(forms.ModelForm):
	transfer_date = forms.DateField(label='Data Transfer', widget=DateInput())
	
	class Meta:
		model = TransferStudent
		fields = ['to_turma', 'transfer_date', 'reason']
		labels = {
			'to_turma': 'Ba Turma',
			'transfer_date': 'Data Transfer',
			'reason': 'Razaun'
		}
		widgets = {
			'reason': forms.Textarea(attrs={'rows': 3})
		}
	
	def __init__(self, *args, **kwargs):
		current_turma = kwargs.pop('current_turma', None)
		super().__init__(*args, **kwargs)
		
		# Exclude current turma from choices
		if current_turma:
			self.fields['to_turma'].queryset = turma.objects.exclude(id=current_turma.id)
		
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('to_turma', css_class='form-group col-md-6 mb-0'),
				Column('transfer_date', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('reason', css_class='form-group col-md-12 mb-0'),
			),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-success" type="submit" title="Save"><span class="btn-label"><i class='fa fa-exchange'></i></span> Transfer Internal</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)


class ExternalTransferForm(forms.ModelForm):
	transfer_date = forms.DateField(label='Data Transfer', widget=DateInput())
	
	class Meta:
		model = TransferStudent
		fields = ['transfer_type', 'from_school', 'to_school', 'to_turma', 'transfer_date', 'reason']
		labels = {
			'transfer_type': 'Tipu Transfer',
			'from_school': 'Husi Eskola',
			'to_school': 'Ba Eskola',
			'to_turma': 'Ba Turma (se transfer IN)',
			'transfer_date': 'Data Transfer',
			'reason': 'Razaun'
		}
		widgets = {
			'reason': forms.Textarea(attrs={'rows': 3}),
			'transfer_type': forms.Select(choices=[('IN', 'Transfer In'), ('OUT', 'Transfer Out')])
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('transfer_type', css_class='form-group col-md-6 mb-0'),
				Column('transfer_date', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('from_school', css_class='form-group col-md-6 mb-0'),
				Column('to_school', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('to_turma', css_class='form-group col-md-6 mb-0'),
			),
			Row(
				Column('reason', css_class='form-group col-md-12 mb-0'),
			),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-warning" type="submit" title="Save"><span class="btn-label"><i class='fa fa-plane'></i></span> Transfer External</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)