from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from funsionariu.models import *
from estudante.models import *
from django.db.models import Sum, Count
from custom.models import *
from Ano.models import *
from valor.models import *
from Turma.models import turma

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def listaReport(request):
	Total_estudante=Estudante.objects.all().count()
	totalProfessores = Funsionariu.objects.all().count()
	# Use new Alumni system instead of old Alumni classes
	from estudante.models import AlumniStudent
	totlAlumi=AlumniStudent.objects.filter(status='APPROVED').count()
	totalestudanteMane=Estudante.objects.filter(Sexo='Mane').count()
	totalestudanteFeto=Estudante.objects.filter(Sexo='Feto').count()
	
	print(Total_estudante)

	context = {
		'konfigurasaunActive':"active",  
		'totlAlumi' :totlAlumi,
		'Total_estudante':Total_estudante,
		'totalProfessores':totalProfessores,
		'totalestudanteMane':totalestudanteMane,
		'totalestudanteFeto':totalestudanteFeto,
		
		
		}
	return render(request,'listaRestudante/repotlist.html',context)
@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def listaReportValorClasseJeral(request):
	
	KlasseLista = classe.objects.exclude(name__icontains='alumni').values('name').distinct()
	listperiodu=Periode.objects.all()
	context = {
		'konfigurasaunActive':"active",  
		'KlasseLista':KlasseLista,
		'listperiodu':listperiodu,
		
		}
	return render(request,'listaRestudante/repotlistvalorJeral.html',context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def reporlistaestudante(request):
	group = request.user.groups.all()[0].name
	tin=Ano.objects.order_by('ano')
	cl=classe.objects.order_by('name')
	tur=turma.objects.filter(classe__name='10 Ano')
	tur1=turma.objects.filter(classe__name='11 Ano')
	tur2=turma.objects.filter(classe__name='12 Ano')
	tur3=turma.objects.filter(classe__name='Alumni')
	dep=departamento.objects.order_by('-nome_departamento')
	Total_estudante=Estudante.objects.all().count()
	# Use new Alumni system for active student count
	from estudante.models import AlumniStudent
	approved_alumni_ids = AlumniStudent.objects.filter(status='APPROVED').values_list('estudante_id', flat=True)
	Total_estudante1=Estudante.objects.exclude(id__in=approved_alumni_ids).count()
	totalProfessores = Funsionariu.objects.all().count()
	totalestudanteMane=Estudante.objects.filter(Sexo='Mane').count()
	totalestudanteFeto=Estudante.objects.filter(Sexo='Feto').count()
	totlAlumi=AlumniStudent.objects.filter(status='APPROVED').count()
	loopingturm=[] 
	for tt in tur.iterator():
		tot=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='10 Ano').count()
		loopingturm.append({'id':tt.id,'Turma':tt.Turma,
			'tot':tot,
			})
	loopingturm1=[]
	for tt in tur1.iterator():
		tot1=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='11 Ano').count()
		loopingturm1.append({'id':tt.id,'Turma':tt.Turma,
			'tot1':tot1,
			})
	loopingturm2=[]
	for tt in tur2.iterator():
		tot2=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='12 Ano').count()
		loopingturm2.append({'id':tt.id,'Turma':tt.Turma,
			'tot2':tot2,
			})
	loopingturm3=[]
	for tt in tur3.iterator():
		tot3=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='Alumni').count()
		loopingturm3.append({'id':tt.id,'Turma':tt.Turma,
			'tot3':tot3,
			})
	looping_total_estudante_ano= []	
	for x in tin.iterator() :
		total_sexo_Mane_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id,Sexo="Mane").count()
		total_sexo_Feto_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id,Sexo="Feto").count()
		total_estudante_kada_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id).all().count()
		# total_osanR_kada_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id).aggregate(Sum('Osan_resistu')).get('Osan_resistu__sum')	
		looping_total_estudante_ano.append({'id':x.id,'ano':x.ano,
		'total_sexo_Mane_tinan':total_sexo_Mane_tinan,'total_estudante_kada_tinan':total_estudante_kada_tinan,
		'total_sexo_Feto_tinan':total_sexo_Feto_tinan,\
		# 'total_osanR_kada_tinan':total_osanR_kada_tinan,
		})
	looping_total_estudante_dep= []	
	for x in dep.iterator() :
		total_dep_estuante = DetailEst.objects.filter(Turma_id__classe_id__Departamento_id=x.id).all().count()		
		looping_total_estudante_dep.append({'id':x.id,'nome_departamento':x.nome_departamento,
		'total_dep_estuante':total_dep_estuante,})
	
	context = {
		'group':group,'tin':tin,'cl':cl,'totlAlumi':totlAlumi,'tur':tur,'tur1':tur1,'tur2':tur2,'tur3':tur3,
		'looping_total_estudante_dep':looping_total_estudante_dep,
		'looping_total_estudante_ano':looping_total_estudante_ano,'Total_estudante':Total_estudante1,'totalProfessores':totalProfessores,
		'totalestudanteMane':totalestudanteMane,'totalestudanteFeto':totalestudanteFeto,'loopingturm':loopingturm,'loopingturm1':loopingturm1,\
		'loopingturm2':loopingturm2,'loopingturm3':loopingturm3,
		'title':"LISTA RELATORIU TABULAR ",
	}
	return render(request,'listaRestudante/tab_repor.html',context)
