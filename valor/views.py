from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from funsionariu.models import *
from .forms import *
from django.contrib import messages
from .filters import estFilter
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.decorators import allowed_users
from django.conf import settings
from valor import forms, models

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def Listaestudantevalor(request):
	group = request.user.groups.all()[0].name
	periodlist= Periode.objects.all()
	est = Estudante.objects.all()		
	deps = departamento.objects.all().order_by('id')
	tinan = Ano.objects.all()
	KlasseLista = classe.objects.distinct().values('name').all()
	Klasse = list()
	for a in KlasseLista:
		getClasse = classe.objects.filter(name=a['name']).last()
		Klasse.append(getClasse)
	context = {
		'est':est, 
		'Klasse':Klasse,
		'est':est, 'deps': deps, 'group': group, 'tinan': tinan,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante','periodlist':periodlist,
	}
	return render(request,'valor/lista_estudanteValor.html',context)

@login_required
@allowed_users(allowed_roles=['admin','estudante','Tesoreira','Director','kurikulum', 'professor'])
def ListEstudanteClassValor(request, id):
	group = request.user.groups.all()[0].name
	klasse = classe.objects.filter(name=id).last()
	KlasseLista = classe.objects.distinct().values('name').all()
	KlasseList = list()
	for a in KlasseLista:
		getClasse = classe.objects.filter(name=a['name']).last()
		KlasseList.append(getClasse)
	est = DetailEst.objects.filter(Turma_id__classe__name=klasse.name,is_active=True).all().order_by('estudante__naran')
	print("est:",est)
	
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
	return render(request, 'Valor/lista_estudanteCValor.html', context)

@login_required
@allowed_users(allowed_roles=['admin','estudante','Tesoreira','Director','kurikulum', 'professor'])
def ListEstDepClaTurValor(request, idDep,klasse,idTur):
	group = request.user.groups.all()[0].name
	klasse = classe.objects.filter(name=klasse).last()
	tur = turma.objects.get(id=idTur)
	dep = departamento.objects.get(id=idDep)
	KlasseLista = classe.objects.distinct().values('name').all()
	KlasseList = list()
	for a in KlasseLista:
		getClasse = classe.objects.filter(name=a['name']).last()
		KlasseList.append(getClasse)
	est = DetailEst.objects.filter(Turma_id__classe_id__Departamento=dep,Turma_id__classe__name=klasse.name,Turma=tur,is_active=True).all().order_by('estudante__naran')
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
	return render(request, 'Valor/lista_estudanteCValor.html', context)

