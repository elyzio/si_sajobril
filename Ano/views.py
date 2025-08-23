from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from estudante.models import Estudante
from estudante.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.conf import settings
from django.db.models import Sum, Count


@login_required()
@allowed_users(allowed_roles=['admin'])
def ListaAno(request):
	group= request.user.groups.all()[0].name
	estudante = Estudante.objects.all().count()
	ano=Ano.objects.order_by('-ano')
	loopingestudanteano= []
	for x in ano.iterator() :
		total_sexo_Mane_tinan = Estudante.objects.filter(
			Ano_Resisto_id=x.id,
			Sexo="Mane").count()
		total_sexo_Feto_tinan = Estudante.objects.filter(
			Ano_Resisto_id=x.id,
			Sexo="Feto").count()
		loopingestudanteano.append({'id':x.id,'ano':x.ano,
		'total_sexo_Mane_tinan':total_sexo_Mane_tinan,
		'total_sexo_Feto_tinan':total_sexo_Feto_tinan,})
	dict = {
		"title":"Lista Tinan Eskola",
		'konf':"in active",
		'konfAct':"active",
		'ano':ano,
		'estudante':estudante,
		'group':group,
		"page":"list",
		'loopingestudanteano':loopingestudanteano,
		
	}
	return render(request, 'ano/homeano1.html',context=dict)
	
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director'])
def EstTinList(request, pk):
	group = request.user.groups.all()[0].name 
	tin = get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin).all().order_by('Ano_Resisto')
	tinan = Ano.objects.all()
	context = {'est': est, 'tinan':tinan, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request, 'estudante/lista_estudante.html', context)
@login_required
@allowed_users(allowed_roles=['admin'])
def AddAno(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = AnoForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			ano = instance.ano
			instance.save()
			messages.success(request, f'Ano {ano} is Added Successfully.')
			return redirect('ListaAno')
	else:
		form = AnoForm()
	context = {
		"group":group,
		'konf':"in active",
		'konfAct':"active",
		'page':"form",
		'form': form, 
	}
	return render(request, 'ano/form_ano1.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def updateAno(request,hashid):
	group = request.user.groups.all()[0].name
	AnoData = get_object_or_404(Ano,id=hashid)
	if request.method == 'POST':
		form = AnoForm(request.POST,instance=AnoData)
		if form.is_valid():
			instance = form.save()
			messages.info(request, f'Ano is updated Successfully.')
			return redirect('ListaAno')
	else:
		form = AnoForm(instance=AnoData)
	context = {
		'konf':"in active",
		'konfAct':"active",
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'ano/form_ano1.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def DeleteAno(request, id_ano):
	# ano = get_object_or_404(Ano, id=id_ano)
	ano = get_object_or_404(Ano, id=id_ano)
	an = ano.ano
	ano.delete()
	messages.warning(request, f'Tinan {an} is Deleted Successfully.')
	return redirect('ListaAno')

@login_required()
@allowed_users(allowed_roles=['admin'])
def ActivateAno(request, id_ano):
	# ano = get_object_or_404(Ano, id=id_ano)
	ano = get_object_or_404(Ano, id=id_ano)
	anos = Ano.objects.exclude(id=ano.id)
	for a in anos:
		a.is_active = False
		a.save()
	an = ano.ano
	ano.is_active = True
	ano.save()
	messages.warning(request, f'Tinan {an} is Activated Successfully.')
	return redirect('ListaAno')