#repot list estudnte print tinan
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def select_estudante_tinan_list(request, pk):
	group = request.user.groups.all()[0].name 
	tin= get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin).all().order_by('Ano_Resisto')
	context = {'est': est, 'tin':tin, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request, 'print/printEstudanteKadaTinan.html', context)
#repot list estudnte print Turma
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','professor'])
def select_estudante_turma_list(request, pk):
	group = request.user.groups.all()[0].name 
	turmaDAta= get_object_or_404(turma, pk=pk)
	estudante10ano = DetailEst.objects.filter(Turma_id=turmaDAta,Turma_id__classe__name='10 Ano').all()
	context = {'estudante10ano': estudante10ano, 'turmaDAta':turmaDAta, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': f'Lista Estudante 10 Ano turma : {turmaDAta.Turma} '
	}
	return render(request, 'print/printEstudanteKadaTurma1o.html', context)

def listValorClassJeral(request, turma_id):
	selected_turma = turma.objects.get(pk=turma_id)

	listPeriod= Periode.objects.all()

	return render(request, 'lista/listaperioduvalorJeral.html',{'listPeriod':listPeriod,\
		'selected_turma':selected_turma,'title':f'{selected_turma.Turma}',\
		
		})

def students_by_turma(request, turma_id, periode_id):
    selected_turma = get_object_or_404(turma, pk=turma_id)
    passing_score = 72
    estudante_ids = valor_est.objects.filter(Turma_id=turma_id, periode_id=periode_id).values_list('estudante_id', flat=True)
    estudantes = Estudante.objects.filter(id__in=estudante_ids)
    estudante_valor_final = [] 
    total_valor_final_sum = 0  # Initialize total sum for average calculation
    total_objects = 13 # Total number of students
    for estudante in estudantes:
        valor_final_sum = valor_est.objects.filter(
            Turma_id=turma_id,
            periode_id=periode_id,
            estudante=estudante
        ).aggregate(Sum('valor_final'))['valor_final__sum'] or 0
        status = 'Aprovado' if valor_final_sum >= passing_score else 'Reprovado'
        # Calculate average valor_final per student
        estudante_valor_final.append({
            'emis': estudante.emis,
            'naran': estudante.naran,
            'Sexo': estudante.Sexo,
            'valor_final_sum': valor_final_sum,
            'status': status,
            'average_valor_final': valor_final_sum / total_objects if total_objects > 0 else 0
        })
        
        total_valor_final_sum += valor_final_sum  # Accumulate valor_final_sum for total sum
    
    # Calculate overall average_valor_final
    average_valor_final = total_valor_final_sum / total_objects if total_objects > 0 else 0
    
    top_3_estudante_valor_final = sorted(estudante_valor_final, key=lambda x: x['valor_final_sum'], reverse=True)[:3]
    passed_count = sum(1 for estudante in estudante_valor_final if estudante['status'] == 'Aprovado')
    not_passed_count = sum(1 for estudante in estudante_valor_final if estudante['status'] == 'Reprovado')
    
    context = {    
        'estudantes': estudantes,
        'top_students': top_3_estudante_valor_final,
        'estudante_valor_final': estudante_valor_final,
        'total_valor_final_sum': total_valor_final_sum,
        'average_valor_final': average_valor_final,
        'selected_turma': selected_turma,
        'passed_count': passed_count,
        'not_passed_count': not_passed_count,
        'legend': f'Lista valores estudantes  Turma: {selected_turma.Turma}'
    }
    
    return render(request, 'print/klasse/printEstudanteKadaTurma1oV.html', context)

def students_by_class(request,periode_id):
    listperiodu = Periode.objects.all()
    passing_score = 72
    estudante_ids = valor_est.objects.filter(Turma_id__classe__name='10 Ano', periode_id=periode_id).values_list('estudante_id', flat=True)
    estudantes = Estudante.objects.filter(id__in=estudante_ids)
    estudante_valor_final = []
    total_valor_final_sum = 0  # Initialize total sum for average calculation
    total_objects = 13 # Total number of students
    for estudante in estudantes:
        valor_final_sum = valor_est.objects.filter(
            Turma_id__classe__name='10 Ano',
            periode_id=periode_id,
            estudante=estudante
        ).aggregate(Sum('valor_final'))['valor_final__sum'] or 0
        status = 'Aprovado' if valor_final_sum >= passing_score else 'Reprovado'
        # Calculate average valor_final per student
        estudante_valor_final.append({
            'emis': estudante.emis,
            'naran': estudante.naran,
            'Sexo': estudante.Sexo,
            'valor_final_sum': valor_final_sum,
            'status': status,
            'average_valor_final': valor_final_sum / total_objects if total_objects > 0 else 0
        })
        
        total_valor_final_sum += valor_final_sum  # Accumulate valor_final_sum for total sum
    
    # Calculate overall average_valor_final
    average_valor_final = total_valor_final_sum / total_objects if total_objects > 0 else 0
    
    top_3_estudante_valor_final = sorted(estudante_valor_final, key=lambda x: x['valor_final_sum'], reverse=True)[:10]
    passed_count = sum(1 for estudante in estudante_valor_final if estudante['status'] == 'Aprovado')
    not_passed_count = sum(1 for estudante in estudante_valor_final if estudante['status'] == 'Reprovado')
    
    context = {    
        'estudantes': estudantes,
        'top_students': top_3_estudante_valor_final,
        'estudante_valor_final': estudante_valor_final,
        'total_valor_final_sum': total_valor_final_sum,
        'average_valor_final': average_valor_final,
        # 'selected_turma': selected_turma,
        'passed_count': passed_count,
        'not_passed_count': not_passed_count,
        'legend': f'Lista valores estudantes top 10 iha 10 Ano'
    }
    
    return render(request, 'print/klasse/printEstudanteKadaKlasse.html', context)
