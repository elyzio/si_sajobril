from django.urls import path
from .views import *

urlpatterns = [
	path('lista-diciplina/', ListaDics, name="ListaDics"),
	path('add-diciplina/', AddDics, name="AddDics"),
	path('update-diciplina/<str:hashid>', updatedics, name="updatedics"),
	path('delete-diciplina/<str:id_dics>', Deletedics, name="Deletedics"),
]