@login_required
@allowed_users(allowed_roles=['admin','estudante','Tesoreira','Director','kurikulum', 'professor'])
def DetailViewsVE(request,hashid,id):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = hashid)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	vl_detail = get_object_or_404(Estudante,id=hashid)
	period = Periode.objects.all().order_by('id')
	loopingestudanteVl= []	
	for x in period.iterator() :
		total_Vl_klass = valor_est.objects.filter(estudante=vl_detail,periode=x, Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
		total_Vl_klass1 = valor_est.objects.filter(estudante=vl_detail,periode=x, Turma_id__classe__name='11 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
		total_Vl_klass2 = valor_est.objects.filter(estudante=vl_detail,periode=x, Turma_id__classe__name='12 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
		loopingestudanteVl.append({'id':x.id,'nome_periode':x.nome_periode,
			'total_Vl_klass':total_Vl_klass,'total_Vl_klass1':total_Vl_klass1,'total_Vl_klass2':total_Vl_klass2,
		})
	context = {
		'group':group,'period':period,
		"page":"list",'title':f"VALOR  ESTUDANTE {vl_detail.naran}",
		'vl_detail':vl_detail,
		'estValor':estValor,
		'detailestvalor':detailestvalor,
		'loopingestudanteVl':loopingestudanteVl, 
	}
	return render(request, "valor/detailvl.html",context)

@login_required
@allowed_users(allowed_roles=['admin','estudante','Tesoreira','Director','kurikulum', 'professor'])
def ValorEstudantePeriod(request,idPeriodu,idEst):
	group = request.user.groups.all()[0].name
	period = get_object_or_404(Periode,id=idPeriodu)
	estudante = get_object_or_404(Estudante,id=idEst)
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor).last()
	periodlist = Periode.objects.all().order_by('id')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode=period,Klasse__name='10 Ano').last()		
	list_Clasificasao_valor1=Clasificasao_valor.objects.filter(estudante=estValor,periode=period,Klasse__name='11 Ano').last()		
	list_Clasificasao_valor2=Clasificasao_valor.objects.filter(estudante=estValor,periode=period,Klasse__name='12 Ano').last()		
	list_valor = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='10 Ano')
	list_valor_count = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='10 Ano').count()
	# print(f'Total Valor Rejistu {list_valor_count}')
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())	
	else:
		sum_valor_final = 0
		media = float()
	
	if list_valor_count >= 13:
		if media<=5.5:
			dis="reprovado"
		else :
			dis="aprovado"
	else:
		dis=""
	cl = detailestvalor.Turma.classe.name
	if cl == "10 Ano":
		page_class = 10
	else:
		page_class = 0
	print(group)
	context = {
		'group':group,'period':period,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,
		'sum_valor_final':sum_valor_final,'page_class':page_class,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'list_Clasificasao_valor1':list_Clasificasao_valor1,
		'list_Clasificasao_valor2':list_Clasificasao_valor2,
		'media':media,
		'dis':dis,
		'list_valor':list_valor,
		"page":"list",'title':f"RESULTADOS OBTIDOS EM CADA DICIPLINA DE : {estudante.naran}",
	}
	return render(request, "valor/classe/valorEstPeriodu.html",context)

@login_required
@allowed_users(allowed_roles=['admin','estudante','Tesoreira','Director','kurikulum', 'professor'])
def ValorEstudantePeriod1(request,idPeriodu,idEst):
	group = request.user.groups.all()[0].name
	period = get_object_or_404(Periode,id=idPeriodu)
	estudante = get_object_or_404(Estudante,id=idEst)
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor).last()
	periodlist = Periode.objects.all().order_by('id')
	list_valor_11ano = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='11 Ano')
	list_valor_11ano_count = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='11 Ano').count()
	sum_valor_final1 = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='11 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final1:
		media1 = float(sum_valor_final1)/float(list_valor_11ano.count())
	else:
		sum_valor_final1 = 0
		media1 = float(0)
	cl = detailestvalor.Turma.classe.name
	
	if cl == "11 Ano":
		page_class = 11
	else:
		page_class = 0
	if list_valor_11ano_count >= 13:
		if media1 <= 5.5:
			dis="reprovado"
		else :
			dis="aprovado"
	else:
		dis = ""
	print(group)
	context = {
		'group':group,'period':period,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,
		'media1':media1 ,'page_class':page_class,"dis":dis,
		'list_valor_11ano':list_valor_11ano,
		'sum_valor_final1':sum_valor_final1,
		"page":"list",'title':f"RESULTADOS OBTIDOS EM CADA DICIPLINA DE : {estudante.naran}",
	}
	return render(request, "valor/classe/valor11ano.html",context)