def students_by_class1(request,periode_id):
    listperiodu = Periode.objects.all()
    passing_score = 72
    estudante_ids = valor_est.objects.filter(Turma_id__classe__name='11 Ano',periode_id=periode_id).values_list('estudante_id', flat=True)
    estudantes = Estudante.objects.filter(id__in=estudante_ids)
    estudante_valor_final = []
    total_valor_final_sum = 0  # Initialize total sum for average calculation
    total_objects = 13 # Total number of students
    for estudante in estudantes:
        valor_final_sum = valor_est.objects.filter(
            Turma_id__classe__name='11 Ano',
            periode_id=periode_id,
            estudante=estudante
        ).aggregate(Sum('valor_final'))['valor_final__sum'] or 0
        status = 'Aprovado' if valor_final_sum >= passing_score else 'Reprovado'
        # Calculate average valor_final per student
        estudante_valor_final.append({
            'emis': estudante.emis,
            'naran': estudante.naran,
            'Sexo': estudante.Sexo,
            'valor_final_sum': valor_final_sum,
            'status': status,
            'average_valor_final': valor_final_sum / total_objects if total_objects > 0 else 0
        })
        
        total_valor_final_sum += valor_final_sum  # Accumulate valor_final_sum for total sum
    
    # Calculate overall average_valor_final
    average_valor_final = total_valor_final_sum / total_objects if total_objects > 0 else 0
    
    top_3_estudante_valor_final = sorted(estudante_valor_final, key=lambda x: x['valor_final_sum'], reverse=True)[:10]
    passed_count = sum(1 for estudante in estudante_valor_final if estudante['status'] == 'Aprovado')
    not_passed_count = sum(1 for estudante in estudante_valor_final if estudante['status'] == 'Reprovado')
    
    context = {    
        'estudantes': estudantes,
        'top_students': top_3_estudante_valor_final,
        'estudante_valor_final': estudante_valor_final,
        'total_valor_final_sum': total_valor_final_sum,
        'average_valor_final': average_valor_final,
        # 'selected_turma': selected_turma,
        'passed_count': passed_count,
        'not_passed_count': not_passed_count,
        'legend': f'Lista valores estudantes Top 10 iha 11 Ano',
    }
    
    return render(request, 'print/klasse/printEstudanteKadaKlasse.html', context)
def students_by_class2(request,periode_id):
    listperiodu = Periode.objects.all()
    passing_score = 72
    estudante_ids = valor_est.objects.filter(Turma_id__classe__name='12 Ano', periode_id=periode_id).values_list('estudante_id', flat=True)
    estudantes = Estudante.objects.filter(id__in=estudante_ids)
    estudante_valor_final = []
    total_valor_final_sum = 0  # Initialize total sum for average calculation
    total_objects = 13 # Total number of students
    for estudante in estudantes:
        valor_final_sum = valor_est.objects.filter(
            Turma_id__classe__name='12 Ano',
            periode_id=periode_id,
            estudante=estudante
        ).aggregate(Sum('valor_final'))['valor_final__sum'] or 0
        status = 'Aprovado' if valor_final_sum >= passing_score else 'Reprovado'
        # Calculate average valor_final per student
        estudante_valor_final.append({
            'emis': estudante.emis,
            'naran': estudante.naran,
            'Sexo': estudante.Sexo,
            'valor_final_sum': valor_final_sum,
            'status': status,
            'average_valor_final': valor_final_sum / total_objects if total_objects > 0 else 0
        })
        
        total_valor_final_sum += valor_final_sum  # Accumulate valor_final_sum for total sum
    
    # Calculate overall average_valor_final
    average_valor_final = total_valor_final_sum / total_objects if total_objects > 0 else 0
    
    top_3_estudante_valor_final = sorted(estudante_valor_final, key=lambda x: x['valor_final_sum'], reverse=True)[:10]
    passed_count = sum(1 for estudante in estudante_valor_final if estudante['status'] == 'Aprovado')
    not_passed_count = sum(1 for estudante in estudante_valor_final if estudante['status'] == 'Reprovado')
    
    context = {    
        'estudantes': estudantes,
        'top_students': top_3_estudante_valor_final,
        'estudante_valor_final': estudante_valor_final,
        'total_valor_final_sum': total_valor_final_sum,
        'average_valor_final': average_valor_final,
        # 'selected_turma': selected_turma,
        'passed_count': passed_count,
        'not_passed_count': not_passed_count,
        'legend': f'Lista valores estudantes Top 10 iha 12 Ano '
    }
    
    return render(request, 'print/klasse/printEstudanteKadaKlasse.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','professor'])
