from django.urls import path
from . import views
urlpatterns = [
	path('home/',views.index,name="home"),
	path('home1/',views.home1,name="home1"),
	path('', views.homelogin, name="home-login"),
	
	
]