@login_required
@allowed_users(allowed_roles=['admin','estudante','Tesoreira','Director','kurikulum', 'professor'])
def ValorEstudantePeriod2(request,idPeriodu,idEst):
	group = request.user.groups.all()[0].name
	period = get_object_or_404(Periode,id=idPeriodu)
	estudante = get_object_or_404(Estudante,id=idEst)
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor).last()
	periodlist = Periode.objects.all().order_by('id')
	list_valor_12ano = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='12 Ano')
	list_valor_12ano_count = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='12 Ano').count()
	sum_valor_final2 = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='12 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final2:
		media2 = float(sum_valor_final2)/float(list_valor_12ano.count())
	else:
		sum_valor_final2 = 0
		media2 = float(0)
	cl = detailestvalor.Turma.classe.name
	if cl == "12 Ano":
		page_class = 12
	else:
		page_class = 0
	if list_valor_12ano_count >= 13:
		if media2 <= 5.5:
			dis="reprovado"
		else :
			dis="aprovado"
	else:
		dis = ""
	print(group)
	context = {
		'group':group,'period':period,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,
		'media2':media2 ,'page_class':page_class,'dis':dis,
		'list_valor_12ano':list_valor_12ano,
		'sum_valor_final2':sum_valor_final2,
		"page":"list",'title':f"RESULTADOS OBTIDOS EM CADA DICIPLINA DE : {estudante.naran}",
	}
	return render(request, "valor/classe/valor12ano.html",context)

# registo Clasificasaun valor estudante
@login_required
@allowed_users(allowed_roles=['admin','kurikulum', 'professor'])
def add_Clasificasao_valor(request, id1):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		get_student = Estudante.objects.get(id=id1)
		form = Clasificasao_valor_form(request.POST, request.FILES) 
		if form.is_valid():
			instance = form.save(commit=False)
			instance.estudante = get_student
			instance.save()
			id1 = instance.estudante.id
			messages.success(request, f' Estundante Clasification is Added Successfully.')
			return redirect('details-valor',id1,id)
	else:
		form = Clasificasao_valor_form() 
	context = {
		"group":group, 
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	
	}
	return render(request, 'valor/form_Clasificasao_valor.html', context)

@login_required
@allowed_users(allowed_roles=['admin','kurikulum', 'professor'])
def add_valor(request, id1):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		get_student = Estudante.objects.get(id=id1)
		form = vl_Form(request.POST, request.FILES) 
		if form.is_valid():
			instance = form.save(commit=False)
			instance.estudante = get_student
			instance.save()
			id1 = instance.estudante.id
			messages.success(request, f'Valor Estundante is Added Successfully.')
			return redirect('details-valor',id1,id)
	else:
		form = vl_Form() 
	context = {
		"group":group,
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	}
	return render(request, 'valor/form_vl.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','kurikulum', 'professor'])
def updatevalor(request,hashid):
	group = request.user.groups.all()[0].name
	vl = get_object_or_404(valor_est,id=hashid)
	if request.method == 'POST':
		form = vl_Form(request.POST,instance=vl)
		if form.is_valid():
			instance = form.save()
			get_student =instance.estudante.pk
			messages.info(request, f' Valor Estudante is updated Successfully.')
			return redirect('details-valor',get_student,id)
	else:
		form = vl_Form(instance=vl)
	context = {
		'sukuActive':"active",
		'page':"form",
		'group': group, 
		'form': form, 
	}
	return render(request, 'valor/form_vl.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','kurikulum', 'professor'])
def deletevalor(request, id_vl):
	vl = get_object_or_404(valor_est, id=id_vl)
	vl.delete()
	studante_data = vl.estudante.id
	messages.warning(request, f'Valor Estudante is Deleted Successfully.')
	return redirect('details-valor',studante_data,id)
	
