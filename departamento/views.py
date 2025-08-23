from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
#from estudante.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users

@login_required()
@allowed_users(allowed_roles=['admin'])
def ListaDep(request):
	group = request.user.groups.all()[0].name
	dep = departamento.objects.all()
	
	context = {
		'konf':"in active",
		'konfAct':"active",
		'group':group,
		'dep':dep,
		'title':"Lista Departamento",
	}
	return render(request,'depertamento/lista_dep.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def adddep(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = depForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			dep = instance.nome_departamento
			instance.save()
			messages.success(request, f'Departamento {dep} is Added Successfully.')
			return redirect('ListaDep')
	else:
		form = depForm()
	context = {
		'konf':"in active",
		'konfAct':"active",
		"group":group,
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	}
	return render(request, 'depertamento/form_dep.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def updateDep(request,hashid):
	group = request.user.groups.all()[0].name
	animalData = get_object_or_404(departamento,id=hashid)
	if request.method == 'POST':
		form = depForm(request.POST,instance=animalData)
		if form.is_valid():
			instance = form.save()
			messages.info(request, f'Departaento is updated Successfully.')
			return redirect('ListaDep')
	else:
		form = depForm(instance=animalData)
	context = {
		'konf':"in active",
		'konfAct':"active",
		'sukuActive':"active",
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'depertamento/form_dep.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def Deletedep(request, id_dep):
	dep = get_object_or_404(departamento, id=id_dep)
	nome_departamento = dep.nome_departamento
	dep.delete()
	messages.warning(request, f'Departamento {nome_departamento} is Deleted Successfully.')
	return redirect('ListaDep')

