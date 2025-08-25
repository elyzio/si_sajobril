from django.urls import path
from .views import *

urlpatterns = [
	path('est/<str:pk>/tinan/',EstTinList, name="est-tin-list"),
	path('lista-ano/', ListaAno, name="ListaAno"),
	path('add-ano/', AddAno, name="AddAno"),
	path('update-ano/<str:hashid>', updateAno, name="updateAno"),
	path('delete-ano/<str:id_ano>', DeleteAno, name="DeleteAno"),
	path('activate-ano/<str:id_ano>', ActivateAno, name="ActivateAno"),
	
	# Filtered year-specific student lists
	path('year/<str:pk>/transferred-in/', YearTransferredIn, name="year-transferred-in"),
	path('year/<str:pk>/transferred-out/', YearTransferredOut, name="year-transferred-out"),
	path('year/<str:pk>/alumni/', YearAlumni, name="year-alumni"),
	path('year/<str:pk>/pending-transfers/', YearPendingTransfers, name="year-pending-transfers"),
	path('year/<str:pk>/all-registered/', YearAllRegistered, name="year-all-registered"),
]