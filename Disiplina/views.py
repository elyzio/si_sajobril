from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.conf import settings

@login_required()
@allowed_users(allowed_roles=['admin'])
def ListaDics(request):
	group = request.user.groups.all()[0].name
	dics = diciplina.objects.all()
	print(dics)
	context = {
		'konf':"in active",
		'konfAct':"active",
		'group':group,
		'dics':dics,
		'title':"Lista Disiplina",
	}
	return render(request,'disiplina/lista_dics.html',context)
@login_required
@allowed_users(allowed_roles=['admin'])
def AddDics(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = dicsForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			dics = instance.Diciplina
			instance.save()
			messages.success(request, f'Diciplina {dics} is Added Successfully.')
			return redirect('ListaDics')
	else:
		form = dicsForm()
	context = {
		'konf':"in active",
		'konfAct':"active",
		"group":group,
		'page':"form",
		'form': form, 
	}
	return render(request, 'disiplina/form_dics.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def updatedics(request,hashid):
	group = request.user.groups.all()[0].name
	dicsData = get_object_or_404(diciplina,id=hashid)
	if request.method == 'POST':
		form = dicsForm(request.POST,instance=dicsData)
		if form.is_valid():
			instance = form.save()
			messages.info(request, f'Diciplina is updated Successfully.')
			return redirect('ListaDics')
	else:
		form = dicsForm(instance=dicsData)
	context = {
		'konf':"in active",
		'konfAct':"active",
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'disiplina/form_dics.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def Deletedics(request, id_dics):
	dics = get_object_or_404(diciplina, id=id_dics)
	Diciplina = dics.Diciplina
	dics.delete()
	messages.warning(request, f'Classe {Diciplina} is Deleted Successfully.')
	return redirect('ListaDics')

