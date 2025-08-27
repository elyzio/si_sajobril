from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from valor.models import *
from Turma.models import *
from .forms import *
from custom.utils import *
from custom.models import *
from departamento.models import departamento
from funsionariu.models import FunsionarioTurma, Funsionariu
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.conf import settings
from .filters import estFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User,Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def Listaestudante(request):
	group = request.user.groups.all()[0].name
	# Exclude students who have been transferred out (approved OUT transfers) or are alumni
	transferred_out_students = TransferStudent.objects.filter(
		transfer_type='OUT', 
		status='APPROVED'
	).values_list('estudante_id', flat=True)
	
	alumni_students = AlumniStudent.objects.filter(
		status='APPROVED'
	).values_list('estudante_id', flat=True)
	
	excluded_students = set(list(transferred_out_students) + list(alumni_students))
	est = Estudante.objects.exclude(id__in=excluded_students)		
	
	# Add alumni eligibility check for each student
	from valor.models import valor_est
	ano_act = Ano.objects.filter(is_active=True).first()
	
	for student in est:
		# Get student's current active class
		current_detail = DetailEst.objects.filter(
			estudante=student,
			is_active=True,
			Ano_Academinco=ano_act
		).first()
		
		# Count grades for each period separately
		grades_periodo_1 = valor_est.objects.filter(
			estudante=student,
			Tinan_periode=ano_act,
			periode__nome_periode='I Periodu'
		).count()
		
		grades_periodo_2 = valor_est.objects.filter(
			estudante=student,
			Tinan_periode=ano_act,
			periode__nome_periode='II Periodu'
		).count()
		
		grades_periodo_3 = valor_est.objects.filter(
			estudante=student,
			Tinan_periode=ano_act,
			periode__nome_periode='III Periodu'
		).count()
		
		total_grades = grades_periodo_1 + grades_periodo_2 + grades_periodo_3
		
		# Check all conditions for alumni eligibility
		is_12_ano = current_detail and current_detail.Turma.classe.name == '12 Ano' if current_detail else False
		has_all_periods_complete = (grades_periodo_1 >= 13 and 
									grades_periodo_2 >= 13 and 
									grades_periodo_3 >= 13)
		
		student.is_alumni_eligible = is_12_ano and has_all_periods_complete
		student.total_grades = total_grades
		student.grades_periodo_1 = grades_periodo_1
		student.grades_periodo_2 = grades_periodo_2
		student.grades_periodo_3 = grades_periodo_3
		student.current_class = current_detail.Turma.classe.name if current_detail else 'No Class'
		student.is_12_ano = is_12_ano
		student.has_all_periods_complete = has_all_periods_complete
	
	deps = departamento.objects.all().order_by('id')
	tinan = Ano.objects.all()
	# Exclude old Alumni classes from the filter buttons
	KlasseLista = classe.objects.exclude(name__icontains='alumni').distinct().values('name').all()
	Klasse = list()
	for a in KlasseLista:
		getClasse = classe.objects.filter(name=a['name']).exclude(name__icontains='alumni').last()
		if getClasse:  # Only add if class exists after filtering
			Klasse.append(getClasse)
	context = {
        'rejDadus':'active',
        'rejDadus2':'in active',
		# 'est':est, 
		'Klasse':Klasse,
		'est':est, 'deps': deps, 'group': group, 'tinan': tinan,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request,'estudante/lista_estudante.html',context)

