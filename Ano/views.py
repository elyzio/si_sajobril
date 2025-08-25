from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from estudante.models import Estudante
from estudante.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.conf import settings
from django.db.models import Sum, Count, Q


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
	
	# Get students who have been transferred out (approved OUT transfers)
	transferred_out_ids = TransferStudent.objects.filter(
		transfer_type='OUT',
		status='APPROVED'
	).values_list('estudante_id', flat=True)
	
	# Get students registered in this year, excluding transferred-out students and alumni
	# First get students from DetailEst to check their current class status
	est_details = DetailEst.objects.filter(
		estudante__Ano_Resisto=tin
	).exclude(
		estudante_id__in=transferred_out_ids
	).exclude(
		Turma__classe__name__icontains='alumni'
	).select_related('estudante').order_by('estudante__Ano_Resisto')
	
	# Extract the Estudante objects
	est = [detail.estudante for detail in est_details]
	
	# Transfer statistics for this specific year
	year_students = Estudante.objects.filter(Ano_Resisto=tin)
	
	# Transfers IN - students who transferred into this school and are in this year
	transfers_in = TransferStudent.objects.filter(
		estudante__Ano_Resisto=tin,
		transfer_type='IN',
		status='APPROVED'
	).count()
	
	# Transfers OUT - students from this year who transferred out
	transfers_out = TransferStudent.objects.filter(
		estudante__Ano_Resisto=tin,
		transfer_type='OUT',
		status='APPROVED'
	).count()
	
	# Pending transfers for this year
	transfers_pending = TransferStudent.objects.filter(
		estudante__Ano_Resisto=tin,
		status='PENDING'
	).count()
	
	# Internal vs External transfers for this year
	internal_transfers = TransferStudent.objects.filter(
		estudante__Ano_Resisto=tin,
		from_turma__isnull=False,
		to_turma__isnull=False,
		status='APPROVED'
	).count()
	
	external_transfers = TransferStudent.objects.filter(
		estudante__Ano_Resisto=tin,
		status='APPROVED'
	).filter(
		Q(from_school__isnull=False) | Q(to_school__isnull=False)
	).count()
	
	# Alumni from this registration year
	alumni_from_year = DetailEst.objects.filter(
		estudante__Ano_Resisto=tin,
		Turma__classe__name__icontains='alumni'
	).count()
	
	# Total students originally from this year
	total_original_students = year_students.count()
	
	# Active students remaining from this year
	active_from_year = len(est)
	
	tinan = Ano.objects.all()
	context = {
		'est': est, 
		'tinan': tinan, 
		'group': group,
		"page": "list",
		'title': f'Lista Estudante - {tin.ano}', 
		'legend': f'Lista Estudante - {tin.ano}',
		'current_year': tin,
		# Transfer statistics
		'transfers_in': transfers_in,
		'transfers_out': transfers_out,
		'transfers_pending': transfers_pending,
		'internal_transfers': internal_transfers,
		'external_transfers': external_transfers,
		'alumni_from_year': alumni_from_year,
		'total_original_students': total_original_students,
		'active_from_year': active_from_year,
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

# Filtered views for year-specific statistics
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director'])
def YearTransferredIn(request, pk):
	group = request.user.groups.all()[0].name 
	tin = get_object_or_404(Ano, pk=pk)
	
	# Get students who transferred IN to this school and are from this registration year
	transferred_in_students = TransferStudent.objects.filter(
		estudante__Ano_Resisto=tin,
		transfer_type='IN',
		status='APPROVED'
	).select_related('estudante')
	
	est = [transfer.estudante for transfer in transferred_in_students]
	tinan = Ano.objects.all()
	
	context = {
		'est': est, 
		'tinan': tinan, 
		'group': group,
		"page": "list",
		'title': f'Students Transferred IN - {tin.ano}', 
		'legend': f'Students Transferred IN - {tin.ano}',
		'current_year': tin,
		'filter_type': 'transferred_in'
	}
	return render(request, 'estudante/lista_estudante.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director'])
def YearTransferredOut(request, pk):
	group = request.user.groups.all()[0].name 
	tin = get_object_or_404(Ano, pk=pk)
	
	# Get students from this year who transferred OUT
	transferred_out_students = TransferStudent.objects.filter(
		estudante__Ano_Resisto=tin,
		transfer_type='OUT',
		status='APPROVED'
	).select_related('estudante')
	
	est = [transfer.estudante for transfer in transferred_out_students]
	tinan = Ano.objects.all()
	
	context = {
		'est': est, 
		'tinan': tinan, 
		'group': group,
		"page": "list",
		'title': f'Students Transferred OUT - {tin.ano}', 
		'legend': f'Students Transferred OUT - {tin.ano}',
		'current_year': tin,
		'filter_type': 'transferred_out'
	}
	return render(request, 'estudante/lista_estudante.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director'])
def YearAlumni(request, pk):
	group = request.user.groups.all()[0].name 
	tin = get_object_or_404(Ano, pk=pk)
	
	# Get alumni from this registration year
	alumni_details = DetailEst.objects.filter(
		estudante__Ano_Resisto=tin,
		Turma__classe__name__icontains='alumni'
	).select_related('estudante')
	
	est = [detail.estudante for detail in alumni_details]
	tinan = Ano.objects.all()
	
	context = {
		'est': est, 
		'tinan': tinan, 
		'group': group,
		"page": "list",
		'title': f'Alumni - {tin.ano}', 
		'legend': f'Alumni - {tin.ano}',
		'current_year': tin,
		'filter_type': 'alumni'
	}
	return render(request, 'estudante/lista_estudante.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director'])
def YearPendingTransfers(request, pk):
	group = request.user.groups.all()[0].name 
	tin = get_object_or_404(Ano, pk=pk)
	
	# Get students with pending transfers from this year
	pending_transfers = TransferStudent.objects.filter(
		estudante__Ano_Resisto=tin,
		status='PENDING'
	).select_related('estudante')
	
	est = [transfer.estudante for transfer in pending_transfers]
	tinan = Ano.objects.all()
	
	context = {
		'est': est, 
		'tinan': tinan, 
		'group': group,
		"page": "list",
		'title': f'Pending Transfers - {tin.ano}', 
		'legend': f'Pending Transfers - {tin.ano}',
		'current_year': tin,
		'filter_type': 'pending_transfers'
	}
	return render(request, 'estudante/lista_estudante.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director'])
def YearAllRegistered(request, pk):
	group = request.user.groups.all()[0].name 
	tin = get_object_or_404(Ano, pk=pk)
	
	# Get all students originally registered in this year
	est = Estudante.objects.filter(Ano_Resisto=tin).order_by('naran')
	tinan = Ano.objects.all()
	
	context = {
		'est': est, 
		'tinan': tinan, 
		'group': group,
		"page": "list",
		'title': f'All Registered Students - {tin.ano}', 
		'legend': f'All Registered Students - {tin.ano}',
		'current_year': tin,
		'filter_type': 'all_registered'
	}
	return render(request, 'estudante/lista_estudante.html', context)




