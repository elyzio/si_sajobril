import django_filters
from crispy_forms.helper import FormHelper
from django_filters import DateFilter, CharFilter
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML

from .models import *

class estFilter(django_filters.FilterSet):
	class Meta:
		model = Estudante
		fields = '__all__'
		exclude = ['emis','naran','religiaun','Sexo ','data_resisto','fatin_moris','Data_moris','Sexo','hela_fatin','municipality','village','administrativepost',
				'aldeia','naran_aman','naran_inan','nu_telefone','image','tipu_e','user_created','date_created','hashed']