@login_required
@allowed_users(allowed_roles=['admin', 'Tesoreira','Director','Secretario','kurikulum','professor'])
def ListEstudanteClass(request, id):
    group = request.user.groups.all()[0].name
    ano_act = Ano.objects.filter(is_active=True).first()
    
    # Prevent access to old Alumni classes
    if 'alumni' in id.lower():
        messages.error(request, 'Old Alumni classes are no longer accessible. Please use the new Alumni system.')
        return redirect('Listaestudante')
    
    klasse = classe.objects.filter(name=id).exclude(name__icontains='alumni').last()
    if not klasse:
        messages.error(request, f'Class "{id}" not found or is an old Alumni class.')
        return redirect('Listaestudante')
        
    # Exclude old Alumni classes from the filter buttons
    KlasseLista = classe.objects.exclude(name__icontains='alumni').distinct().values('name').all()
    KlasseList = list()
    for a in KlasseLista:
        getClasse = classe.objects.filter(name=a['name']).exclude(name__icontains='alumni').last()
        if getClasse:  # Only add if class exists after filtering
            KlasseList.append(getClasse)
    # Exclude students who have been transferred out (approved OUT transfers) or are alumni
    transferred_out_students = TransferStudent.objects.filter(
        transfer_type='OUT', 
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    alumni_students = AlumniStudent.objects.filter(
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    excluded_students = set(list(transferred_out_students) + list(alumni_students))
    est = DetailEst.objects.filter(
        Turma_id__classe__name=klasse.name,
        is_active=True,
        Ano_Academinco=ano_act
    ).exclude(estudante_id__in=excluded_students).order_by('estudante__naran')
    
    # Add alumni eligibility check for each student
    from valor.models import valor_est
    for detail_est in est:
        student = detail_est.estudante
        
        # Count grades for each period separately
        grades_periodo_1 = valor_est.objects.filter(
            estudante=student,
            Tinan_periode=ano_act,
            periode__nome_periode='I Periodu'
        ).count()
        
        grades_periodo_2 = valor_est.objects.filter(
            estudante=student,
            Tinan_periode=ano_act,
            periode__nome_periode='II Periodu'
        ).count()
        
        grades_periodo_3 = valor_est.objects.filter(
            estudante=student,
            Tinan_periode=ano_act,
            periode__nome_periode='III Periodu'
        ).count()
        
        total_grades = grades_periodo_1 + grades_periodo_2 + grades_periodo_3
        
        # Check all conditions for alumni eligibility
        is_12_ano = detail_est.Turma.classe.name == '12 Ano'
        has_all_periods_complete = (grades_periodo_1 >= 13 and 
                                    grades_periodo_2 >= 13 and 
                                    grades_periodo_3 >= 13)
        
        student.is_alumni_eligible = is_12_ano and has_all_periods_complete
        student.total_grades = total_grades
        student.grades_periodo_1 = grades_periodo_1
        student.grades_periodo_2 = grades_periodo_2
        student.grades_periodo_3 = grades_periodo_3
        student.current_class = detail_est.Turma.classe.name
        student.is_12_ano = is_12_ano
        student.has_all_periods_complete = has_all_periods_complete
	
    sumariuEstudante = list()
    depList = departamento.objects.all()
    for x in depList:
        tur = turma.objects.filter(classe__name=klasse.name,classe__Departamento=x)
        estTurma = list()
        for y in tur:
            totEst = DetailEst.objects.filter(Turma=y,Turma_id__classe__name=klasse.name,is_active=True, Ano_Academinco=ano_act).count()
            estTurma.append([y,totEst])
        sumariuEstudante.append([x,estTurma])
	# print("sumariuEstudante:",sumariuEstudante)
    context = {
        'rejDadus':'active',
        'rejDadus2':'in active',
		'sumariuEstudante':sumariuEstudante,'est':est,'KlasseList':KlasseList,'klasse': klasse,
		'group': group,"page":"list",
		'title': f'Lista Estudante Klasse {klasse.name}', 'legend': f'Lista Estudante Klasse {klasse.name}'
	}
    return render(request, 'estudante/lista_estudanteC.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def ListEstDepClaTur(request, idDep,klasse,idTur):
	group = request.user.groups.all()[0].name
	klasse = classe.objects.filter(name=klasse).last()
	tur = turma.objects.get(id=idTur)
	dep = departamento.objects.get(id=idDep)

	KlasseLista = classe.objects.distinct().values('name').all()
	KlasseList = list()
	for a in KlasseLista:
		getClasse = classe.objects.filter(name=a['name']).last()
		KlasseList.append(getClasse)
	# Exclude students who have been transferred out (approved OUT transfers) or are alumni
	transferred_out_students = TransferStudent.objects.filter(
		transfer_type='OUT', 
		status='APPROVED'
	).values_list('estudante_id', flat=True)
	
	alumni_students = AlumniStudent.objects.filter(
		status='APPROVED'
	).values_list('estudante_id', flat=True)
	
	excluded_students = set(list(transferred_out_students) + list(alumni_students))
	est = DetailEst.objects.filter(
		Turma_id__classe_id__Departamento=dep,
		Turma_id__classe__name=klasse.name,
		Turma=tur,
		is_active=True
	).exclude(estudante_id__in=excluded_students).order_by('estudante__naran')
	
	sumariuEstudante = list()
	depList = departamento.objects.all()
	for x in depList:
		tur = turma.objects.filter(classe__name=klasse.name,classe__Departamento=x)
		print("tur:",tur)
		estTurma = list()
		for y in tur:
			totEst = DetailEst.objects.filter(Turma=y,Turma_id__classe__name=klasse.name,is_active=True).count()
			estTurma.append([y,totEst])
		sumariuEstudante.append([x,estTurma])
	print("sumariuEstudante:",sumariuEstudante)
	context = {
		'sumariuEstudante':sumariuEstudante,'est':est,'KlasseList':KlasseList,'klasse': klasse,
		'group': group,"page":"list",
		'title': f'Lista Estudante Klasse {klasse.name}', 'legend': f'Lista Estudante Klasse {klasse.name}'
	}
	return render(request, 'estudante/lista_estudanteC.html', context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','professor'])
def EstTinList(request, pk):
	group = request.user.groups.all()[0].name 
	tin = get_object_or_404(Ano, pk=pk)
	# Exclude students who have been transferred out (approved OUT transfers) or are alumni
	transferred_out_students = TransferStudent.objects.filter(
		transfer_type='OUT', 
		status='APPROVED'
	).values_list('estudante_id', flat=True)
	
	alumni_students = AlumniStudent.objects.filter(
		status='APPROVED'
	).values_list('estudante_id', flat=True)
	
	excluded_students = set(list(transferred_out_students) + list(alumni_students))
	est = DetailEst.objects.filter(Ano_Academinco=tin).exclude(estudante_id__in=excluded_students).order_by('Ano_Academinco')
	# tinan = Ano.objects.all()
	context = {'est': est, 'group': group,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request, 'estudante/lista_estudante.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def add_estudante(request):
    if request.method == "POST":
        form = est_Form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            username = instance.emis  # or any other unique identifier
            password = 'sajobril2025'  # Generate or assign a default password
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already exists.')
            else:
                user = User.objects.create_user(username=username, password=password)
                instance.user = user

                # Add user to the "Students" group
                student_group, created = Group.objects.get_or_create(name='estudante')
                user.groups.add(student_group)
                
                instance.save()
                n = instance.naran
                messages.success(request, f'Estudante {n} foi adicionado com sucesso.')
                return redirect('Listaestudante')
    else:
        form = est_Form()

    context = {
        'rejDadus':'active',
        'rejDadus2':'in active',
        'form': form, 
        "page": "form",
        'title': 'Aumenta Estudante',
        'legend': 'Aumenta Estudante'
    }
    return render(request, 'estudante/lista_estudante.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Secretario'])
def updateest(request,hashid):
	group = request.user.groups.all()[0].name
	est = get_object_or_404(Estudante,id=hashid)
	if request.method == 'POST':
		form = est_Form(request.POST,request.FILES,instance=est)
		if form.is_valid():
			instance = form.save()
			messages.info(request, f'Estudante is updated Successfully.')
			return redirect('Listaestudante')
	else:
		form = est_Form(instance=est)
	context = {
        'rejDadus':'active',
        'rejDadus2':'in active',
		'sukuActive':"active",
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'estudante/lista_estudante.html', context)


@login_required()
@allowed_users(allowed_roles=['admin','Secretario'])
def deleteest(request, id_est):
	est = get_object_or_404(DetailEst, id=id_est)
	naran = est.estudante.naran
	est.delete()
	messages.warning(request, f'Estudante {naran} is Deleted Successfully.')
	return redirect('Listaestudante')

@login_required()
@allowed_users(allowed_roles=['admin','Director','Secretario','estudante','professor'])
def detailViewest(request, id_est):
	est = Estudante.objects.get(id = id_est)
	detailest=DetailEst.objects.filter(estudante=est, is_active=True).last()
	context = {
		'est':est,'detailest':detailest,
	}
	return render(request, 'estudante/detailest.html', context)

#Report 

@login_required
@allowed_users(allowed_roles=['admin','Secretario'])
def EReportListActiveEstudante(request):
	objects = Estudante.objects.all()

	context ={
        'rejDadus':'active',
        'rejDadus2':'in active',
		"title":f"Pajina Relatoriu Lista Estudnate",
		"report_active":"active",
		"objects":objects,
		
	}
	return render(request, "estudante/listActiveEstudante.html",context)

@login_required
@allowed_users(allowed_roles=['admin','Director','Secretario','kurikulum','professor'])
def EReportListActiveEstudanteClasse(request):
	objects = DetailEst.objects.all()

	context ={
        'rejDadus':'active',
        'rejDadus2':'in active',
		"title":f"Pajina Relatoriu Lista Estudnate",
		"report_active":"active",
		"objects":objects,
		
	}
	return render(request, "estudante/listActiveEstudanteClassePrint.html",context)


# registo classe estudante	
@login_required
@allowed_users(allowed_roles=['admin','Secretario'])
def add_classe_estudante(request ,id1):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		get_student = Estudante.objects.get(id=id1)
		form = est_classe_Form(request.POST,request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.estudante = get_student
			instance.save()
			id1 = instance.estudante.id
			messages.success(request, f'Classe is Added Successfully.')
			return redirect('Listaestudante')
	else:
		form = est_classe_Form()
	context = {
        'rejDadus':'active',
        'rejDadus2':'in active',
		"group":group,
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	}
	return render(request, 'estudante/form_estudante_classe.html', context)

##
###
###################
############
@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def updateClassestudante(request, idEst): 
    
    detail_est = DetailEst.objects.filter(id=idEst).first()
    estudante = get_object_or_404(Estudante, id=detail_est.estudante.id)
    # detail_est = DetailEst.objects.filter(estudante=estudante).first() 
    
    if request.method == 'POST':
        form = est_classe_Form(request.POST, instance=detail_est)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe do Estudante foi atualizada com sucesso.')
            return redirect('list_students_aprovado')
    else:
        form = est_classe_Form(instance=detail_est)

    context = {
        'rejDadus':'active',
        'rejDadus2':'in active',
        'form': form,
        'page':'list',
        'page':'form',
        'estudante': estudante
    }
    return render(request, 'estudante/lista_estudante.html', context)

 
@login_required
@allowed_users(allowed_roles=['admin', 'Secretario', 'Tesoreira', 'Director', 'kurikulum','professor'])
def list_students_aprovado(request):
    group = request.user.groups.all()[0].name
    # print(group)
    KlasseLista = classe.objects.exclude(name__icontains='alumni').values('name').distinct()
    ano_act = Ano.objects.filter(is_active=True).first()
    # Exclude students who have been transferred out (approved OUT transfers) or are alumni
    transferred_out_students = TransferStudent.objects.filter(
        transfer_type='OUT', 
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    alumni_students = AlumniStudent.objects.filter(
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    excluded_students = set(list(transferred_out_students) + list(alumni_students))
    estudantes = DetailEst.objects.filter(Ano_Academinco=ano_act).exclude(estudante_id__in=excluded_students)
    # estudantes = Estudante.objects.all()
    students_with_media = []  # Initialize the list here
    object_disc = 13
    for est in estudantes:
        list_valor = valor_est.objects.filter(Tinan_periode=ano_act,estudante=est.estudante, periode__nome_periode='III Periodu', Turma_id__classe__name='10 Ano')
        # list_valor = valor_est.objects.filter(estudante=est, periode__nome_periode='III Periodu', Turma_id__classe__name='10 Ano')
        sum_valor_final = list_valor.aggregate(Sum('valor_final')).get('valor_final__sum')
        if sum_valor_final:
            media = float(sum_valor_final) / float(object_disc)
        else:
            media = 0

        val_approv = valor_est.objects.filter(Tinan_periode=ano_act,estudante=est.estudante, Turma_id__classe__name='10 Ano', is_approved=True).count()
        if val_approv > 30:
            aprovadu = 1
        else:
            aprovadu = 0
        
        # Only include students with media above 5.4
        if media > 5.4:
            students_with_media.append({
                'estudante': est,
                'media': media,
                'aprovadu':aprovadu,
            })
        
        # Assign sum_valor_final and media to each Estudante object
        est.sum_valor_final = sum_valor_final
        est.media = media
    
    context = {
        'group': group,
        'estudantes': students_with_media,  # Use filtered list here
        'KlasseLista': KlasseLista,
        "page": "list",
        'title': f"LISTA ESTUDANTE QUE TINHA VALORES MEDIA >= 5.5",
    }
    return render(request, "estudante/list_students_aprovado.html", context)

def Aprova_estudante_classe(request, id1):
    det_est = get_object_or_404(DetailEst, id=id1)
    valor = valor_est.objects.filter(estudante=det_est.estudante,Turma=det_est.Turma)
    # student = get_object_or_404(valor_est, id=id1)
    # student.is_approved = True
    # student.save()
    for val in valor:
         val.is_approved = True
         val.save()
    messages.success(request, f'Dados do estudante aprovados com sucesso.')
    return redirect('list_students_aprovado')

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario', 'Tesoreira', 'Director', 'kurikulum','professor'])
def ListEstudanteClassAprovado(request):
    group = request.user.groups.all()[0].name
    KlasseLista = classe.objects.exclude(name__icontains='alumni').values('name').distinct()
    ano_act = Ano.objects.filter(is_active=True).first()
    # Exclude students who have been transferred out (approved OUT transfers) or are alumni
    transferred_out_students = TransferStudent.objects.filter(
        transfer_type='OUT', 
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    alumni_students = AlumniStudent.objects.filter(
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    excluded_students = set(list(transferred_out_students) + list(alumni_students))
    estudantes = DetailEst.objects.filter(Ano_Academinco=ano_act).exclude(estudante_id__in=excluded_students)
    # estudantes = Estudante.objects.all()
    # ano_act = Ano.objects.filter(is_active=True).first()
    students_with_media = []  # Initialize the list here
    object_disc = 13 
    for est in estudantes:
        list_valor = valor_est.objects.filter(Tinan_periode=ano_act,estudante=est.estudante, periode__nome_periode='III Periodu', Turma_id__classe__name='11 Ano')
        sum_valor_final = list_valor.aggregate(Sum('valor_final')).get('valor_final__sum')
        if sum_valor_final:
            media = float(sum_valor_final) / float(object_disc)
        else:
            media = 0
        
        val_approv = valor_est.objects.filter(Tinan_periode=ano_act,estudante=est.estudante, Turma_id__classe__name='10 Ano', is_approved=True).count()
        if val_approv > 30:
            aprovadu = 1
        else:
            aprovadu = 0
        
        # Only include students with media above 5.4
        if media > 5.4:
            students_with_media.append({
                'estudante': est,
                'media': media,
                'aprovadu':aprovadu
            })
        
        # Assign sum_valor_final and media to each Estudante object
        est.sum_valor_final = sum_valor_final
        est.media = media
    
    context = {
        'group': group,
        'estudantes': students_with_media,  # Use filtered list here
        'KlasseLista': KlasseLista,
        "page": "list",
        'title': f"LISTA ESTUDANTE QUE TINHA VALORES MEDIA >= 5.5 KLASSE 11 ANO ",
    }
    return render(request, "estudante/reinscrisaun/lista_estudanteCAprovado.html", context)


@login_required
@allowed_users(allowed_roles=['admin', 'Secretario', 'Tesoreira', 'Director', 'kurikulum','professor'])
def ListEstudanteClassAprovado12(request):
    group = request.user.groups.all()[0].name
    KlasseLista = classe.objects.exclude(name__icontains='alumni').values('name').distinct()
    ano_act = Ano.objects.filter(is_active=True).first()
    # Exclude students who have been transferred out (approved OUT transfers) or are alumni
    transferred_out_students = TransferStudent.objects.filter(
        transfer_type='OUT', 
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    alumni_students = AlumniStudent.objects.filter(
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    excluded_students = set(list(transferred_out_students) + list(alumni_students))
    estudantes = DetailEst.objects.filter(Ano_Academinco=ano_act).exclude(estudante_id__in=excluded_students)
    # estudantes = Estudante.objects.all()
    students_with_media = []  # Initialize the list here
    object_disc = 13 
    for est in estudantes:
        list_valor = valor_est.objects.filter(Tinan_periode=ano_act,estudante=est.estudante, periode__nome_periode='III Periodu', Turma_id__classe__name='12 Ano')
        sum_valor_final = list_valor.aggregate(Sum('valor_final')).get('valor_final__sum')
        if sum_valor_final:
            media = float(sum_valor_final) / float(object_disc)
        else:
            media = 0

        val_approv = valor_est.objects.filter(Tinan_periode=ano_act,estudante=est.estudante, Turma_id__classe__name='10 Ano', is_approved=True).count()
        if val_approv > 30:
            aprovadu = 1
        else:
            aprovadu = 0
        
        # Only include students with media above 5.4
        if media > 5.4:
            students_with_media.append({
                'estudante': est,
                'media': media,
                'aprovadu':aprovadu,
            })
        
        # Assign sum_valor_final and media to each Estudante object
        est.sum_valor_final = sum_valor_final
        est.media = media
    
    context = {
        'group': group,
        'estudantes': students_with_media,  # Use filtered list here
        'KlasseLista': KlasseLista,
        "page": "list",
        'title': f"LISTA ESTUDANTE QUE TINHA VALORES MEDIA >= 5.5 KALSSE 12 ANO ",
    }
    return render(request, "estudante/reinscrisaun/listaaprovado12ano.html", context)


# # # Pofessor # # #
# # # 
#
#######
@login_required
@allowed_users(allowed_roles=['professor'])
def ListEstTurma(request):
    user = request.user
    prof = Funsionariu.objects.get(user = user)
    profturma = FunsionarioTurma.objects.filter(funsionario = prof.id).last()
    if profturma:
        # Exclude students who have been transferred out (approved OUT transfers) or are alumni
        transferred_out_students = TransferStudent.objects.filter(
            transfer_type='OUT', 
            status='APPROVED'
        ).values_list('estudante_id', flat=True)
        
        alumni_students = AlumniStudent.objects.filter(
            status='APPROVED'
        ).values_list('estudante_id', flat=True)
        
        excluded_students = set(list(transferred_out_students) + list(alumni_students))
        list_est = DetailEst.objects.filter(
            Turma = profturma.turma, 
            Ano_Academinco = profturma.ano
        ).exclude(estudante_id__in=excluded_students)
    else:
        list_est = DetailEst.objects.none()
    context = {
        'title': 'Lista Estudante da Turma',
        'est':list_est,
        'page':'list',
        'profturma':profturma,
    }
    return render(request, 'estudante/turma/lista_estudanteTurma.html',context)


# ## Transferencia

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def list_transfers(request):
    group = request.user.groups.all()[0].name
    transfers = TransferStudent.objects.all().order_by('-request_date')
    
    context = {
        'transfers': transfers,
        'group': group,
        'title': 'Lista Transfer',
        'page': 'list'
    }
    return render(request, 'estudante/transfer/list_transfers.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def create_internal_transfer(request, estudante_id):
    group = request.user.groups.all()[0].name
    estudante = get_object_or_404(Estudante, id=estudante_id)
    
    if request.method == 'POST':
        form = InternalTransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.estudante = estudante
            transfer.transfer_type = 'OUT'  # Internal transfer out of current turma
            transfer.save()
            messages.success(request, f'Internal transfer request for {estudante.naran} created successfully.')
            return redirect('list_transfers')
    else:
        form = InternalTransferForm()
    
    context = {
        'form': form,
        'estudante': estudante,
        'group': group,
        'title': f'Internal Transfer - {estudante.naran}',
        'page': 'form'
    }
    return render(request, 'estudante/transfer/create_internal_transfer.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def create_external_transfer(request, estudante_id):
    group = request.user.groups.all()[0].name
    estudante = get_object_or_404(Estudante, id=estudante_id)
    
    if request.method == 'POST':
        form = ExternalTransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.estudante = estudante
            transfer.save()
            messages.success(request, f'External transfer request for {estudante.naran} created successfully.')
            return redirect('list_transfers')
    else:
        form = ExternalTransferForm()
    
    context = {
        'form': form,
        'estudante': estudante,
        'group': group,
        'title': f'External Transfer - {estudante.naran}',
        'page': 'form'
    }
    return render(request, 'estudante/transfer/create_external_transfer.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def approve_transfer(request, transfer_id):
    transfer = get_object_or_404(TransferStudent, id=transfer_id)
    transfer.status = 'APPROVED'
    transfer.approved_by = request.user
    from django.utils import timezone
    transfer.approval_date = timezone.now()
    transfer.save()
    
    # If it's an OUT transfer, deactivate the student's current detail record
    if transfer.transfer_type == 'OUT':
        current_detail = DetailEst.objects.filter(
            estudante=transfer.estudante,
            is_active=True
        ).first()
        if current_detail:
            current_detail.is_active = False
            current_detail.save()
    
    messages.success(request, f'Transfer for {transfer.estudante.naran} approved successfully.')
    return redirect('list_transfers')

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def reject_transfer(request, transfer_id):
    transfer = get_object_or_404(TransferStudent, id=transfer_id)
    transfer.status = 'REJECTED'
    transfer.approved_by = request.user
    from django.utils import timezone
    transfer.approval_date = timezone.now()
    transfer.save()
    
    messages.warning(request, f'Transfer for {transfer.estudante.naran} rejected.')
    return redirect('list_transfers')

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def transfer_detail(request, transfer_id):
    transfer = get_object_or_404(TransferStudent, id=transfer_id)
    group = request.user.groups.all()[0].name
    
    context = {
        'transfer': transfer,
        'group': group,
        'title': f'Transfer Detail - {transfer.estudante.naran}',
        'page': 'detail'
    }
    return render(request, 'estudante/transfer/transfer_detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def transferred_out_students(request, year_id=None):
    group = request.user.groups.all()[0].name
    
    # Get students who have been transferred out (approved OUT transfers)
    # transfers = TransferStudent.objects.filter(transfer_type='OUT',status='APPROVED')
    transfers = TransferStudent.objects.filter(
        transfer_type='OUT',
        status='APPROVED'
    ).select_related('estudante')

    anos = Ano.objects.all()
    
    if year_id:
        year = get_object_or_404(Ano, id=year_id)
        transfers = transfers.filter(estudante__Ano_Resisto=year)
        title = f'Transferred Out Students - {year.ano}'
        print("year:",year)
    else:
        title = 'All Transferred Out Students'
    print(year_id)
    
    context = {
        'transfers': transfers,
        'group': group,
        'title': title,
        'page': 'list',
        'anos': anos,
    }
    return render(request, 'estudante/transfer/transferred_out_students.html', context)


# ## Alumni functionality

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def list_alumni(request):
    group = request.user.groups.all()[0].name
    alumni_records = AlumniStudent.objects.all().order_by('-request_date')
    
    context = {
        'alumni_records': alumni_records,
        'group': group,
        'title': 'Lista Alumni',
        'page': 'list'
    }
    return render(request, 'estudante/alumni/list_alumni.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def create_alumni_record(request, estudante_id):
    group = request.user.groups.all()[0].name
    estudante = get_object_or_404(Estudante, id=estudante_id)
    
    # Check if student meets both alumni requirements before allowing alumni creation
    from valor.models import valor_est
    ano_act = Ano.objects.filter(is_active=True).first()
    
    # Get student's current active class
    current_detail = DetailEst.objects.filter(
        estudante=estudante,
        is_active=True,
        Ano_Academinco=ano_act
    ).first()
    
    # Count grades for each period separately
    grades_periodo_1 = valor_est.objects.filter(
        estudante=estudante,
        Tinan_periode=ano_act,
        periode__nome_periode='I Periodu'
    ).count()
    
    grades_periodo_2 = valor_est.objects.filter(
        estudante=estudante,
        Tinan_periode=ano_act,
        periode__nome_periode='II Periodu'
    ).count()
    
    grades_periodo_3 = valor_est.objects.filter(
        estudante=estudante,
        Tinan_periode=ano_act,
        periode__nome_periode='III Periodu'
    ).count()
    
    total_grades = grades_periodo_1 + grades_periodo_2 + grades_periodo_3
    
    # Check all conditions
    is_12_ano = current_detail and current_detail.Turma.classe.name == '12 Ano' if current_detail else False
    has_all_periods_complete = (grades_periodo_1 >= 13 and 
                                grades_periodo_2 >= 13 and 
                                grades_periodo_3 >= 13)
    
    if not is_12_ano:
        current_class = current_detail.Turma.classe.name if current_detail else 'No Class'
        messages.error(request, f'Student {estudante.naran} is in {current_class}. Only students in 12 Ano class can become alumni.')
        return redirect('Listaestudante')
    
    if not has_all_periods_complete:
        missing_periods = []
        if grades_periodo_1 < 13:
            missing_periods.append(f'I Periodu ({grades_periodo_1}/13)')
        if grades_periodo_2 < 13:
            missing_periods.append(f'II Periodu ({grades_periodo_2}/13)')
        if grades_periodo_3 < 13:
            missing_periods.append(f'III Periodu ({grades_periodo_3}/13)')
        
        missing_text = ', '.join(missing_periods)
        messages.error(request, f'Student {estudante.naran} needs 13 grades in each period. Missing: {missing_text}.')
        return redirect('Listaestudante')
    
    # Get the student's current active detail record
    current_detail = DetailEst.objects.filter(
        estudante=estudante,
        is_active=True
    ).first()
    
    if request.method == 'POST':
        form = AlumniForm(request.POST)
        if form.is_valid():
            alumni_record = form.save(commit=False)
            alumni_record.estudante = estudante
            alumni_record.save()
            messages.success(request, f'Alumni record for {estudante.naran} created successfully.')
            return redirect('list_alumni')
    else:
        # Pre-populate form with current student data
        initial_data = {}
        if current_detail:
            initial_data['completed_turma'] = current_detail.Turma
            initial_data['graduation_year'] = current_detail.Ano_Academinco
        
        form = AlumniForm(initial=initial_data)
    
    context = {
        'form': form,
        'estudante': estudante,
        'current_detail': current_detail,
        'group': group,
        'title': f'Create Alumni Record - {estudante.naran}',
        'page': 'form'
    }
    return render(request, 'estudante/alumni/create_alumni.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def approve_alumni(request, alumni_id):
    alumni_record = get_object_or_404(AlumniStudent, id=alumni_id)
    alumni_record.status = 'APPROVED'
    alumni_record.approved_by = request.user
    from django.utils import timezone
    alumni_record.approval_date = timezone.now()
    alumni_record.save()
    
    # Deactivate the student's current detail record
    current_detail = DetailEst.objects.filter(
        estudante=alumni_record.estudante,
        is_active=True
    ).first()
    if current_detail:
        current_detail.is_active = False
        current_detail.save()
    
    messages.success(request, f'Alumni record for {alumni_record.estudante.naran} approved successfully.')
    return redirect('list_alumni')

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def reject_alumni(request, alumni_id):
    alumni_record = get_object_or_404(AlumniStudent, id=alumni_id)
    alumni_record.status = 'REJECTED'
    alumni_record.approved_by = request.user
    from django.utils import timezone
    alumni_record.approval_date = timezone.now()
    alumni_record.save()
    
    messages.warning(request, f'Alumni record for {alumni_record.estudante.naran} rejected.')
    return redirect('list_alumni')

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def alumni_detail(request, alumni_id):
    alumni_record = get_object_or_404(AlumniStudent, id=alumni_id)
    group = request.user.groups.all()[0].name
    
    context = {
        'alumni_record': alumni_record,
        'group': group,
        'title': f'Alumni Detail - {alumni_record.estudante.naran}',
        'page': 'detail'
    }
    return render(request, 'estudante/alumni/alumni_detail.html', context)

@login_required
@allowed_users(allowed_roles=['admin', 'Secretario'])
def approved_alumni_students(request, year_id=None):
    group = request.user.groups.all()[0].name
    
    # Get students who have been approved as alumni
    alumni_records = AlumniStudent.objects.filter(
        status='APPROVED'
    ).select_related('estudante')

    anos = Ano.objects.all()
    
    if year_id:
        year = get_object_or_404(Ano, id=year_id)
        alumni_records = alumni_records.filter(graduation_year=year)
        title = f'Alumni Students - {year.ano}'
    else:
        title = 'All Alumni Students'
    
    context = {
        'alumni_records': alumni_records,
        'group': group,
        'title': title,
        'page': 'list',
        'anos': anos,
    }
    return render(request, 'estudante/alumni/approved_alumni_students.html', context)