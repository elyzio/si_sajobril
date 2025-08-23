from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from .models import *

class trForm(forms.ModelForm):
	class Meta:
		model = turma
		fields = ['Turma','classe']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				# Column('Departamento', css_class='form-group col-md-4 mb-0'),
				# Column('code_turma', css_class='form-group col-md-4 mb-0'),
				Column('Turma', css_class='form-group col-md-4 mb-0'),
				Column('classe', css_class='form-group col-md-4 mb-0'),

			),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)