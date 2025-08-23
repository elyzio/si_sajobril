from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import render as filtering
from estudante.models import *
from funsionariu.models import *
from historia.models import * 
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from horario.models import *
from django.views.generic import ListView
from django.db.models import Q

def PublicFilter(filters):
	estudante = Estudante.objects.all()
	totalEstudantes = DetailEst.objects.exclude(Turma_id__classe__name='Alumni').filter(
		Q(Turma_id__classe__name='10 Ano') |
		Q(Turma_id__classe__name='11 Ano') |
		Q(Turma_id__classe__name='12 Ano')
	).count()
	totalEstFeto = Estudante.objects.filter(Sexo='Feto').count()
	totalEstMane = Estudante.objects.filter(Sexo='Mane').count()
	totalAlumni = DetailEst.objects.filter(Turma_id__classe__name='Alumni').count()
	
	tin=Ano.objects.order_by('ano')
	data_mun=Municipality.objects.all()
	data_class=classe.objects.all()
	loopingestudantesexo = []
	for ii in data_mun.iterator():
		total_sexo_Mane = Estudante.objects.filter(
			municipality_id=ii.id, 
			Sexo="Mane").count()
		total_Sexo_Feto = Estudante.objects.filter(
			municipality_id=ii.id,
			Sexo="Feto").count()
		total_estudante=Estudante.objects.filter(
			municipality_id=ii.id).all().count()
		loopingestudantesexo.append({'id':ii.id,'name':ii.name,
			'total_sexo_Mane':total_sexo_Mane,
			'total_estudante':total_estudante,
			"total_Sexo_Feto":total_Sexo_Feto,})
	dict = {
		"title":"Sistema Informasaun Akademika ba Eskola Colegio de Santo Inacio de Loiola ",'konfigurasaunActive':"active",\
		"totalEstudantes":totalEstudantes,
		"totalEstFeto":totalEstFeto,
		"totalEstMane":totalEstMane,
		"totalAlumni":totalAlumni,
		"data_mun":data_mun,"loopingestudantesexo":loopingestudantesexo,		
	}
	return filtering(filters, 'index_public.html',context=dict)
def public_horariu (request):
	datahorS=Horario_est.objects.filter(loron='Day One').all()
	datahorT=Horario_est.objects.filter(loron='Day Two').all()
	datahorQ=Horario_est.objects.filter(loron='Day Three').all()
	datahorQui=Horario_est.objects.filter(loron='Day Four').all()
	datahorSE=Horario_est.objects.filter(loron='Day Five').all()
	datahorSa=Horario_est.objects.filter(loron='Sabadu').all()
	context={'datahorS':datahorS,'datahorT':datahorT,'datahorQ':datahorQ,'datahorQui':datahorQui,'datahorSE':datahorSE,
		'datahorSa':datahorSa,
	}
	return render(request, 'horariu/horariupublic.html',context)

def PrintHorario(request):
	objects = Horario_est.objects.all()
	context ={
		"title":f"Report Relatoriu Lista Horario","report_active":"active","objects":objects,	
	}
	return render(request, "horariu/printhorariu.html",context)

#list estudent in munisipality
def public_List_estudnte_munisipiu(request):
	data_mun=Municipality.objects.all()
	loopingestudantesexo=[]
	for x in data_mun.iterator():
		total_sexo_Mane_mun = Estudante.objects.filter(municipality_id=x.id,Sexo="Mane").count()
		total_sexo_Feto_mun= Estudante.objects.filter(municipality_id=x.id,Sexo="Feto").count()
		total_estudantes = Estudante.objects.filter(municipality_id=x.id).all().count()
		loopingestudantesexo.append({'id':x.id,'name':x.name,
			'total_estudantes':total_estudantes,'total_sexo_Mane_mun':total_sexo_Mane_mun,'total_sexo_Feto_mun':total_sexo_Feto_mun,
			})
	context={
	"page":"list",
	'data_mun':data_mun,
	'loopingestudantesexo':loopingestudantesexo,
	}
	return render(request,'munisipiu/munisipiulist.html',context)
def list_mun_M(request,pk):
	list_mun=get_object_or_404(Municipality,pk=pk)
	listMun_M= Estudante.objects.filter(municipality_id=list_mun, Sexo='Mane').all()
	context={
		"page":"list",
		"title":f'Lista Estudante Mane husi Munisipiu {list_mun.name}',
		'list_mun':list_mun,
		'listMun_M':listMun_M,
	}
	return render (request,'munisipiu/listmunM.html',context)

def list_mun_F(request,pk):
	list_mun=get_object_or_404(Municipality,pk=pk)
	listMun_F= Estudante.objects.filter(municipality_id=list_mun, Sexo='Feto').all()
	context={
		"page":"list",
		"title":f'Lista Estudante Feto husi Munisipiu {list_mun.name}',
		'list_mun':list_mun,
		'listMun_F':listMun_F,
	}
	return render (request,'munisipiu/listmunF.html',context)
