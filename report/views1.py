from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import render
from collections import defaultdict
import pandas as pd
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from funsionariu.models import *
from estudante.models import *
from departamento.models import *
from django.db.models import Sum, Count, Q
from custom.models import *
from Classe.models import *
from Turma.models import *
from Ano.models import *
from valor.models import *
from Turma.models import turma
from collections import OrderedDict

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def ReportStudentStats(request):
     # Get active academic year
    active_year = Ano.objects.filter(is_active=True).first()
    
    if not active_year:
        return {}
    student_gender = DetailEst.objects.filter(Ano_Academinco=active_year).values('estudante__Sexo').annotate(count=Count('estudante__Sexo'))
    print(student_gender)

    # Get all departments
    departments = departamento.objects.all().order_by('nome_departamento')
    
    # Get distinct class names (10 Ano, 11 Ano, 12 Ano) excluding Alumni
    class_names = ['10 Ano', '11 Ano', '12 Ano']
    
    # Prepare the result structure
    result = {
        'headers': ['Class'] + [dep.nome_departamento for dep in departments],
        'data': []
    }
    
    # For each distinct class name (not class instance)
    for class_name in class_names:
        row = {'Class': class_name}
        
        # Initialize all departments to 0
        for dep in departments:
            row[dep.nome_departamento] = 0
        
        # Find all classes with this name
        classes_with_name = classe.objects.filter(name=class_name)
        
        # For each department, sum counts across all classes with this name
        for dep in departments:
            count = DetailEst.objects.filter(
                Ano_Academinco=active_year,
                is_active=True,
                Turma__classe__name=class_name,
                Turma__classe__Departamento=dep
            ).count()
            
            row[dep.nome_departamento] = count
        
        result['data'].append(row)

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
        'title':'Report Estudante',
        'student_gender':student_gender,
        'headers': result['headers'],
        'rows': result['data'],
        'class_gender_counts': class_gender_counts,
    }
    return render(request,'report/student/stats.html',context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def ReportFunStats(request):
     # Get active academic year
    active_year = Ano.objects.filter(is_active=True).first()
    
    if not active_year:
        return {}
    
    # Get all departments
    departments = departamento.objects.all().order_by('nome_departamento')
    
    # Get distinct class names (10 Ano, 11 Ano, 12 Ano) excluding Alumni
    class_names = ['10 Ano', '11 Ano', '12 Ano']
    
    # Prepare the result structure
    result = {
        'headers': ['Class'] + [dep.nome_departamento for dep in departments],
        'data': []
    }
    
    # For each distinct class name (not class instance)
    for class_name in class_names:
        row = {'Class': class_name}
        
        # Initialize all departments to 0
        for dep in departments:
            row[dep.nome_departamento] = 0
        
        # Find all classes with this name
        classes_with_name = classe.objects.filter(name=class_name)
        
        # For each department, sum counts across all classes with this name
        for dep in departments:
            count = DetailEst.objects.filter(
                Ano_Academinco=active_year,
                is_active=True,
                Turma__classe__name=class_name,
                Turma__classe__Departamento=dep
            ).count()
            
            row[dep.nome_departamento] = count
        
        result['data'].append(row)

    # 1. Total count by municipality
    count_by_municipality = Funsionariu.objects.values('municipality__name').annotate(total=Count('id'))

    # 2. Total count by nivel_estudu
    count_by_nivel_estudu = Funsionariu.objects.values('nivel_estudu').annotate(total=Count('id'))

    # 3. Total count by estatus
    count_by_estatus = Funsionariu.objects.values('estatus').annotate(total=Count('id'))

    count_by_gender_fun = Funsionariu.objects.values('Sexo').annotate(total=Count('id'))

    context = {
        'title':'Report Funsionariu',
        'count_by_municipality': count_by_municipality,
        'count_by_nivel_estudu': count_by_nivel_estudu,
        'count_by_estatus': count_by_estatus,
        'count_by_gender_fun': count_by_gender_fun,
    }
    return render(request,'report/fun/stats.html',context)