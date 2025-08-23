from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from .models import *
from valor import models


class vl_Form(forms.ModelForm):
	class Meta:
		model = valor_est
		fields = ['Tinan_periode','Turma','Diciplina','valor_final','periode','por_extenso']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('Tinan_periode', css_class='form-group col-md-6 mb-0'),
				Column('Turma', css_class='form-group col-md-6 mb-0'),
				Column('Diciplina', css_class='form-group col-md-6 mb-0'),
				Column('periode', css_class='form-group col-md-6 mb-0'),
				Column('valor_final', css_class='form-group col-md-4 mb-0'),
				Column('por_extenso', css_class='form-group col-md-4 mb-0'),
			),
			HTML(
				""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML(
				"""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)

class vl_Form1(forms.ModelForm):
	class Meta:
		model = valor_est
		fields = ['Diciplina','valor_final','por_extenso']

	def __init__(self, *args, **kwargs):
		
		tinan = kwargs.pop('tinan', None)
		periode = kwargs.pop('periode', None)
		estudante = kwargs.pop('estudante', None)
		dept = kwargs.pop('dept', None)

		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				# Column('Tinan_periode', css_class='form-group col-md-6 mb-0'),
				# Column('Turma', css_class='form-group col-md-6 mb-0'),
				Column('Diciplina', css_class='form-group col-md-6 mb-0'),
				# Column('periode', css_class='form-group col-md-6 mb-0'),
				Column('valor_final', css_class='form-group col-md-4 mb-0'),
				Column('por_extenso', css_class='form-group col-md-4 mb-0'),
			),
			HTML(
				""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML(
				"""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)

		CT_SUBJECTS = ["Matematica", "Fisica", "Quimica", "Biologia", "Geologia"]
		CSH_SUBJECTS = ["Economia", "Sociologia", "Geografia", "Historia", "Cidadania"]
		SPECIAL_SUBJECTS = CT_SUBJECTS + CSH_SUBJECTS
		
		qs = diciplina.objects.none()
		if tinan and periode and estudante:
			qs = diciplina.objects.all()

			if dept == 1:  # IPA
				qs = qs.exclude(Diciplina__in=CSH_SUBJECTS)
			elif dept == 2:  # IPS
				qs = qs.exlude(Diciplina__in=CT_SUBJECTS)
				
			existing = valor_est.objects.filter(
                Tinan_periode=tinan,
                periode=periode,
                estudante=estudante
            ).values_list('Diciplina_id', flat=True)
			qs = qs.exclude(id__in=existing)
		
		self.fields['Diciplina'].queryset = qs


class periodoForm(forms.ModelForm):
	class Meta:
		model = Periode
		fields = ['nome_periode']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('nome_periode', css_class='form-group col-md-6 mb-0'),
			),
			HTML(
				""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML(
				"""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)


# Clasificasaun valor forms 

class Clasificasao_valor_form(forms.ModelForm):
	class Meta:
		model = Clasificasao_valor
		fields = ['clasificasao','No_clasificasao','Klasse','Comportamento','Aplicasao_assiduidade','Higene','Justificasao','Injustificasao','periode']

		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				
				
				Column('periode', css_class='form-group col-md-4 mb-0'),
				Column('Klasse', css_class='form-group col-md-4 mb-0'),
				Column('clasificacao', css_class='form-group col-md-6 mb-0'),
				Column('No_clasificasao', css_class='form-group col-md-6 mb-0'),
				Column('Justificasao', css_class='form-group col-md-6 mb-0'),
				Column('Injustificacao', css_class='form-group col-md-6 mb-0'),
				Column('Comportamento', css_class='form-group col-md-12 mb-0'),
				Column('Aplicacao_assiduidade', css_class='form-group col-md-6 mb-0'),
				Column('Higene', css_class='form-group col-md-6 mb-0'),
				
			),
			HTML(""" <div class="text-left mt-4"> <button class="btn btn-sm btn-labeled btn-info" type="submit" title="Save"><span class="btn-label"><i class='fa fa-save'></i></span> Save</button>"""),
			HTML("""  <button class="btn btn-sm btn-labeled btn-secondary" onclick=self.history.back()><span class="btn-label"><i class="fa fa-window-close"></i></span> Cancel</button></div>""")
		)