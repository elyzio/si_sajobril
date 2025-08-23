from django.urls import path
from . import views
urlpatterns = [
	path('userlist/',views.userlist, name="userlist"),
	path('manage-user-account/', views.manageAccount, name="manageAccount"),
	path('change-user-password/', views.changeAccountPassword, name="changeAccountPassword"),
	path('delete-user/<str:id_user>', views.deleteuser, name="deleteuser"),

]