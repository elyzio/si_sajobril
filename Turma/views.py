from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.conf import settings

@login_required()
@allowed_users(allowed_roles=['admin'])
def listaTurma(request):
	group = request.user.groups.all()[0].name
	tr = turma.objects.all()
	context = {
		'konf':"in active",
		'konfAct':"active",
		'group':group,
		'tr':tr,
		'title':"Lista Turma",
	}
	return render(request,'turma/lista_turma.html',context)
@login_required
@allowed_users(allowed_roles=['admin'])
def addTurma(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = trForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			tr = instance.Turma
			instance.save()
			messages.success(request, f'Turma {tr} is Added Successfully.')
			return redirect('listaTurma')
	else:
		form = trForm()
	context = {
		'konf':"in active",
		'konfAct':"active",
		"group":group,
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	}
	return render(request, 'turma/form_turma.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def updateTurma(request,hashid):
	group = request.user.groups.all()[0].name
	trData = get_object_or_404(turma,id=hashid)
	if request.method == 'POST':
		form = trForm(request.POST,instance=trData)
		if form.is_valid():
			instance = form.save()
			messages.info(request, f'Classe is updated Successfully.')
			return redirect('listaTurma')
	else:
		form = trForm(instance=trData)
	context = {
		'konf':"in active",
		'konfAct':"active",
		'sukuActive':"active",
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'turma/form_turma.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def deleteTurma(request, id_turma):
	tr = get_object_or_404(turma, id=id_turma)
	Turma = tr.Turma
	tr.delete()
	messages.warning(request, f'Classe {Turma} is Deleted Successfully.')
	return redirect('listaTurma')
	
@login_required
def load_Turma(request):
	post_id = request.GET.get('turma')
	tur = turma.objects.filter(Classe__id=post_id).order_by('name')
	return render(request, 'turma_dropdownd.html', {'tur': tur})