def select_estudante_turma1_list(request, pk):
	group = request.user.groups.all()[0].name 
	turmaDAta= get_object_or_404(turma, pk=pk)
	estudante11ano = DetailEst.objects.filter(Turma_id=turmaDAta,Turma_id__classe__name='11 Ano').all()
	context = {'estudante11ano': estudante11ano, 'turmaDAta':turmaDAta, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': f'Lista Estudante 11 Ano turma : {turmaDAta.Turma} '
	}
	return render(request, 'print/printEstudanteKadaTurma11.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','professor'])
def select_estudante_turma2_list(request, pk):
	group = request.user.groups.all()[0].name 
	turmaDAta= get_object_or_404(turma, pk=pk)
	estudante12ano = DetailEst.objects.filter(Turma_id=turmaDAta,Turma_id__classe__name='12 Ano').all()
	context = {'estudante12ano': estudante12ano, 'turmaDAta':turmaDAta, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': f'Lista Estudante 12 Ano turma : {turmaDAta.Turma} '
	}
	return render(request, 'print/printEstudanteKadaTurma12.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def select_estudante_tinan_list_Mane(request, pk):
	group = request.user.groups.all()[0].name 
	tin= get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin, Sexo="Mane").all().order_by('naran')
	# tinan = Ano.objects.all()
	context = {'est': est, 'tin':tin, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request, 'print/printEstudanteKadaTinanM.html', context)
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario'])
def select_estudante_tinan_list_feto(request, pk):
	group = request.user.groups.all()[0].name 
	tin= get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin, Sexo="Feto").all().order_by('naran')
	context = {'est': est, 'tin':tin, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request, 'print/printEstudanteKadaTinanF.html', context)

#repot list estudnte print  osan kada tinan
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def select_estudante_osan_tinan_list(request, pk):
	group = request.user.groups.all()[0].name 
	tin= get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin).all().order_by('Ano_Resisto')
	est_count = Estudante.objects.filter(Ano_Resisto=tin).all().aggregate(Sum('Osan_resistu')).get('Osan_resistu__sum')
	tinan = Ano.objects.all()
	context = {'est': est, 'tin':tin, 'group': group,"page":"list",
		'est_count':est_count,
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request, 'print/printEstudanteOsanKadaTinan.html', context)
@login_required
@allowed_users(allowed_roles=['admin','Director','Secretario','kurikulum','professor'])
def EReportListActiveEstudanteAlumiprint(request):
	group = request.user.groups.all()[0].name
	objects = DetailEst.objects.filter(Turma_id__classe__name='Alumi')

	context ={
		"title":f"Pajina Relatoriu Lista Estudnate",
		"group":group,
		"report_active":"active",
		"objects":objects,
		
	}
	return render(request, "print/listActiveEstudanteClasseAlumiPrint.html",context)

@login_required
@allowed_users(allowed_roles=['admin','Director','Secretario','kurikulum','professor'])
def ListaEstudanteAlumi(request):
	group = request.user.groups.all()[0].name
	# Use new Alumni system instead of old Alumni classes
	from estudante.models import AlumniStudent
	alumni_records = AlumniStudent.objects.filter(status='APPROVED').select_related('estudante')

	context ={
		"title":f"Pajina Relatoriu Lista Estudante Alumni",
		"report_active":"active",
		"objects":alumni_records,  # Pass alumni records instead of DetailEst objects
		'group': group,
		"page":"list",
		
	}
	return render(request, "lista/listEstudanteAlumi.html",context)

#report Grafiku
@login_required()
def report_shart(request):
	group = request.user.groups.all()[0].name
	estudante = Estudante.objects.all()
	Total_estudante=Estudante.objects.all().count() 
	totalestudanteMane=Estudante.objects.filter(Sexo='Mane').count()
	totalestudanteFeto=Estudante.objects.filter(Sexo='Feto').count()
	totalProfessoresFeto=Funsionariu.objects.filter(Sexo='Feto').count()
	totalProfessoresM=Funsionariu.objects.filter(Sexo='Mane').count()
	ano=Ano.objects.order_by('-ano')
	#loping turma
	turM= turma.objects.all()
	# .....................luping estudante kada munisipiu..........................
	data_class=classe.objects.all()
	loopingestudanteano= []	
	for x in ano.iterator() :
		total_sexo_Mane_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id,Sexo="Mane").count()
		total_sexo_Feto_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id,Sexo="Feto").count()
		loopingestudanteano.append({'id':x.id,'ano':x.ano,
		'total_sexo_Mane_tinan':total_sexo_Mane_tinan,'total_sexo_Feto_tinan':total_sexo_Feto_tinan,})

	data_mun=Municipality.objects.all()
	loopingestudantesexo = []
	for ii in data_mun.iterator():
		total_sexo_Mane = Estudante.objects.filter(municipality_id=ii.id, Sexo="Mane").count()
		total_Sexo_Feto = Estudante.objects.filter(municipality_id=ii.id,Sexo="Feto").count()
		total_estudante=Estudante.objects.filter(municipality_id=ii.id).all().count()
		loopingestudantesexo.append({'id':ii.id,'name':ii.name,
			'total_sexo_Mane':total_sexo_Mane,'total_estudante':total_estudante,"total_Sexo_Feto":total_Sexo_Feto,})

	loopingturm=[] 
	for tt in turM.iterator():
		tot=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='10 Ano').count()
		tot1=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='11 Ano').count()
		tot2=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='12 Ano').count()
		tot3=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='Alumni').count()
		loopingturm.append({'id':tt.id,'Turma':tt.Turma,
			'tot':tot,
			'tot1':tot1,
			'tot2':tot2,
			'tot3':tot3,
			})

