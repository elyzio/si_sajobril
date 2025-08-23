from django.urls import path
from .views import *

urlpatterns = [
	path('est/<str:pk>/tinan/',EstTinList, name="est-tin-list"),
	path('lista-ano/', ListaAno, name="ListaAno"),
	path('add-ano/', AddAno, name="AddAno"),
	path('update-ano/<str:hashid>', updateAno, name="updateAno"),
	path('delete-ano/<str:id_ano>', DeleteAno, name="DeleteAno"),
	path('activate-ano/<str:id_ano>', ActivateAno, name="ActivateAno"),
]