def list_mun_GF(request,pk):
	list_mun=get_object_or_404(Municipality,pk=pk)
	listMun_GF= Estudante.objects.filter(municipality_id=list_mun, Sexo='Feto').all()
	context={
		"page":"list",
		"title":f'Foto Estudante Feto husi Munisipiu {list_mun.name}',
		'list_mun':list_mun,
		'listMun_GF':listMun_GF,
	}
	return render (request,'munisipiu/Galery/listmunGF.html',context)
def list_mun_G(request,pk):
	list_mun=get_object_or_404(Municipality,pk=pk)
	listMun_G= Estudante.objects.filter(municipality_id=list_mun).all()
	context={
		"page":"list",
		"title":f'Foto Estudante husi Munisipiu {list_mun.name}',
		'list_mun':list_mun,
		'listMun_G':listMun_G,
	}
	return render (request,'munisipiu/Galery/listmunG.html',context)
def list_mun_GM(request,pk):
	list_mun=get_object_or_404(Municipality,pk=pk)
	listMun_GM= Estudante.objects.filter(municipality_id=list_mun, Sexo='Mane').all()
	context={
		"page":"list",
		"title":f'Foto Estudante Mane husi Munisipiu {list_mun.name}',
		'list_mun':list_mun,
		'listMun_GM':listMun_GM,
	}
	return render (request,'munisipiu/Galery/listmunGM.html',context)

def list_mun(request,pk):
	list_mun=get_object_or_404(Municipality,pk=pk)
	listMun= Estudante.objects.filter(municipality_id=list_mun).order_by('municipality')
	context={
		"page":"list",
		"title":f'Lista Estudante husi Munisipiu {list_mun.name}',
		'list_mun':list_mun,
		'listMun':listMun,
	}
	return render (request,'munisipiu/listmun.html',context)
#end list minisipiu
#list estudent in program
def public_List_estudnte_Pro(request):
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
	context={
	"page":"list",
	'data_programa':data_programa,
	'data_tin':data_tin,
	'loopingestudantesProgrm':loopingestudantesProgrm,
	}
	return render(request,'programa/Programalist.html',context)
#list estudent in Tinan
def public_List_estudnte_tinan(request):
	data_tin=Ano.objects.all()
	looping_total_estudante_tin= []	
	for x in data_tin.iterator() :
		total_sexo_Mane_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id,Sexo="Mane").count()
		total_sexo_Feto_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id,Sexo="Feto").count()
		total_estudante_kada_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id).all().count()
		# total_osanR_kada_tinan = Estudante.objects.filter(Ano_Resisto_id=x.id).aggregate(Sum('Osan_resistu')).get('Osan_resistu__sum')	
		looping_total_estudante_tin.append({'id':x.id,'ano':x.ano,
		'total_sexo_Mane_tinan':total_sexo_Mane_tinan,'total_estudante_kada_tinan':total_estudante_kada_tinan,
		'total_sexo_Feto_tinan':total_sexo_Feto_tinan,
		# 'total_osanR_kada_tinan':total_osanR_kada_tinan,
		})
	context={
	"page":"list",
	'data_tin':data_tin,
	'looping_total_estudante_tin':looping_total_estudante_tin,
	}
	return render(request,'tinan/EstudanteTinan.html',context)
def list_progrmCT(request,pk):
	list_tin=get_object_or_404(Ano,pk=pk)
	listestCt= DetailEst.objects.filter(estudante_id__Ano_Resisto_id=list_tin,Turma_id__classe_id__Departamento__nome_departamento='Ciencias e Tecnologia').all()
	context={
		"page":"list",
		"title":f'Lista Estudante husi departamento Ciencias e Tecnologia iha tinan {list_tin.ano}',
		'list_tin':list_tin,
		'listestCt':listestCt,
	}
	return render (request,'programa/list_progrmCT.html',context)
def list_progrmCsh(request,pk):
	list_tin=get_object_or_404(Ano,pk=pk)
	listestCsh= DetailEst.objects.filter(estudante_id__Ano_Resisto_id=list_tin,Turma_id__classe_id__Departamento__nome_departamento='Ciensias Sociais e Humanidade').all()
	context={
		"page":"list",
		"title":f'Lista Estudante husi departamento Ciencias Sociais e Humanidade iha tinan {list_tin.ano}',
		'list_tin':list_tin,
		'listestCsh':listestCsh,
	}
	return render (request,'programa/list_progrmCsh.html',context)

def list_Ct_G(request,pk):
	list_tin=get_object_or_404(Ano,pk=pk)
	listCt_G= DetailEst.objects.filter(estudante_id__Ano_Resisto_id=list_tin,Turma_id__classe_id__Departamento__nome_departamento='Ciencias e Tecnologia').all()
	context={
		"page":"list",
		"title":f'Foto Estudante husi departamento Ciencias e Tecnologia iha tinan {list_tin.ano}',
		'list_tin':list_tin,
		'listCt_G':listCt_G,
	}
	return render (request,'programa/galery/list_CTG.html',context)
