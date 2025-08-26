from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from import_export import resources


class estudanteRecources(resources.ModelResource):
	class Meta:
		model = Estudante
class EstudanteAdmin(ImportExportModelAdmin):
	resource_class = estudanteRecources
admin.site.register(Estudante, EstudanteAdmin)

# admin.site.register(UserEstudante)
admin.site.register(DetailEst)
admin.site.register(TransferStudent)

