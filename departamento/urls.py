from django.urls import path
from .views import *

urlpatterns = [
	#path('lista-dep/', homeDep, name="homeDep"),
	path('lista-dep/', ListaDep, name="ListaDep"),
	path('add-dep/', adddep, name="adddep"),
	path('update-dep/<str:hashid>', updateDep, name="updateDep"),
	path('delete-dep/<str:id_dep>', Deletedep, name="Deletedep"),
]