#LOOPING DEPARTAMENTO
	data_tin=Ano.objects.all()
	data_programa=departamento.objects.all()
	loopingestudantesProgrm=[]
	for x in data_tin.iterator():
		total_estudantesCt = DetailEst.objects.filter(estudante_id__Ano_Resisto_id=x.id,Turma_id__classe_id__Departamento__nome_departamento='Ciencias e Tecnologia').all().count()
		total_estudantesCsh = DetailEst.objects.filter(estudante_id__Ano_Resisto_id=x.id,Turma_id__classe_id__Departamento__nome_departamento='Ciensias Sociais e Humanidade').all().count()
		total_estudante= DetailEst.objects.filter(estudante_id__Ano_Resisto_id=x.id).all().count()
		loopingestudantesProgrm.append({'id':x.id,'ano':x.ano,
			'total_estudantesCt':total_estudantesCt,
			'total_estudantesCsh':total_estudantesCsh,
			'total_estudante':total_estudante,
			})

	dict = {
		"title":"Sistema Informasaun Akademika Escola Colegio de Santo Inacio de Loiola ",
		'konfigurasaunActive':"active",
		'loopingestudanteano':loopingestudanteano,'totalestudanteMane':totalestudanteMane,
		'totalestudanteFeto':totalestudanteFeto,
		'Total_estudante':Total_estudante,
		'totalProfessoresFeto':totalProfessoresFeto,'turM':turM,
		'totalProfessoresM':totalProfessoresM,
		'Total_estudante':Total_estudante,
		"data_mun":data_mun,
		"loopingestudantesexo":loopingestudantesexo,'loopingturm':loopingturm,'loopingestudantesProgrm':loopingestudantesProgrm,
		'group': group,
	}
	return render(request, 'listaRestudante/shart_report.html',context=dict)

#report Grafiku alumni
@login_required()
def report_shartAlumni(request):
	group = request.user.groups.all()[0].name
	from estudante.models import AlumniStudent
	
	# Use new Alumni system
	estudante = Estudante.objects.all()
	Total_estudante = DetailEst.objects.all().count() 
	
	# Get Alumni statistics by gender using new system
	approved_alumni = AlumniStudent.objects.filter(status='APPROVED').select_related('estudante')
	totalestudanteMane = approved_alumni.filter(estudante__Sexo='Mane').count()
	totalestudanteFeto = approved_alumni.filter(estudante__Sexo='Feto').count()
	ano = Ano.objects.order_by('-ano')

	# Remove old alumni turma references
	# tur3=turma.objects.filter(classe__name='Alumni')
	# .....................luping estudante kada munisipiu..........................
	data_class=classe.objects.all()
	loopingestudanteano= []	
	for x in ano.iterator():
		# Use new Alumni system for year-based statistics
		total_sexo_Mane_tinan = AlumniStudent.objects.filter(
			estudante__Ano_Resisto_id=x.id,
			estudante__Sexo="Mane",
			status='APPROVED'
		).count()
		total_sexo_Feto_tinan = AlumniStudent.objects.filter(
			estudante__Ano_Resisto_id=x.id,
			estudante__Sexo="Feto",
			status='APPROVED'
		).count()
		loopingestudanteano.append({'id':x.id,'ano':x.ano,
		'total_sexo_Mane_tinan':total_sexo_Mane_tinan,'total_sexo_Feto_tinan':total_sexo_Feto_tinan,})

	data_mun=Municipality.objects.all()
	loopingestudantesexo = []
	for ii in data_mun.iterator():
		total_sexo_Mane = AlumniStudent.objects.filter(estudante__municipality_id=ii.id, estudante__Sexo="Mane", status='APPROVED').count()
		total_Sexo_Feto = AlumniStudent.objects.filter(estudante__municipality_id=ii.id, estudante__Sexo="Feto", status='APPROVED').count()
		total_estudante = AlumniStudent.objects.filter(estudante__municipality_id=ii.id, status='APPROVED').count()
		loopingestudantesexo.append({'id':ii.id,'name':ii.name,
			'total_sexo_Mane':total_sexo_Mane,'total_estudante':total_estudante,"total_Sexo_Feto":total_Sexo_Feto,})

