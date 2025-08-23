from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from funsionariu.models import Funsionariu,UserFunsionariu
from .forms import * 
from django.contrib.auth.models import User,Group
from custom.utils import *
from custom.models import *
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from users.decorators import allowed_users

# Create your views here.
@login_required
@allowed_users(allowed_roles=['admin','Director','Secretario'])
def ListaFunsionariu(request):
	group = request.user.groups.all()[0].name
	listaFunsionariu = Funsionariu.objects.all()
	context = {
		"rejDadus":"active",
		"rejDadus2":"in active",
		"title":"Lista Professores",
		"active_funsionariu":"active",
		"page":"list",
		"group":group,
		"listaFunsionariu":listaFunsionariu,
	}
	return render(request, "ListaFunsionariu.html",context)

@login_required
@allowed_users(allowed_roles=['admin','Secretario'])
def AddFunsionariu(request):
	group = request.user.groups.all()[0].name
	if request.method == "POST":
	
		form = FunsionariuPostuForm(request.POST,request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			fun = instance.naran
			base_username = instance.naran.split()[0].lower()
			username = base_username
			password = 'sajobril2025'
			counter = 1
			while User.objects.filter(username=username).exists():
				username = f"{base_username}{counter}"
				counter += 1
			user = User.objects.create_user(username=username, password=password)
			instance.user = user
			fun_group, created = Group.objects.get_or_create(name='professor')
			user.groups.add(fun_group)
			
			instance.save()
			
			messages.success(request, f'Professor {fun} Rejistu ho Susesu.')
			return redirect('ListaFunsionariu')
	else:	
		form = FunsionariuPostuForm()
	context ={
		"rejDadus":"active",
		"rejDadus2":"in active",
		"title":"Formulariu Rejistu Professores ",
		"page":"form",
		"form":form,
		"active_funsionariu":"active",
	}
	return render(request,'ListaFunsionariu.html',context)

@login_required
@allowed_users(allowed_roles=['admin','Secretario'])
def UpdateFunsionariu(request,hashid):
	funsionariu = get_object_or_404(Funsionariu,id=hashid)
	if request.method == "POST":
		newid2 = getjustnewid(UserFunsionariu)
		hashid2 = hash_md5(str(newid2))
		newid3 = getjustnewid(User)
		form = FunsionariuPostuForm(request.POST,request.FILES,instance=funsionariu)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Dadus Funsionariu Altera ho Susesu.')
			return redirect('ListaFunsionariu')
	else:	
		form = FunsionariuPostuForm(instance=funsionariu)
	context ={
		"rejDadus":"active",
		"rejDadus2":"in active",
		"title":"Formulariu Altera Dadus Professores",
		"page":"form",
		"form":form,
		"active_funsionariu":"active",
	}
	return render(request,'ListaFunsionariu.html',context)

@login_required()
@allowed_users(allowed_roles=['admin','Secretario'])
def deleteprof(request, id_prof):
	prof = get_object_or_404(Funsionariu, id=id_prof)
	naran = prof.naran
	userP = prof.user
	prof.delete()
	userP.delete()
	messages.warning(request, f'Professor {naran} is Deleted Successfully.')
	return redirect('ListaFunsionariu')


@login_required()
@allowed_users(allowed_roles=['admin','Director','Secretario'])
def detailViewprof(request, id_est):
	activeAno = Ano.objects.filter(is_active=True).first()
	est = Funsionariu.objects.get(id = id_est)
	turma = FunsionarioTurma.objects.filter(ano=activeAno, funsionario=est.id).last()
	context={
		"acAC":"active",
		"acAC2":"in active",
		'form':'list',
		'est':est,
		'mtr':turma,
	}
	return render(request, 'detailprof.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Director','kurikulum','Secretario'])
def EReportListActiveFunsionariu(request):
	objects = Funsionariu.objects.all()
	objects1 = Funsionariu.objects.filter(naran='jbjk')
	context ={
		"title":f"Pajina Relatoriu Lista Professores",
		"page":"list",
		"report_active":"active",
		"objects":objects,
		
	}
	return render(request, "ereportprofessores.html",context)


# Professor
@login_required
@allowed_users(allowed_roles=['Secretario','admin'])
def AddProfTurma(request,idGet):
	prof = Funsionariu.objects.get(id=idGet)
	if request.method == 'POST':
		form = FunsionariuClasseForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.funsionario = prof
			instance.save()
			id1 = instance.funsionario.naran
			messages.success(request, f'Professor da Classe is Added Successfully.')
			return redirect('detailViewprof', prof.id)
	else:
		form = FunsionariuClasseForm()
	context = {
		"rejDadus":"active",
		"rejDadus2":"in active",
		'form':form,
		"title":f"Pajina Adisiona Professores da Classe",
		"page":"formprofT",
		"id": prof.id,
	}
	return render(request, 'detailprof.html', context)

