from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.decorators import allowed_users
from django.conf import settings
from valor import forms, models

@login_required()
@allowed_users(allowed_roles=['admin','estudante','Tesoreira','diretor','professor','Secretario'])
def lista_historia_eskola(request):
	group = request.user.groups.all()[0].name
	historia_eskola = historia.objects.all()		
	context = {
		'hisAct':'active',
		'konBAct':'in active',
		'historia_eskola':historia_eskola, 
		'group': group, "page":"list",
		'title': 'HISTORIA ',
	}
	return render(request,'historia/lista_historia.html',context)

	
@login_required
@allowed_users(allowed_roles=['admin'])
def add_historia(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = historiaform(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			his = instance.Naran_eskola
			instance.save()
			messages.success(request, f'Historia {his} is Added Successfully.')
			return redirect('lista-historia-eskola')
	else:
		form = historiaform()
	context = {
		'hisAct':'active',
		'konBAct':'in active',
		"group":group,
		'page':"form",
		'form': form, 
	}
	return render(request, 'historia/form_historia.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def updatehistoria(request,hashid):
	group = request.user.groups.all()[0].name
	historiaData = get_object_or_404(historia,id=hashid)
	if request.method == 'POST':
		form = historiaform(request.POST,instance=historiaData)
		if form.is_valid():
			instance = form.save()
			messages.info(request, f'historia is updated Successfully.')
			return redirect('lista-historia-eskola')
	else:
		form = historiaform(instance=historiaData)
	context = {
		'hisAct':'active',
		'konBAct':'in active',
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'historia/form_historia.html', context)

