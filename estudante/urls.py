from django.urls import path
from .views import *

urlpatterns = [
	path('lista-estudante/', Listaestudante, name="Listaestudante"),
	path('est/<str:pk>/tinan/',EstTinList, name="est-tin-list"),
	path('add-estudante/', add_estudante, name="add_estudante"),
	path('update-estudante/<str:hashid>', updateest, name="updateest"),
	path('update-Klasse-estudante/<str:idEst>', updateClassestudante, name="updateClassestudante"),
	path('delete-estudante/<str:id_est>', deleteest, name="deleteest"),
	path('Detail-View-estudante/<str:id_est>/', detailViewest, name='detailViewest'),
	path('dashboard/report/e/active/Estudante/', EReportListActiveEstudante, name="e-active-estudante"),
	path('dashboard/report/e/active/Estudante/Classe', EReportListActiveEstudanteClasse, name="EReportListActiveEstudanteClasse"),

	path('lista-estudante/klasse/<str:id>/', ListEstudanteClass, name='list-estudante-classe'),
	path('lista-estudante/Dep/klasse/turma/<str:idDep>/<str:klasse>/<str:idTur>', ListEstDepClaTur, name='ListEstDepClaTur'),
	path('add-estudante/Klasse-<int:id1>/', add_classe_estudante, name="add-classe-estudante"),



	path('students-aprovado/10ANO', list_students_aprovado, name='list_students_aprovado'),
	path('lista-estudante/klasse/aprovado/klasse11ano', ListEstudanteClassAprovado, name='ListEstudanteClassAprovado'),
	path('secretaria/aprova/classe/estudante/<int:id1>', Aprova_estudante_classe, name="Aprova_estudante_classe"),
	path('lista-estudante/Dep/klasse/turma/aprovado/12ANO/aprovasaun/', ListEstudanteClassAprovado12, name='ListEstudanteClassAprovado12'),
	# path('approve-student-home/', list_students_aprovadoHome, name='list_students_aprovadoHome'),
    
	# professor
    path('lista-student/turma', ListEstTurma, name='listEstTurma'),
    path('aprova-student/<id1>', Aprova_estudante_classe, name='aprova-classe'),
    
    # Transfer functionality
    path('transfers/', list_transfers, name='list_transfers'),
    path('transfer/internal/<int:estudante_id>/', create_internal_transfer, name='create_internal_transfer'),
    path('transfer/external/<int:estudante_id>/', create_external_transfer, name='create_external_transfer'),
    path('transfer/detail/<int:transfer_id>/', transfer_detail, name='transfer_detail'),
    path('transfer/approve/<int:transfer_id>/', approve_transfer, name='approve_transfer'),
    path('transfer/reject/<int:transfer_id>/', reject_transfer, name='reject_transfer'),
    path('transferred-out/', transferred_out_students, name='transferred_out_students_all'),
    path('transferred-out/<int:year_id>/', transferred_out_students, name='transferred_out_students'),
    
    # Alumni functionality
    path('alumni/', list_alumni, name='list_alumni'),
    path('alumni/create/<int:estudante_id>/', create_alumni_record, name='create_alumni_record'),
    path('alumni/detail/<int:alumni_id>/', alumni_detail, name='alumni_detail'),
    path('alumni/approve/<int:alumni_id>/', approve_alumni, name='approve_alumni'),
    path('alumni/reject/<int:alumni_id>/', reject_alumni, name='reject_alumni'),
    path('approved-alumni/', approved_alumni_students, name='approved_alumni_students_all'),
    path('approved-alumni/<int:year_id>/', approved_alumni_students, name='approved_alumni_students'),
]