from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from funsionariu.models import *
from estudante.models import *
from django.db.models import Sum, Count
from custom.models import *
from Ano.models import * 
from django.db.models import Q
from collections import OrderedDict

@login_required()
def index(request): 
	ano=Ano.objects.filter(is_active=True).first()
	print(ano)
	total_estudante = DetailEst.objects.exclude(Turma_id__classe__name='Alumni').filter(
		Q(Turma_id__classe__name='10 Ano') |
		Q(Turma_id__classe__name='11 Ano') |
		Q(Turma_id__classe__name='12 Ano')
	).count()
	totalProfessores = Funsionariu.objects.all().count()
	totlAlumi=DetailEst.objects.filter(Turma_id__classe__name='Alumni').all().count()
	# totalestudanteMane=Estudante.objects.filter(Sexo='Mane').count()
	# totalestudanteFeto=Estudante.objects.filter(Sexo='Feto').count()
	totalestudanteMane=DetailEst.objects.filter(estudante__Sexo='Mane', Ano_Academinco__ano=ano).count()
	totalestudanteFeto=DetailEst.objects.filter(estudante__Sexo='Feto', Ano_Academinco__ano=ano).count()
	# ano=Ano.objects.order_by('-ano')

	classes = ['10 Ano', '11 Ano', '12 Ano']
	class_gender_counts = OrderedDict()

	for c in classes:
		mane_count = DetailEst.objects.filter(
			Turma__classe__name=c,
			estudante__Sexo='Mane',
			Turma__classe__name__in=classes
		).count()

		feto_count = DetailEst.objects.filter(
			Turma__classe__name=c,
			estudante__Sexo='Feto',
			Turma__classe__name__in=classes
		).count()

		class_gender_counts[c] = {'Mane': mane_count, 'Feto': feto_count}
	print(totalestudanteMane)
	print(totalestudanteFeto)
	context = {
		'homeActive':"active",  
		'totlAlumi' :totlAlumi,
		'total_estudante':total_estudante,
		'totalProfessores':totalProfessores,
		'totalestudanteMane':totalestudanteMane,
		'totalestudanteFeto':totalestudanteFeto,
		# 'loopingestudanteano':loopingestudanteano,
		'class_gender_counts': class_gender_counts,
		}
	return render(request, 'home/index1.html',context)

def homelogin(request):
	return redirect('login')

def home1(request):
	total_estudante = DetailEst.objects.exclude(Turma_id__classe__name='Alumni').filter(
		Q(Turma_id__classe__name='10 Ano') |
		Q(Turma_id__classe__name='11 Ano') |
		Q(Turma_id__classe__name='12 Ano')
	).count()
	totalProfessores = Funsionariu.objects.all().count()
	totlAlumi=DetailEst.objects.filter(Turma_id__classe__name='Alumni').all().count()
	totalestudanteMane=Estudante.objects.filter(Sexo='Mane').count()
	totalestudanteFeto=Estudante.objects.filter(Sexo='Feto').count()
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
	context = {
		'konfigurasaunActive':"active",  
		'totlAlumi' :totlAlumi,
		'total_estudante':total_estudante,
		'totalProfessores':totalProfessores,
		'totalestudanteMane':totalestudanteMane,
		'totalestudanteFeto':totalestudanteFeto,
		'loopingestudanteano':loopingestudanteano,
		
		}
	return render(request,'home/index.html',context)

def test(request):
	classes = ['10 Ano', '11 Ano', '12 Ano']
	class_gender_counts = OrderedDict()

	for c in classes:
		mane_count = DetailEst.objects.filter(
			Turma__classe__name=c,
			estudante__Sexo='Mane',
			Turma__classe__name__in=classes
		).count()

		feto_count = DetailEst.objects.filter(
			Turma__classe__name=c,
			estudante__Sexo='Feto',
			Turma__classe__name__in=classes
		).count()

		class_gender_counts[c] = {'Mane': mane_count, 'Feto': feto_count}

	context = {
		'class_gender_counts': class_gender_counts,
		# Add other context if needed
	}
	return render(request, 'home/index1.html', context)