# ....................print valor .......................
@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum', 'professor','estudante'])
def ValorEstudantePeriod_Print(request,idPeriodu,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	period = get_object_or_404(Periode,id=idPeriodu)
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='10 Ano')
	list_Clasificasao_valor=Clasificasao_valor.objects.filter(estudante=estValor,periode=period,Klasse__name='10 Ano').last()
	sum_valor_final = valor_est.objects.filter(estudante=estudante,periode=period,  Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final:
		media = float(sum_valor_final)/float(list_valor.count())
	else:
		sum_valor_final = 0
		media = float(0)

	context = {
		'group':group,'period':period,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final':sum_valor_final,
		'list_Clasificasao_valor':list_Clasificasao_valor,
		'media':media,'list_valor':list_valor,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",
	}
	return render(request, "print/valorEstPerioduPrint.html",context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','estudante','Director','kurikulum', 'professor'])
def ValorEstudantePeriod1_Print1(request,idPeriodu,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	period1 = get_object_or_404(Periode,id=idPeriodu)
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist1 = Periode.objects.all().order_by('id')
	list_valor1 = valor_est.objects.filter(estudante=estudante,periode=period1, Turma_id__classe__name='11 Ano')
	list_Clasificasao_valor1=Clasificasao_valor.objects.filter(estudante=estValor,periode=period1,Klasse__name='11 Ano').last()
	sum_valor_final1 = valor_est.objects.filter(estudante=estudante,periode=period1,  Turma_id__classe__name='11 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final1:
		media1 = float(sum_valor_final1)/float(list_valor1.count())
	else:
		sum_valor_final1 = 0
		media1 = float(0)

	context = {
		'group':group,'period1':period1,'periodlist1':periodlist1,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final1':sum_valor_final1,
		'list_Clasificasao_valor1':list_Clasificasao_valor1,
		'media1':media1,'list_valor1':list_valor1,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",
	}
	return render(request, "print/valorEstPerioduPrint1.html",context)

@login_required
@allowed_users(allowed_roles=['admin','Tesoreira','estudante','Director','kurikulum', 'professor'])
def ValorEstudantePeriod_Print2(request,idPeriodu,idEst):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = idEst)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	period = get_object_or_404(Periode,id=idPeriodu)
	estudante = get_object_or_404(Estudante,id=idEst)
	periodlist = Periode.objects.all().order_by('id')
	list_valor2 = valor_est.objects.filter(estudante=estudante,periode=period, Turma_id__classe__name='12 Ano')
	list_Clasificasao_valor2=Clasificasao_valor.objects.filter(estudante=estValor,periode=period,Klasse__name='12 Ano').last()
	sum_valor_final2 = valor_est.objects.filter(estudante=estudante,periode=period,  Turma_id__classe__name='12 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
	if sum_valor_final2:
		media = float(sum_valor_final2)/float(list_valor2.count())
	else:
		sum_valor_final2 = 0
		media = float(0)

	context = {
		'group':group,'period':period,'periodlist':periodlist,'estudante':estudante,'detailestvalor':detailestvalor,'estValor':estValor,
		'sum_valor_final2':sum_valor_final2,
		'list_Clasificasao_valor2':list_Clasificasao_valor2,
		'media':media,'list_valor2':list_valor2,
		"page":"list",'title':f"VALOR  ESTUDANTE {estudante.naran}",
	}
	return render(request, "print/valorEstPerioduPrint2.html",context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def lista_valor_Jeral(request):
	group= request.user.groups.all()[0].name
	KlasseLista = classe.objects.distinct().values('name').all()
	Klasse = list()
	for a in KlasseLista:
		getClasse = classe.objects.filter(name=a['name']).last()
		Klasse.append(getClasse)
	valorData=valor_est.objects.all()
	context = {
		'group':group,
		'Klasse':Klasse,
		'valorData':valorData,
		'title': 'lista valor ',	
	}
	return render(request,'valor/listaValorjeral.html',context)
@login_required
@allowed_users(allowed_roles=['admin', 'Tesoreira','Director','Secretario','kurikulum', 'professor'])
def ListaVAlorClass(request, id):
	group = request.user.groups.all()[0].name
	klasse = classe.objects.filter(name=id).last()
	KlasseLista = classe.objects.distinct().values('name').all()
	KlasseList = list()
	for a in KlasseLista:
		getClasse = classe.objects.filter(name=a['name']).last()
		KlasseList.append(getClasse)
	est = valor_est.objects.filter(Turma_id__classe__name=klasse.name).all().order_by('estudante__naran')
	print("est:",est)
	
	sumariuEstudante = list()
	depList = departamento.objects.all()
	for x in depList:
		tur = turma.objects.filter(classe__name=klasse.name,classe__Departamento=x)
		print("tur:",tur)
		estTurma = list()
		for y in tur:
			totEst = valor_est.objects.filter(Turma=y,Turma_id__classe__name=klasse.name).count()
			estTurma.append([y,totEst])
		sumariuEstudante.append([x,estTurma])
	print("sumariuEstudante:",sumariuEstudante)
	context = {
		'sumariuEstudante':sumariuEstudante,'est':est,'KlasseList':KlasseList,'klasse': klasse,
		'group': group,"page":"list",
		'title': f'Lista Estudante Klasse {klasse.name}', 'legend': f'Lista Estudante Klasse {klasse.name}'
	}
	return render(request, 'valor/lista_valorC.html', context)


#periodu ..........//.......................//.........................//
@login_required()
@allowed_users(allowed_roles=['admin'])
def ListaPr(request):
	group = request.user.groups.all()[0].name
	pr = Periode.objects.all()		
	context = {
		'konf':"in active",
		'konfAct':"active",
		'pr':pr, 
		'group': 'Lista Periodu',
	}
	return render(request,'periodu/lista_pr.html',context)


@login_required
@allowed_users(allowed_roles=['admin'])
def addperiodo(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = periodoForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			dep = instance.nome_periode
			instance.save()
			messages.success(request, f' {dep} is Added Successfully.')
			return redirect('Lista-periode')
	else:
		form = periodoForm()
	context = {
		'konf':"in active",
		'konfAct':"active",
		"group":group,
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	}
	return render(request, 'periodu/form_periode.html', context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def updateperiode(request,hashid):
	group = request.user.groups.all()[0].name
	periodeData= get_object_or_404(Periode,id=hashid)
	if request.method =='POST':
		form = periodoForm(request.POST,instance=periodeData)
		if form.is_valid():
			instance = form.save()
			messages.info (request, f' Periode is update Successfully')
			return redirect ('Lista-periode')

	else :
		form =  periodoForm(instance=periodeData)
	context={
		'konf':"in active",
		'konfAct':"active",
		'sukuActive':"active",
		'page':"form",
		'group':group,
		'form':form,
	}
	return render(request, 'periodu/form_periode.html',context)

@login_required()
@allowed_users(allowed_roles=['admin'])
def deletePeriode(request ,hashid):
	periode = get_object_or_404(Periode, id=hashid)
	pr=periode.nome_periode
	periode.delete()
	messages.warning(request,f'Periode {pr} is Deleted Successfully.' )
	return redirect ('Lista-periode')

# ### 
# ### professor ###
###
@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def Listaestudantevalorprof1(request):
	group = request.user.groups.all()[0].name
	periodlist= Periode.objects.all()
	est = Estudante.objects.all()		
	deps = departamento.objects.all().order_by('id')
	tinan = Ano.objects.all()
	KlasseLista = classe.objects.distinct().values('name').all()
	Klasse = list()
	for a in KlasseLista:
		getClasse = classe.objects.filter(name=a['name']).last()
		Klasse.append(getClasse)
	context = {
		'est':est, 
		'Klasse':Klasse,
		'est':est, 'deps': deps, 'group': group, 'tinan': tinan,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante','periodlist':periodlist,
	}
	return render(request,'valor/lista_estudanteValor.html',context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','kurikulum','professor'])
def Listaestudantevalorprof(request):
	user = request.user
	prof = Funsionariu.objects.get(user = user)
	profturma = FunsionarioTurma.objects.filter(funsionario = prof.id).last()
	if profturma:
		turma = str(profturma.turma)
		list_est = DetailEst.objects.filter(Turma = profturma.turma, Ano_Academinco = profturma.ano)
	else:
		turma = ""
		list_est = DetailEst.objects.none()
	context = {
        'title': 'Lista Valor Estudante da Turma '+ turma,
        'est':list_est,
        'page':'list',
		'profturma':profturma,
    }
	return render(request, 'valor/lista_estudanteValor2.html',context)

@login_required
@allowed_users(allowed_roles=['admin','estudante','Tesoreira','Director','kurikulum', 'professor'])
def DetailViewsVEProf(request,hashid):
	group = request.user.groups.all()[0].name
	estValor = Estudante.objects.get(id = hashid)
	detailestvalor=DetailEst.objects.filter(estudante=estValor, is_active=True).last()
	vl_detail = get_object_or_404(Estudante,id=hashid)
	period = Periode.objects.all().order_by('id')
	loopingestudanteVl= []	
	for x in period.iterator() :
		total_Vl_klass = valor_est.objects.filter(estudante=vl_detail,periode=x, Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
		total_Vl_klass1 = valor_est.objects.filter(estudante=vl_detail,periode=x, Turma_id__classe__name='11 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
		total_Vl_klass2 = valor_est.objects.filter(estudante=vl_detail,periode=x, Turma_id__classe__name='12 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
		loopingestudanteVl.append({'id':x.id,'nome_periode':x.nome_periode,
			'total_Vl_klass':total_Vl_klass,'total_Vl_klass1':total_Vl_klass1,'total_Vl_klass2':total_Vl_klass2,
		})
	
	# print(detailestvalor.Turma.classe.name)

	if detailestvalor.Turma.classe.name == "10 Ano":
		classlink = "ValorEstudatePeriod"
	if detailestvalor.Turma.classe.name == "11 Ano":
		classlink = "ValorEstudatePeriod1"
	if detailestvalor.Turma.classe.name == "12 Ano":
		classlink = "ValorEstudatePeriod2"
	if detailestvalor.Turma.classe.name == "Alumni":
		classlink = "ValorEstudatePeriod"
	context = {
		'group':group,'period':period,
		"page":"list",'title':f"VALOR  ESTUDANTE {vl_detail.naran}",
		'vl_detail':vl_detail,
		'estValor':estValor,
		'detailestvalor':detailestvalor,
		'loopingestudanteVl':loopingestudanteVl, 
		'classlink':classlink,
		'classe':detailestvalor.Turma.classe.name,
	}
	return render(request, "valor/detailvl1.html",context)

@login_required
@allowed_users(allowed_roles=['professor'])
def add_valor1(request, id1, period):
	group = request.user.groups.all()[0].name
	get_student = Estudante.objects.get(id=id1)
	det_est = DetailEst.objects.filter(estudante=get_student).order_by('-id').first()
	dept = det_est.Turma.classe.Departamento.id

	classe = det_est.Turma.classe.name
	periodu = Periode.objects.get(id=period)
	if classe == "10 Ano":
		class_link = "ValorEstudatePeriod"
	if classe == "11 Ano":
		class_link = "ValorEstudatePeriod1"
	if classe == "12 Ano":
		class_link = "ValorEstudatePeriod2"
	if request.method == 'POST':
		# periodu
		form = vl_Form1(request.POST, request.FILES, tinan=det_est.Ano_Academinco, periode=periodu, estudante=get_student, dept=dept) 
		if form.is_valid():
			instance = form.save(commit=False)
			instance.estudante = get_student
			instance.Tinan_periode = det_est.Ano_Academinco
			instance.Turma = det_est.Turma
			instance.periode = periodu
			instance.save()
			id1 = instance.estudante.id
			messages.success(request, f'Valor Estundante is Added Successfully.')
			return redirect('details-valorPr',id1)
	else:
		form = vl_Form1(tinan=det_est.Ano_Academinco, periode=periodu, estudante=get_student, dept=dept)
	
	context = {
		"group":group,
		'aldeiaActive':"active",
		'page':"form",
		'form': form, 
	}
	return render(request, 'valor/form_vl1.html', context)