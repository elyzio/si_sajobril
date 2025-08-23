from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from .models import *

class DateInput(forms.DateInput):
	input_type = 'date'
class TimeInput(forms.TimeInput):
	input_type = 'time'

class hor_Form(forms.ModelForm):
	#Data = forms.DateTimeField(label='Data', widget=DateInput())
	class Meta:
		model = Horario_est
		fields ='__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				# Column('Data', css_class='form-group col-md-4 mb-0'),
				Column('loron', css_class='form-group col-md-4 mb-0'),
				Column('profesores', css_class='form-group col-md-4 mb-0'),
				Column('turma', css_class='form-group col-md-4 mb-0'),
				# Column('Classe', css_class='form-group col-md-4 mb-0'),
				#Column('Departamento', css_class='form-group col-md-4 mb-0'),
				Column('Diciplina', css_class='form-group col-md-4 mb-0'),
				Column('Horas', css_class='form-group col-md-4 mb-0'),
				
			),
			HTML(
				""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML(
				"""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)

