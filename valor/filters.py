import django_filters
from crispy_forms.helper import FormHelper
from django_filters import DateFilter, CharFilter
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from estudante.models import *

from .models import *

class estFilter(django_filters.FilterSet):
	# start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	# end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	# note = CharFilter(field_name='note', lookup_expr='icontains')
	class Meta:
		model = valor_est 
		fields = ['estudante','Diciplina','periode']
		exclude = ['user_created','hashed','valor_final']