@login_required
@allowed_users(allowed_roles=['Secretario', 'admin'])
def UpdateProfTurma(request,idGet, idPT):
	prof = Funsionariu.objects.get(id=idGet)
	turma = FunsionarioTurma.objects.get(id=idPT)
	if request.method == 'POST':
		form = FunsionariuClasseForm(request.POST, request.FILES, instance=turma)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.funsionario = prof
			instance.save()
			id1 = instance.funsionario.naran
			messages.success(request, f'Professor da Classe is Added Successfully.')
			return redirect('detailViewprof', prof.id)
	else:
		form = FunsionariuClasseForm(instance=turma)
	context = {
		"rejDadus":"active",
		"rejDadus2":"in active",
		'form':form,
		"title":f"Pajina Update Professores da Classe",
		"page":"formprofTU",
		"id": prof.id,
	}
	return render(request, 'detailprof.html', context)

@login_required
@allowed_users(allowed_roles=['professor'])
def FunsionariuProfile(request):
	activeAno = Ano.objects.filter(is_active=True).first()
	user = request.user
	detFun = Funsionariu.objects.get(user=user)
	turma = FunsionarioTurma.objects.filter(ano=activeAno, funsionario=detFun).last()
	context={
		"acAC":"active",
		"acAC2":"in active",
		'form':'list',
		'est':detFun,
		'mtr':turma,
	}
	return render(request,'userFun.html',context)

@login_required
@allowed_users(allowed_roles=['professor'])
def FunsionariuProfileUpdate(request):
	user = request.user
	funsionariu = get_object_or_404(Funsionariu,user=user.id)
	if request.method == "POST":
		newid2 = getjustnewid(UserFunsionariu)
		hashid2 = hash_md5(str(newid2))
		newid3 = getjustnewid(User)
		form = FunsionariuPostuForm(request.POST,request.FILES,instance=funsionariu)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Dadus Funsionariu Altera ho Susesu.')
			return redirect('fun-profile')
	else:	
		form = FunsionariuPostuForm(instance=funsionariu)
	context={
		"acAC":"active",
		"acAC2":"in active",
		"title":"Formulariu Altera Dadus Funsionariu",
		"page":"form",
		"form":form,
		"active_fun":"active",
	}
	return render(request,'userFun.html',context)

@login_required
@allowed_users(allowed_roles=['admin','Secretario'])
def ProfTurmaLista(request):
	group = request.user.groups.all()[0].name
	ano = Ano.objects.filter(is_active=True).first()
	turma = FunsionarioTurma.objects.filter(ano=ano)

	context={
		"acAC":"active",
		"acAC2":"in active",
		"title":"Lista Professor da Turma",
		"page":"list",
		"active_fun":"active",
		"group":group,
		'turmas':turma,
	}
	return render(request,'profTurma/listaTurma.html',context)

@login_required
@allowed_users(allowed_roles=['Secretario'])
def ProfTurmaAdd(request):
	group = request.user.groups.all()[0].name
	ano = Ano.objects.filter(is_active=True).first()
	turma = FunsionarioTurma.objects.filter(ano=ano)

	if request.method == "POST":
		form = FunsionariuClasseForm2(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			naran = instance.turma
			form.save()
			messages.success(request, f'Turma {naran} is Added Successfully.')
			return redirect('fun-turma-lista')
	else:
		form = FunsionariuClasseForm2()

	context={
		"acAC":"active",
		"acAC2":"in active",
		"title":"Adisiona Professor da Turma",
		"page":"form",
		"active_fun":"active",
		"group":group,
		"form":form,
	}
	return render(request,'profTurma/listaTurma.html',context)

@login_required
@allowed_users(allowed_roles=['Secretario'])
def ProfTurmaUpdate(request, pk):
	group = request.user.groups.all()[0].name
	ano = Ano.objects.filter(is_active=True).first()
	turma = get_object_or_404(FunsionarioTurma, id=pk)

	if request.method == "POST":
		form = FunsionariuClasseForm2(request.POST, instance=turma)
		if form.is_valid():
			naran = turma
			form.save()
			messages.success(request, f'Turma {naran} is Updated Successfully.')
			return redirect('fun-turma-lista')
	else:
		form = FunsionariuClasseForm2(instance=turma)

	context={
		"acAC":"active",
		"acAC2":"in active",
		"title":"Update Professor da Turma",
		"page":"form",
		"active_fun":"active",
		"group":group,
		"form":form,
	}
	return render(request,'profTurma/listaTurma.html',context)


@login_required
@allowed_users(allowed_roles=['Secretario'])
def ProfTurmaDelete(request, pk):
	group = request.user.groups.all()[0].name
	ano = Ano.objects.filter(is_active=True).first()
	turma = get_object_or_404(FunsionarioTurma, id=pk)
	naran = turma
	turma.delete()
	messages.warning(request, f'Professor {naran} is Deleted Successfully.')
	return redirect('fun-turma-lista')

@login_required
@allowed_users(allowed_roles=['admin','Secretario'])
def ProfTurmareport(request):
	group = request.user.groups.all()[0].name
	ano = Ano.objects.filter(is_active=True).first()
	turma = FunsionarioTurma.objects.filter(ano=ano)

	context={
		"acAC":"active",
		"acAC2":"in active",
		"title":"Lista Professor da Turma",
		"page":"list",
		"active_fun":"active",
		"group":group,
		'objects':turma,
	}
	return render(request,'profTurma/ereportprofturma.html',context)