def list_Csh_G(request,pk):
	list_tin=get_object_or_404(Ano,pk=pk)
	listCsh_G= DetailEst.objects.filter(estudante_id__Ano_Resisto_id=list_tin,Turma_id__classe_id__Departamento__nome_departamento='Ciensias Sociais e Humanidade').all()
	context={
		"page":"list",
		"title":f'Foto Estudante husi departamento Ciencias e Tecnologia iha tinan {list_tin.ano}',
		'list_tin':list_tin,
		'listCsh_G':listCsh_G,
	}
	return render (request,'programa/galery/list_CSHG.html',context)



#list historia	
def Public_historia(request):
	historia_eskola = historia.objects.all()		
	context = {
		'historia_eskola':historia_eskola, 
		"page":"list",
		'title': 'HISTORIA ',
	}
	return render(request,'public_historia.html',context)
#list news 
def public_news(request):
	list_news = news.objects.all()	
	cat = category.objects.all()	
	context = {
		'list_news':list_news, 
		'cat':cat, 
		"page":"list",
		'title': 'INFORMASAUN',
	}
	return render(request,'publicInformasaun/publicnews.html',context)

def public_detailView_news(request, id_news):
	cat = news.objects.get(id = id_news)
	context = {
		'cat':cat,
	}
	return render(request, 'publicInformasaun/detPublicInformasaun.html', context)
#end list news
#list estudent 
def public_Listaestudante(request):
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
		'est':est, 'deps': deps,'tinan': tinan,"page":"list",
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request,'Publicestudnte/lista_estudante.html',context)

def public_detailViewest(request, id_est):
	est = Estudante.objects.get(id = id_est)
	detailest=DetailEst.objects.filter(estudante=est, is_active=True).last()
	context = {
		'est':est,'detailest':detailest,
	}
	return render(request, 'Publicestudnte/detailest.html', context)
def public_ListEstudanteClass(request, id):
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
"page":"list",
		'title': f'Lista Estudante Klasse {klasse.name}', 'legend': f'Lista Estudante Klasse {klasse.name}'
	}
	return render(request, 'Publicestudnte/lista_estudanteC.html', context)

def public_ListEstDepClaTur(request, idDep,klasse,idTur):
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
		"page":"list",
		'title': f'Lista Estudante Klasse {klasse.name}', 'legend': f'Lista Estudante Klasse {klasse.name}'
	}
	return render(request, 'Publicestudnte/lista_estudanteC.html', context)


def publicEstTinList(request, pk):
	tin = get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin).all().order_by('Ano_Resisto')
	tinan = Ano.objects.all()
	context = {'est': est, 'tinan':tinan,"page":"list",'tin':tin,
		'title': 'Lista Estudante', 'legend': 'Lista Estudante'
	}
	return render(request, 'Publicestudnte/lista_estudante.html', context)

def publicEstGaleriList(request):
	tinanG = Ano.objects.all()
	publicGaleriList = Estudante.objects.all()
	book_paginator = Paginator(publicGaleriList, 16)
	page_num = request.GET.get('page')
	page = book_paginator.get_page(page_num)
	context = {
		'publicGaleriList':page,
		'page' : page,
		'title': 'Galery Estudante', 'tinanG':tinanG
	}
	return render(request, 'Publicestudnte/Galery_estudante.html', context)
def publicGaleryEstTinList(request, pk):
	tin = get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin).all().order_by('Ano_Resisto')
	tinanG= Ano.objects.all()
	book_paginator = Paginator(est, 8)
	page_num = request.GET.get('page')
	page = book_paginator.get_page(page_num)
	context = {'est': page,"page":page,'tin':tin,'tinanG':tinanG,
		'title': 'Galery Estudante','legend': f'Foto Estudante husi tinan {tin.ano}'
	}
	return render(request, 'Publicestudnte/Galery_estudanteTin.html', context)
#lit estudent in years 
def public_list_estudante_Mane(request,pk):
	tin= get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin, Sexo="Mane").all().order_by('naran')
	context={
		'tin':tin,
		'est':est,
		"page":"list",
		"title":f'Lista Estudante Mane iha tinan {tin.ano}',
	}
	return render(request, 'Publicestudnte/estudanteM.html',context)
def public_list_estudante_feto(request,pk):
	tin= get_object_or_404(Ano, pk=pk)
	est = Estudante.objects.filter(Ano_Resisto=tin, Sexo="Feto").all().order_by('naran')
	context={
		'tin':tin,
		'est':est,
		"page":"list",
		"title":f'Lista Estudante Feto Iha Tinan {tin.ano}',
	}
	return render(request, 'Publicestudnte/estudanteF.html',context)
def public_Listaestudante_tin(request,pk):
	lisTin=get_object_or_404(Ano ,pk=pk)
	public_list_estudante=Estudante.objects.filter(Ano_Resisto=lisTin).all().order_by('naran')
	context={
		'lisTin':lisTin,
		'public_list_estudante':public_list_estudante,
		"page":"list",
		"title":f'Lista  Estudante Husi Tinan {lisTin.ano}',
	}
	return render(request, 'Publicestudnte/listaEstudantePerTinan.html',context)