#LOOPING DEPARTAMENTO
	data_tin=Ano.objects.all()
	data_programa=departamento.objects.all()
	loopingestudantesProgrm=[]
	for x in data_tin.iterator():
		total_estudantesCt = AlumniStudent.objects.filter(estudante__Ano_Resisto_id=x.id, status='APPROVED', completed_turma__classe__Departamento__nome_departamento='Ciencias e Tecnologia').count()
		total_estudantesCsh = AlumniStudent.objects.filter(estudante__Ano_Resisto_id=x.id, status='APPROVED', completed_turma__classe__Departamento__nome_departamento='Ciensias Sociais e Humanidade').count()
		total_estudante = AlumniStudent.objects.filter(estudante__Ano_Resisto_id=x.id, status='APPROVED').count()
		loopingestudantesProgrm.append({'id':x.id,'ano':x.ano,
			'total_estudantesCt':total_estudantesCt,
			'total_estudantesCsh':total_estudantesCsh,
			'total_estudante':total_estudante,
			})

	dict = {
		"title":"Sistema Informasaun Akademika Escola Secundario Colegio santo Inacio de Loiola",
		'konfigurasaunActive':"active",
		'loopingestudanteano':loopingestudanteano,'totalestudanteMane':totalestudanteMane,
		'totalestudanteFeto':totalestudanteFeto,
		'Total_estudante':Total_estudante,
		"data_mun":data_mun,
		"loopingestudantesexo":loopingestudantesexo,'loopingestudantesProgrm':loopingestudantesProgrm,
		'group': group,
	}
	return render(request, 'listaRestudante/shart_reportAlumni.html',context=dict)

#report Tabular alumni
@login_required()
def report_TabularAlumni(request):
	group = request.user.groups.all()[0].name
	from estudante.models import AlumniStudent
	
	# Use new Alumni system
	estudante = Estudante.objects.all()
	Total_estudante = DetailEst.objects.all().count() 
	
	# Get Alumni statistics by gender using new system
	approved_alumni = AlumniStudent.objects.filter(status='APPROVED').select_related('estudante')
	totalestudanteMane = approved_alumni.filter(estudante__Sexo='Mane').count()
	totalestudanteFeto = approved_alumni.filter(estudante__Sexo='Feto').count()
	ano = Ano.objects.order_by('-ano')
	
	# Remove old alumni turma references
	# tur3=turma.objects.filter(classe__name='Alumni')
	# .....................luping estudante kada munisipiu..........................
	data_class=classe.objects.all()
	loopingestudanteano= []	
	for x in ano.iterator():
		# Use new Alumni system for year-based statistics
		total_sexo_Mane_tinan = AlumniStudent.objects.filter(
			estudante__Ano_Resisto_id=x.id,
			estudante__Sexo="Mane",
			status='APPROVED'
		).count()
		total_sexo_Feto_tinan = AlumniStudent.objects.filter(
			estudante__Ano_Resisto_id=x.id,
			estudante__Sexo="Feto",
			status='APPROVED'
		).count()
		loopingestudanteano.append({'id':x.id,'ano':x.ano,
		'total_sexo_Mane_tinan':total_sexo_Mane_tinan,'total_sexo_Feto_tinan':total_sexo_Feto_tinan,})

	data_mun=Municipality.objects.all()
	loopingestudantesexo = []
	for ii in data_mun.iterator():
		total_sexo_Mane = AlumniStudent.objects.filter(estudante__municipality_id=ii.id, estudante__Sexo="Mane", status='APPROVED').count()
		total_Sexo_Feto = AlumniStudent.objects.filter(estudante__municipality_id=ii.id, estudante__Sexo="Feto", status='APPROVED').count()
		total_estudante = AlumniStudent.objects.filter(estudante__municipality_id=ii.id, status='APPROVED').count()
		loopingestudantesexo.append({'id':ii.id,'name':ii.name,
			'total_sexo_Mane':total_sexo_Mane,'total_estudante':total_estudante,"total_Sexo_Feto":total_Sexo_Feto,})

	# Remove old Alumni turma loops since we're using new Alumni system
	# loopingturm3=[]
	# for tt in tur3.iterator():
	#	tot3=DetailEst.objects.filter(Turma_id=tt.id,Turma_id__classe__name='Alumni').count()
	#	loopingturm3.append({'id':tt.id,'Turma':tt.Turma,
	#		'tot3':tot3,
	#		})
#LOOPING DEPARTAMENTO
	data_tin=Ano.objects.all()
	data_programa=departamento.objects.all()
	loopingestudantesProgrm=[]
	for x in data_tin.iterator():
		total_estudantesCt = AlumniStudent.objects.filter(estudante__Ano_Resisto_id=x.id, status='APPROVED', completed_turma__classe__Departamento__nome_departamento='Ciencias e Tecnologia').count()
		total_estudantesCsh = AlumniStudent.objects.filter(estudante__Ano_Resisto_id=x.id, status='APPROVED', completed_turma__classe__Departamento__nome_departamento='Ciensias Sociais e Humanidade').count()
		total_estudante = AlumniStudent.objects.filter(estudante__Ano_Resisto_id=x.id, status='APPROVED').count()
		loopingestudantesProgrm.append({'id':x.id,'ano':x.ano,
			'total_estudantesCt':total_estudantesCt,
			'total_estudantesCsh':total_estudantesCsh,
			'total_estudante':total_estudante,
			})

	dict = {
		"title":"Sistema Informasaun Akademiku Escola Secundario Colegio Santo de Inacio de Loiola ",
		'konfigurasaunActive':"active",
		'loopingestudanteano':loopingestudanteano,'totalestudanteMane':totalestudanteMane,
		'totalestudanteFeto':totalestudanteFeto,
		'Total_estudante':Total_estudante,
		"data_mun":data_mun,
		"loopingestudantesexo":loopingestudantesexo,'loopingestudantesProgrm':loopingestudantesProgrm,
		'group': group,
	}
	return render(request, 'listaRestudante/tab_reportAlumni.html',context=dict)


