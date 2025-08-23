from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import Group,User
from .models import *
from custom.models import *

class DateInput(forms.DateInput):
	input_type = 'date'

class FunsionariuPostuForm(forms.ModelForm):
	class Meta:
		model = Funsionariu
		fields = ['image','aldeia','naran','departamento','municipality','administrativepost','village','Sexo','nu_telefone','email','estatus','pozisaun','nivel_estudu','area_estudu','estadu_civil','data_moris','hela_fatin']
		exclude = ['user_created','hashed','date_created','tipu_f']
		widgets = {
            'data_moris': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['municipality'].queryset = Municipality.objects.all()
		self.fields['administrativepost'].queryset = AdministrativePost.objects.none()
		self.fields['village'].queryset = Village.objects.none()
		# self.fields['data_moris'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
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

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('naran', css_class='form-group col-md-12 mb-0'),
				Column('Sexo', css_class='form-group col-md-4 mb-0'),
				Column('departamento', css_class='form-group col-md-4 mb-0'),
				Column('municipality', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
				
			),
			Row(
				
				Column('administrativepost', css_class='form-group col-md-4 mb-0'),
				Column('village', css_class='form-group col-md-4 mb-0'),
				Column('aldeia', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('data_moris', css_class='form-group col-md-6 mb-0'),
				Column('hela_fatin', css_class='form-group col-md-6 mb-0'),
				# Column('fatin_moris', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('nu_telefone', css_class='form-group col-md-4 mb-0'),
				Column('email', css_class='form-group col-md-4 mb-0'),
				Column('pozisaun', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			
			Row(
				Column('estatus', css_class='form-group col-md-2 mb-0'),
				Column('nivel_estudu', css_class='form-group col-md-3 mb-0'),
				Column('area_estudu', css_class='form-group col-md-5 mb-0'),
				Column('estadu_civil', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				
				Column('image', css_class='form-group col-md-12 mb-0', onchange="myFunction()"),
				css_class='form-row'
			), 
	        HTML(""" <center> <img id='output' width='200' /> </center> """),

			HTML(""" <div class="form-group text-right"><button class="btn btn-sm btn-success" type="submit">Save <i class="fa fa-save"></i></button> """),
			HTML(""" <span class="btn btn-sm btn-secondary"  onclick=self.history.back()><i class="fa close"></i> Cancel</span></div> """)
		)

class FunsionariuClasseForm(forms.ModelForm):
	class Meta:
		model = FunsionarioTurma
		fields = ['ano','turma']
		labels = {
			'ano': 'Tinan Akademiku',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('ano', css_class='form-group col-md-4 mb-0'),
				
				Column('turma', css_class='form-group col-md-4 mb-0'),
			),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)

class FunsionariuClasseForm2(forms.ModelForm):
	class Meta:
		model = FunsionarioTurma
		fields = ['funsionario','ano','turma',]
		labels = {
			'ano': 'Tinan Akademiku',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('funsionario', css_class='form-group col-md-4 mb-0'),
				Column('turma', css_class='form-group col-md-4 mb-0'),
				Column('ano', css_class='form-group col-md-4 mb-0'),
			),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)

