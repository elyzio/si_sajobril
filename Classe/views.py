from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from estudante.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.conf import settings

@login_required()
@allowed_users(allowed_roles=['admin'])
def ListaClasse(request):
	group = request.user.groups.all()[0].name
	cl = classe.objects.all()
	estudante = Estudante.objects.all()
	context = {
		'konf':"in active",
		'konfAct':"active",
		'group':group,
		'title':"Lista classe",
		"page":"list",
		'cl':cl,	
		'estudante':estudante,	
	}
	return render(request,'classe/lista_classe.html',context)
@login_required
@allowed_users(allowed_roles=['admin'])
def addclasse(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = clForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			cl = instance.name
			instance.save()
			messages.success(request, f'Classe {cl} is Added Successfully.')
			return redirect('ListaClasse')
	else:
		form = clForm()
	context = {
		'konf':"in active",
		'konfAct':"active",
		"group":group,
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	}
	return render(request, 'classe/lista_classe.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def updatecl(request,hashid):
	group = request.user.groups.all()[0].name
	clData = get_object_or_404(classe,id=hashid)
	if request.method == 'POST':
		form = clForm(request.POST,instance=clData)
		if form.is_valid():
			instance = form.save()
			messages.info(request, f'Classe is updated Successfully.')
			return redirect('ListaClasse')
	else:
		form = clForm(instance=clData)
	context = {
		'konf':"in active",
		'konfAct':"active",
		'sukuActive':"active",
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'classe/lista_classe.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def Deletecl(request, id_classe):
	cl = get_object_or_404(classe, id=id_classe)
	Classe = cl.classe
	cl.delete()
	messages.warning(request, f'Classe {Classe} is Deleted Successfully.')
	return redirect('ListaClasse')

@login_required
def load_Classe(request):
	cl_id = request.GET.get('Departamento')
	cl = classe.objects.filter(Departamento_id=cl_id).order_by('name')
	return render(request, 'classe_dropdownd.html', {'cl': cl})