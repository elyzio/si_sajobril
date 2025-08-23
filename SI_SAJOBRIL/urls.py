from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from SI_SAJOBRIL import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('publicApp.urls')),
    path('', include('main.urls')),
    path('visitor/', include('publicApp.urls')),
    path('utilizador/', include('users.urls')),
    path('dadus-custom/', include('custom.urls')),
    path('dep/', include('departamento.urls')),
    path('estudante/', include('estudante.urls')),
    path('Classe/', include('Classe.urls')),
    path('Turma/', include('Turma.urls')),
    path('Diciplina/', include('Disiplina.urls')),
    path('Ano/', include('Ano.urls')),
    path('horario/', include('horario.urls')),
    path('valor/', include('valor.urls')),
    path('funsionariu/', include('funsionariu.urls')),
    path('userestudante/', include('userestudante.urls')),
    path('historia/', include ('historia.urls')),
    path('report/', include ('report.urls')),
    path('login/', views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)