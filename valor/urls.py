from django.urls import path
from . import views

urlpatterns = [
	# print
	path('Valor-estudate10-ano/periodu/print/<str:idPeriodu>/<str:idEst>', views.ValorEstudantePeriod_Print, name="ValorEstudatePeriod-Print"),
	path('Valor-estudate11-ano/periodu/print/<str:idPeriodu>/<str:idEst>', views.ValorEstudantePeriod1_Print1, name="ValorEstudantePeriod1_Print1"),
	path('Valor-estudate12-ano/periodu/print/<str:idPeriodu>/<str:idEst>', views.ValorEstudantePeriod_Print2, name="ValorEstudatePeriod-Print2"),
	path('Valor-estudate/Jeral/', views.lista_valor_Jeral, name="lista_valor_Jeral"),
	path('lista-estudante/klasse/valores/<str:id>/', views.ListaVAlorClass, name='ListaVAlorClass'),
	
	#lista estudante nia Valor
	path('lista-Valor/', views.Listaestudantevalor, name="Listavalor"),
	path('lista-estudante/klasse/<str:id>/Valor', views.ListEstudanteClassValor, name='list-estudante-classe-Valor'),
	path('lista-estudante/Dep/klasse/turma/<str:idDep>/<str:klasse>/<str:idTur>/Valor', views.ListEstDepClaTurValor, name='ListEstDepClaTur-Valor'),
	path('add-add_Clasificasao_valor-+<int:id1>/', views.add_Clasificasao_valor, name="add_Clasificasao_valor"),
	path('add-Valor-estudante/<int:id1>/', views.add_valor, name="add_valor"),
 	path('valor-details/<str:hashid>/<str:id>/', views.DetailViewsVE, name="details-valor"),
	path('update-Valor/<str:hashid>', views.updatevalor, name="updatevalor"),
	path('Valor-estudate/periodu/<str:idPeriodu>/<str:idEst>/', views.ValorEstudantePeriod, name="ValorEstudatePeriod"),
	path('Valor-estudate/periodu11-ano/<str:idPeriodu>/<str:idEst>/', views.ValorEstudantePeriod1, name="ValorEstudantePeriod1"),
	path('Valor-estudate/periodu12-ano/<str:idPeriodu>/<str:idEst>/', views.ValorEstudantePeriod2, name="ValorEstudantePeriod2"),
	path('delete-valor/<str:id_vl>', views.deletevalor, name="deletevalor"),
	

	#periode ..............//................//......................//...................
	path('lista-periodu/', views.ListaPr, name="Lista-periode"),
	path('adisiona-periode/', views.addperiodo, name="adisiona-periode-exame"),
	path('update-Periode/<str:hashid>', views.updateperiode, name="update-periode"),
	path('delete-periode/<str:hashid>', views.deletePeriode, name="Delete-periode"),

	# Prof
	path('lista-Valores-estudante/', views.Listaestudantevalorprof, name="Listavaloresprof"),
    path('valores-details/<str:hashid>/', views.DetailViewsVEProf, name="details-valorPr"),
	path('add-Valor-estudante-turma/<int:id1>/<int:period>/', views.add_valor1, name="add_valor1"),
]