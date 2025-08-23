from django.urls import path
from . import views


urlpatterns = [
	path('lista-Funsionariu/',views.ListaFunsionariu,name="ListaFunsionariu"),
	path('adisiona-Funsionariu/',views.AddFunsionariu,name="AddFunsionariu"),
	path('delete-professores/<str:id_prof>', views.deleteprof, name="deleteprof"),
	path('altera-dadus-Funsionariu/<str:hashid>',views.UpdateFunsionariu,name="UpdateFunsionariu"),
	path('Detail-View-professor/<str:id_est>/', views.detailViewprof, name='detailViewprof'), 
	path('dashboard/report/e/active/professores/', views.EReportListActiveFunsionariu, name="e-active-funsionariu"),
    path('adisiona/professor-classe/<str:idGet>', views.AddProfTurma, name="addFunTurma"),
    path('update/professor-classe/<str:idGet>/<str:idPT>/', views.UpdateProfTurma, name="updateFunTurma"),
    
	# Professor
    path('profile/',views.FunsionariuProfile,name="fun-profile"),
    path('profile/update/',views.FunsionariuProfileUpdate,name="fun-profile-update"),
    
	path('turma/list/',views.ProfTurmaLista, name='fun-turma-lista'),
	path('turma/report/',views.ProfTurmareport, name='fun-turma-report'),
	path('turma/add/',views.ProfTurmaAdd, name='fun-turma-add'),
	path('turma/update/<pk>/',views.ProfTurmaUpdate, name='fun-turma-update'),
	path('turma/delete/<pk>/',views.ProfTurmaDelete, name='fun-turma-delete'),
]