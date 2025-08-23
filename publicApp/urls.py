from django.urls import path
from .views import *

urlpatterns = [
	path('', PublicFilter, name="index_public"),
	path('public-histori-pajination', Public_historia, name="Public_historia"),
	path('public-Galery-estundante', publicEstGaleriList, name="publicEstGaleriList"),
	path('public-Galery-Tin-estundante/<str:pk>/', publicGaleryEstTinList, name="publicGaleryEstTinList"),
	path('public-News-pajination', public_news, name="public_news"),

	path('public-estudante-munisipiu-list/', public_List_estudnte_munisipiu, name="public_List_estudnte_munisipiu"),
	path('public-estudante-tinan-list/', public_List_estudnte_tinan, name="public_List_estudnte_tinan"),
	path('public-estudante-mane-munisipiu-list/<str:pk>/', list_mun_M, name="list_mun_M"),
	path('public-estudante-feto-munisipiu-list/<str:pk>/', list_mun_F, name="list_mun_F"),
	path('public-estudante-Foto-feto-munisipiu-list/<str:pk>/', list_mun_GF, name="list_mun_GF"),
	path('public-estudante-Foto-Mane-munisipiu-list/<str:pk>/', list_mun_GM, name="list_mun_GM"),
	path('public-estudante-Foto-munisipiu-list/<str:pk>/', list_mun_G, name="list_mun_G"),

	path('public-estudante-Progrm-list/', public_List_estudnte_Pro, name="public_List_estudnte_Pro"),
	path('public-estudante-Progrm-list-CT/<str:pk>/', list_progrmCT, name="list_progrmCT"),
	path('public-estudante-Progrm-list-Csh/<str:pk>/', list_progrmCsh, name="list_progrmCsh"),
	path('public-estudante-Foto-Progrm-CT-list/<str:pk>/', list_Ct_G, name="list_Ct_G"),
	path('public-estudante-Foto-Progrm-CSH-list/<str:pk>/', list_Csh_G, name="list_Csh_G"),
	path('public-horariu/', public_horariu, name="public_horariu"),
	path('public-print-horariu/', PrintHorario, name="PrintHorario"),

	path('public-estudante-munisipiu-list/<str:pk>/', list_mun, name="list_mun"),
	path('Public-Detail-News/<str:id_news>/', public_detailView_news, name='public_detailView_news'),
	path('public-lista-estudnate/', public_Listaestudante, name="public_Listaestudante"),
	path('public-lista-sexo-estudnate-Mane/<str:pk>', public_list_estudante_Mane, name="public_list_estudante_Mane"),
	path('public-lista-sexo-estudnate-feto/<str:pk>', public_list_estudante_feto, name="public_list_estudante_feto"),
	path('public-lista-sexo-estudnate-tinan/<str:pk>', public_Listaestudante_tin, name="public_Listaestudante_tin"),
	path('public-lista-estudnate/<str:pk>/tinan/',publicEstTinList, name="publicEstTinList"),
	path('public-Galery-estundante-Tin/<str:pk>/tinan/',publicGaleryEstTinList, name="publicGaleryEstTinList"),
	path('public-Detail-View-estudante/<str:id_est>/', public_detailViewest, name='public_detailViewest'),
	path('public-lista-estudante/klasse/<str:id>/', public_ListEstudanteClass, name='public-list-estudante-classe'),
	path('public-lista-estudante/Dep/klasse/turma/<str:idDep>/<str:klasse>/<str:idTur>', public_ListEstDepClaTur, name='public_ListEstDepClaTur'),
	]