#report Tabular Professores
@login_required()
def report_TabularProf(request):
	group = request.user.groups.all()[0].name
	totalProfessores=Funsionariu.objects.all().count() 
	TotalProfessoresM=Funsionariu.objects.filter(Sexo='Mane').count()
	TotalProfessora=Funsionariu.objects.filter(Sexo='Feto').count()
	# .....................luping estudante kada munisipiu..........................
	data_mun=Municipality.objects.all()
	loopingProfessoresMun = []
	for ii in data_mun.iterator():
		total_sexo_Mane = Funsionariu.objects.filter(municipality_id=ii.id, Sexo="Mane").count()
		total_Sexo_Feto = Funsionariu.objects.filter(municipality_id=ii.id,Sexo="Feto").count()
		totalProfessores=Funsionariu.objects.filter(municipality_id=ii.id).all().count()
		loopingProfessoresMun.append({'id':ii.id,'name':ii.name,
			'total_sexo_Mane':total_sexo_Mane,'totalProfessores':totalProfessores,"total_Sexo_Feto":total_Sexo_Feto,})
	data_Dep=DepFun.objects.all()
	loopingProfDep=[]
	for ii in data_Dep.iterator():
		# TMane=Funsionariu.objects.filter(departamento_id=ii.id , Sexo="Mane").count()
		# TFeto=Funsionariu.objects.filter(departamento_id=ii.id , Sexo="Feto").count()
		Total=Funsionariu.objects.filter(departamento_id=ii.id ).count()
		loopingProfDep.append({'id':ii.id,'name':ii.name,
			'Total':Total,
			})


	dict = {
		"title":"Sistema Informasaun Akademiku Escola Secundario Colegio Santo de Inacio de Loiola ",
		'konfigurasaunActive':"active",
		'TotalProfessoresM':TotalProfessoresM,
		'TotalProfessora':TotalProfessora,
		'totalProfessores':totalProfessores,
		"data_mun":data_mun,
		"loopingProfessoresMun":loopingProfessoresMun,
		"loopingProfDep":loopingProfDep,
		'group': group,
	}
	return render(request, 'listaRestudante/tab_reportProfessores.html',context=dict)
	
@login_required()
def shartMunisipiu(request):
	estudante = Estudante.objects.all()
	data_mun=Municipality.objects.all()
	loopingestudantesexo = []
	for ii in data_mun.iterator():
		total_sexo_Mane = Estudante.objects.filter(municipality_id=ii.id, Sexo="Mane").count()
		total_Sexo_Feto = Estudante.objects.filter(municipality_id=ii.id,Sexo="Feto").count()
		total_estudante=Estudante.objects.filter(municipality_id=ii.id).all().count()
		loopingestudantesexo.append({'id':ii.id,'name':ii.name,
			'total_sexo_Mane':total_sexo_Mane,'total_estudante':total_estudante,"total_Sexo_Feto":total_Sexo_Feto,})
	dict = {
		"data_mun":data_mun,
		"loopingestudantesexo":loopingestudantesexo,

	}
	return render(request, 'listaRestudante/shart_report_munisipiu.html',dict)

