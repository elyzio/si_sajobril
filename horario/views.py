from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.conf import settings
from departamento.models import departamento
from django.http import HttpResponseBadRequest
from estudante.models import *
from datetime import time
@login_required()
@allowed_users(allowed_roles=['admin','Secretario','kurikulum','professor']) 
def Listahor(request):
	group = request.user.groups.all()[0].name
	hor= Horario_est.objects.all()
	dep = turma.objects.exclude(classe__name='Alumni').order_by('id')
	context = {
		'group':group,
		'hor':hor,
		'dep':dep,
		'title':"Lista Horario",
		'legend': 'Lista Horario'
	}
	return render(request,'horario/lista_hor.html',context)

def horario_por_loron(request):
	horarios = Horario_est.objects.filter(loron='Segunda').all()
	hor10 = Horario_est.objects.filter(turma__classe__name='10 Ano', loron='Segunda').all()
	hor11 = Horario_est.objects.filter(turma__classe__name='11 Ano', loron='Segunda').all()
	hor12 = Horario_est.objects.filter(turma__classe__name='12 Ano', loron='Segunda').all()

	tur=turma.objects.filter(classe__name='10 Ano')
	tur1=turma.objects.filter(classe__name='11 Ano')
	tur2=turma.objects.filter(classe__name='12 Ano')

	loopingturm = [
        {
            'id': tt.id,
            'Turma': tt.Turma,
            'tot1': Horario_est.objects.filter(turma_id=tt.id, turma__classe__name='10 Ano', loron='Segunda')
        }
        for tt in tur
    ]
	loopingturm1 = [
        {
            'id': tt.id,
            'Turma': tt.Turma,
            'tot1': Horario_est.objects.filter(turma_id=tt.id, turma__classe__name='11 Ano', loron='Segunda')
        }
        for tt in tur1
    ]
    # Get distinct professors and disciplines
	profesores = set(horario.profesores for horario in horarios)
	disciplinas = set(horario.Diciplina for horario in horarios)
	context = {
		'horarios': horarios,
		'profesores': profesores,
		'disciplinas': disciplinas,'tur':tur,'tur1':tur1,'tur2':tur2,\
		'hor10':hor10,
		'hor11':hor11,
		'hor12':hor12,
		'loopingturm1':loopingturm1,
		'loopingturm':loopingturm,

	
    }
	return render(request, 'horario/horario_por_loron.html', context)



@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def HorKlasseList(request, pk):
	group = request.user.groups.all()[0].name 
	dep = get_object_or_404(turma, pk=pk)
	
	hr = Horario_est.objects.filter(turma=dep).all().order_by('loron')
	deps = turma.objects.exclude(classe__name='Alumni').order_by('id')
	context = {'hr': hr, 'group': group,"page":"list",
		'title': 'Lista Horario', 'legend': 'Lista Horario','deps':deps,'dep':dep
	}
	return render(request, 'horario/lista_hor_dep.html', context)

@login_required
@allowed_users(allowed_roles=['admin','kurikulum','professor'])
def add_hor(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = hor_Form(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			hor=instance.loron
			instance.save()
			messages.success(request, f'Horario {hor} is Added Successfully.')
			return redirect('Listahor')
	else:
		form =hor_Form()
	context = {
		"group":group,
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	} 
	return render(request, 'horario/form_hor.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','kurikulum','professor'])
def updatehor(request,hashid):
	group = request.user.groups.all()[0].name
	hor = get_object_or_404(Horario_est,id=hashid)
	if request.method == 'POST':
		form = hor_Form(request.POST,instance=hor)
		if form.is_valid():
			instance = form.save()
			messages.info(request, f'Horario is updated Successfully.')
			return redirect('Listahor')
	else:
		form = hor_Form(instance=hor)
	context = {
		'sukuActive':"active",
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'horario/form_hor.html', context)


@login_required()
@allowed_users(allowed_roles=['admin','kurikulum','professor'])
def deletehor(request, id_hor):
	hor = get_object_or_404(Horario_est, id=id_hor)
	Loron = hor.Loron
	hor.delete()
	messages.warning(request, f'Horario  is Deleted Successfully.')
	return redirect('Listahor')

#Report 

@login_required
@allowed_users(allowed_roles=['admin','Secretario','kurikulum','professor'])
def EReportListActiveHorario(request):
	objects = Horario_est.objects.all()

	context ={
		"title":f"Pajina Relatoriu Lista Horario",
		"report_active":"active",
		"objects":objects,
		
	}
	return render(request, "horario/listActiveHorario.html",context)	

@login_required()
@allowed_users(allowed_roles=['estudante','professor']) 
def ListahorFun(request):
	group = request.user.groups.all()[0].name
	user_id = request.user
	fun = Funsionariu.objects.filter(user=user_id).last()
	hor= Horario_est.objects.filter(profesores=fun)
	dep = turma.objects.exclude(classe__name='Alumni').order_by('id')
	context = {
		'group':group,
		'hor':hor,
		'dep':dep,
		'title':"Lista Horario",
		'legend': 'Lista Horario'
	}
	return render(request,'horario/lista_hor_fun.html',context)

@login_required()
@allowed_users(allowed_roles=['estudante','professor']) 
def ListahorEst(request):
	group = request.user.groups.all()[0].name
	user_id = request.user
	est = Estudante.objects.filter(user=user_id).last()
	detEst = DetailEst.objects.filter(estudante=est).last()
	print(detEst)
	hor= Horario_est.objects.filter(turma=detEst.Turma)
	dep = turma.objects.exclude(classe__name='Alumni').order_by('id')
	context = {
		'group':group,
		'hor':hor,
		'dep':dep,
		'title':"Lista Horario",
		'legend': 'Lista Horario'
	}
	return render(request,'horario/lista_hor_fun.html',context)