@login_required()
def shartvalor(request):
	estudante = Estudante.objects.all()
	list_valor = valor_est.objects.filter(periode__nome_periode='I Periodu', Turma_id__classe__name='10 Ano')
	sum_valor_final = valor_est.objects.filter(periode__nome_periode='I Periodu',Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	if media<=6:
		dis=media.count()
	else :
		dis= float(0)
		print( "media",dis) 

	dict = {
		
		"sum_valor_final":sum_valor_final,
		"media":media,
		"dis":dis,
		# "lopingvalor":lopingvalor,

	}
	return render(request, 'listaRestudante/shart_valor.html',dict)
# Repot SHART GRAFIK PROPINAS KADA TINAN KODING
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum'])
def repor_tb_propinas(request):
	group = request.user.groups.all()[0].name
	tin=Ano.objects.order_by('ano')
	pro=propinas.objects.all()

	looping_total_estudante_propinas_tin= []	
	for x in tin.iterator() :
		total_propinas_per_ano=propinas.objects.filter(tinan_id=x.id).aggregate(Sum('total')).get('total__sum')

		looping_total_estudante_propinas_tin.append({'id':x.id,'ano':x.ano,
		'total_propinas_per_ano':total_propinas_per_ano,
		})
	context = {
		'group':group,
		'tin':tin,
		'pro':pro,
		'looping_total_estudante_propinas_tin':looping_total_estudante_propinas_tin,
		'title':"LISTA REPORT TABULAR PROPINAS ",
	}
	return render(request,'listaRestudante/shartpropinas.html',context)

# VALOR ESTUDANTE TUIR TURMA NIA  KODIGU SELECT
@login_required
@allowed_users(allowed_roles=['admin','kurikulum','Director','professor'])
def select_estudante_turma_listValor1(request, pk):
	group = request.user.groups.all()[0].name 
	turmaDAta= get_object_or_404(turma, pk=pk)
	vl_detail = Estudante.objects.all()
	valorEstudante1 = DetailEst.objects.filter(Turma_id=turmaDAta,Turma_id__classe__name='10 Ano').all()
	context = {'valorEstudante1': valorEstudante1, 'turmaDAta':turmaDAta, 'group': group,"page":"list",
		'vl_detail':vl_detail,
		'title': 'Lista Estudante', 'legend': f'Lista Valor Estudante 10 Ano turma : {turmaDAta.Turma} '
	}
	return render(request, 'print/valor/valor1.html', context)

@login_required
@allowed_users(allowed_roles=['admin','kurikulum','Director','professor'])
def select_estudante_turma_listValor2(request, pk):
	group = request.user.groups.all()[0].name 
	turmaDAta= get_object_or_404(turma, pk=pk)
	valorEstudante2 = DetailEst.objects.filter(Turma_id=turmaDAta,Turma_id__classe__name='11 Ano').all()
	context = {'valorEstudante2': valorEstudante2, 'turmaDAta':turmaDAta, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': f'Lista Estudante 11 Ano turma : {turmaDAta.Turma} '
	}
	return render(request, 'print/valor/valor2.html', context)
@login_required
@allowed_users(allowed_roles=['admin','kurikulum','Director'])
def select_estudante_turma_listValor3(request, pk):
	group = request.user.groups.all()[0].name 
	turmaDAta= get_object_or_404(turma, pk=pk)
	valorEstudante3 = DetailEst.objects.filter(Turma_id=turmaDAta,Turma_id__classe__name='12 Ano').all()
	context = {'valorEstudante3': valorEstudante3, 'turmaDAta':turmaDAta, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': f'Lista Estudante 12 Ano turma : {turmaDAta.Turma} '
	}
	return render(request, 'print/valor/valor3.html', context)
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def ReportValorEstudantePeriod_Print(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='I Periodu', Turma_id__classe__name='10 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='I Periodu',Klasse__name='10 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='I Periodu',  Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",
	}
	return render(request, "print/valor/pritValor1.html",context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def ReportValorEstudanteIIPeriod_Print(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='II Periodu', Turma_id__classe__name='10 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='II Periodu',Klasse__name='10 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='II Periodu',  Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",'legend': f'Segundo Periode ',
	}
	return render(request, "print/valor/printvalor1peroioduII.html",context)
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def ReportValorEstudanteIIIPeriod_Print(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='III Periodu', Turma_id__classe__name='10 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='III Periodu',Klasse__name='10 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='III Periodu',  Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"III PERIODE",
	}
	return render(request, "print/valor/printvalor1peroioduIII.html",context)

	# KODIGU PRINT 11 ANO
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def ReportValorEstudantePeriod_Print11ano(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	# period = get_object_or_404(Periode,id=idPeriodu)
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='I Periodu', Turma_id__classe__name='11 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='I Periodu',Klasse__name='11 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='I Periodu',  Turma_id__classe__name='11 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",
	}
	return render(request, "print/valor/11Ano/Iperiodu.html",context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum'])
def ReportValorEstudanteIIPeriod_Print11ano(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='II Periodu', Turma_id__classe__name='11 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='II Periodu',Klasse__name='11 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='II Periodu',  Turma_id__classe__name='11 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",'legend': f'Segundo Periode ',
	}
	return render(request, "print/valor/11Ano/IIperiodu.html",context)
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def ReportValorEstudanteIIIPeriod_Print11ano(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='III Periodu', Turma_id__classe__name='11 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='III Periodu',Klasse__name='11 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='III Periodu',  Turma_id__classe__name='11 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"III PERIODE",
	}
	return render(request, "print/valor/11Ano/IIIperiodu.html",context)
# KODIGU PRINT 12 ANO
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def ReportValorEstudantePeriod_Print12ano(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	# period = get_object_or_404(Periode,id=idPeriodu)
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='I Periodu', Turma_id__classe__name='12 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='I Periodu',Klasse__name='12 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='I Periodu',  Turma_id__classe__name='12 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",
	}
	return render(request, "print/valor/12Ano/Iperiodu.html",context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def ReportValorEstudanteIIPeriod_Print12ano(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='II Periodu', Turma_id__classe__name='12 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='II Periodu',Klasse__name='12 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='II Periodu',  Turma_id__classe__name='12 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",'legend': f'Segundo Periode ',
	}
	return render(request, "print/valor/12Ano/IIperiodu.html",context)
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def ReportValorEstudanteIIIPeriod_Print12ano(request,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode__nome_periode='III Periodu', Turma_id__classe__name='12 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode__nome_periode='III Periodu',Klasse__name='12 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode__nome_periode='III Periodu',  Turma_id__classe__name='12 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"III PERIODE",
	}
	return render(request, "print/valor/12Ano/IIIperiodu.html",context)