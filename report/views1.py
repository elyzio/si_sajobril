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
    
    # Calculate excluded students (transferred out and approved alumni)
    from estudante.models import AlumniStudent
    transferred_out_ids = TransferStudent.objects.filter(
        transfer_type='OUT',
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    approved_alumni_ids = AlumniStudent.objects.filter(
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    # Combine both exclusion lists
    excluded_ids = set(list(transferred_out_ids) + list(approved_alumni_ids))
    
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
        # Exclude approved alumni and transferred out students
        for dep in departments:
            count = DetailEst.objects.filter(
                Ano_Academinco=active_year,
                is_active=True,
                Turma__classe__name=class_name,
                Turma__classe__Departamento=dep
            ).exclude(
                estudante_id__in=excluded_ids
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
		).exclude(
            estudante_id__in=excluded_ids
        ).count()
        
        feto_count = DetailEst.objects.filter(
			Turma__classe__name=c,
			estudante__Sexo='Feto',
			Turma__classe__name__in=classes
		).exclude(
            estudante_id__in=excluded_ids
        ).count()
        class_gender_counts[c] = {'Mane': mane_count, 'Feto': feto_count}

    # Alumni statistics using new AlumniStudent system
    alumni_count = AlumniStudent.objects.filter(status='APPROVED').count()
    
    alumni_by_gender = AlumniStudent.objects.filter(
        status='APPROVED'
    ).values('estudante__Sexo').annotate(count=Count('estudante__Sexo'))
    
    # Transfer statistics  
    total_transfers = TransferStudent.objects.count()
    
    transfer_in_approved = TransferStudent.objects.filter(
        transfer_type='IN', 
        status='APPROVED'
    ).count()
    
    transfer_out_approved = TransferStudent.objects.filter(
        transfer_type='OUT', 
        status='APPROVED'
    ).count()
    
    transfer_pending = TransferStudent.objects.filter(
        status='PENDING'
    ).count()
    
    # Internal vs External transfers
    internal_transfers = TransferStudent.objects.filter(
        from_turma__isnull=False,
        to_turma__isnull=False,
        status='APPROVED'
    ).count()
    
    external_transfers = TransferStudent.objects.filter(
        Q(from_school__isnull=False) | Q(to_school__isnull=False),
        status='APPROVED'
    ).count()
    
    # Current active students (already calculated excluded_ids above)
    active_students_count = Estudante.objects.exclude(
        id__in=excluded_ids
    ).count()

    context = {
        'title':'Report Estudante',
        'student_gender':student_gender,
        'headers': result['headers'],
        'rows': result['data'],
        'class_gender_counts': class_gender_counts,
        # Alumni stats
        'alumni_count': alumni_count,
        'alumni_by_gender': alumni_by_gender,
        # Transfer stats
        'total_transfers': total_transfers,
        'transfer_in_approved': transfer_in_approved,
        'transfer_out_approved': transfer_out_approved,
        'transfer_pending': transfer_pending,
        'internal_transfers': internal_transfers,
        'external_transfers': external_transfers,
        'active_students_count': active_students_count,
    }
    return render(request,'report/student/stats.html',context)

# Filtered views for student statistics
@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StudentsByGender(request, gender):
    active_year = Ano.objects.filter(is_active=True).first()
    
    # Get transferred out students to exclude
    transferred_out_ids = TransferStudent.objects.filter(
        transfer_type='OUT',
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    # Get active students by gender - exclude both transferred out and alumni
    from estudante.models import AlumniStudent
    alumni_ids = AlumniStudent.objects.filter(status='APPROVED').values_list('estudante_id', flat=True)
    excluded_ids = set(list(transferred_out_ids) + list(alumni_ids))
    
    students = DetailEst.objects.filter(
        Ano_Academinco=active_year,
        estudante__Sexo=gender,
        is_active=True
    ).exclude(
        estudante_id__in=excluded_ids
    ).select_related('estudante')
    
    context = {
        'title': f'Students by Gender - {gender}',
        'students': students,
        'filter_type': 'gender',
        'filter_value': gender,
    }
    return render(request, 'report/student/students_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StudentsByClass(request, class_name):
    active_year = Ano.objects.filter(is_active=True).first()
    
    # Get transferred out students to exclude
    transferred_out_ids = TransferStudent.objects.filter(
        transfer_type='OUT',
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    # Get active students by class
    students = DetailEst.objects.filter(
        Ano_Academinco=active_year,
        Turma__classe__name=class_name,
        is_active=True
    ).exclude(
        estudante_id__in=transferred_out_ids
    ).select_related('estudante')
    
    context = {
        'title': f'Students in {class_name}',
        'students': students,
        'filter_type': 'class',
        'filter_value': class_name,
    }
    return render(request, 'report/student/students_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StudentsAlumni(request):
    # Get alumni students using new AlumniStudent system
    from estudante.models import AlumniStudent
    
    alumni_records = AlumniStudent.objects.filter(
        status='APPROVED'
    ).select_related('estudante', 'completed_turma__classe__Departamento')
    
    context = {
        'title': 'Alumni Students',
        'alumni_records': alumni_records,  # Pass alumni records directly
        'filter_type': 'alumni',
        'filter_value': 'Alumni',
    }
    return render(request, 'report/student/students_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StudentsTransferredIn(request):
    # Get students who transferred IN (approved)
    transfers = TransferStudent.objects.filter(
        transfer_type='IN',
        status='APPROVED'
    ).select_related('estudante')
    
    students = [transfer for transfer in transfers]
    
    context = {
        'title': 'Students Transferred IN',
        'transfers': students,
        'filter_type': 'transferred_in',
        'filter_value': 'Transferred IN',
    }
    return render(request, 'report/student/transfers_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StudentsTransferredOut(request):
    # Get students who transferred OUT (approved)
    transfers = TransferStudent.objects.filter(
        transfer_type='OUT',
        status='APPROVED'
    ).select_related('estudante')
    
    students = [transfer for transfer in transfers]
    
    context = {
        'title': 'Students Transferred OUT',
        'transfers': students,
        'filter_type': 'transferred_out',
        'filter_value': 'Transferred OUT',
    }
    return render(request, 'report/student/transfers_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StudentsActive(request):
    active_year = Ano.objects.filter(is_active=True).first()
    
    # Get transferred out students to exclude
    transferred_out_ids = TransferStudent.objects.filter(
        transfer_type='OUT',
        status='APPROVED'
    ).values_list('estudante_id', flat=True)
    
    # Get all active students - exclude both transferred out and alumni
    from estudante.models import AlumniStudent
    alumni_ids = AlumniStudent.objects.filter(status='APPROVED').values_list('estudante_id', flat=True)
    excluded_ids = set(list(transferred_out_ids) + list(alumni_ids))
    
    students = DetailEst.objects.filter(
        Ano_Academinco=active_year,
        is_active=True
    ).exclude(
        estudante_id__in=excluded_ids
    ).select_related('estudante')
    
    context = {
        'title': 'Active Students',
        'students': students,
        'filter_type': 'active',
        'filter_value': 'Active Students',
    }
    return render(request, 'report/student/students_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def ReportFunStats(request):
    # Get active academic year
    active_year = Ano.objects.filter(is_active=True).first()
    
    if not active_year:
        return {}

    # Basic counts
    total_staff = Funsionariu.objects.count()
    
    # 1. Total count by municipality
    count_by_municipality = Funsionariu.objects.values('municipality__name', 'municipality__id').annotate(total=Count('id')).order_by('-total')

    # 2. Total count by nivel_estudu
    count_by_nivel_estudu = Funsionariu.objects.values('nivel_estudu').annotate(total=Count('id')).order_by('-total')

    # 3. Total count by estatus
    count_by_estatus = Funsionariu.objects.values('estatus').annotate(total=Count('id')).order_by('-total')

    # 4. Count by gender
    count_by_gender_fun = Funsionariu.objects.values('Sexo').annotate(total=Count('id'))

    # 5. Count by civil status
    count_by_civil_status = Funsionariu.objects.values('estadu_civil').annotate(total=Count('id')).order_by('-total')

    # 6. Count by department
    count_by_department = Funsionariu.objects.values('departamento__name', 'departamento__id').annotate(total=Count('id')).order_by('-total')

    # 7. Count by position  
    count_by_position = Funsionariu.objects.values('pozisaun').annotate(total=Count('id')).order_by('-total')

    # 8. Count by study area
    count_by_study_area = Funsionariu.objects.values('area_estudu').annotate(total=Count('id')).order_by('-total')

    # 9. Teaching assignments - Staff assigned to turmas
    active_teachers = FunsionarioTurma.objects.filter(ano=active_year).values('funsionario__naran', 'turma__Turma').distinct()
    teachers_with_classes = FunsionarioTurma.objects.filter(ano=active_year).values('funsionario').distinct().count()
    staff_without_classes = total_staff - teachers_with_classes

    # 10. Age statistics (if birth dates available)
    from django.db.models import Case, When, IntegerField
    from datetime import date, timedelta
    
    today = date.today()
    age_ranges = Funsionariu.objects.aggregate(
        age_20_30=Count(Case(When(data_moris__lte=today - timedelta(days=365*20), 
                                 data_moris__gte=today - timedelta(days=365*30), then=1))),
        age_31_40=Count(Case(When(data_moris__lte=today - timedelta(days=365*31), 
                                 data_moris__gte=today - timedelta(days=365*40), then=1))),
        age_41_50=Count(Case(When(data_moris__lte=today - timedelta(days=365*41), 
                                 data_moris__gte=today - timedelta(days=365*50), then=1))),
        age_51_plus=Count(Case(When(data_moris__lt=today - timedelta(days=365*51), then=1)))
    )

    # 11. Staff by class assignment (which grades they teach)
    staff_by_class = FunsionarioTurma.objects.filter(ano=active_year).values(
        'turma__classe__name'
    ).annotate(total_teachers=Count('funsionario', distinct=True)).order_by('-total_teachers')

    context = {
        'title':'Report Funsionariu',
        'total_staff': total_staff,
        'count_by_municipality': count_by_municipality,
        'count_by_nivel_estudu': count_by_nivel_estudu,
        'count_by_estatus': count_by_estatus,
        'count_by_gender_fun': count_by_gender_fun,
        'count_by_civil_status': count_by_civil_status,
        'count_by_department': count_by_department,
        'count_by_position': count_by_position,
        'count_by_study_area': count_by_study_area,
        'teachers_with_classes': teachers_with_classes,
        'staff_without_classes': staff_without_classes,
        'age_ranges': age_ranges,
        'staff_by_class': staff_by_class,
        'active_teachers': active_teachers,
    }
    return render(request,'report/fun/stats.html',context)

# Filtered views for staff statistics
@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffByGender(request, gender):
    staff = Funsionariu.objects.filter(Sexo=gender).order_by('naran')
    context = {
        'title': f'Staff by Gender - {gender}',
        'staff': staff,
        'filter_type': 'gender',
        'filter_value': gender,
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffByMunicipality(request, municipality_id):
    municipality = Municipality.objects.get(id=municipality_id)
    staff = Funsionariu.objects.filter(municipality_id=municipality_id).order_by('naran')
    context = {
        'title': f'Staff by Municipality - {municipality.name}',
        'staff': staff,
        'filter_type': 'municipality',
        'filter_value': municipality.name,
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffByEducation(request, education_level):
    staff = Funsionariu.objects.filter(nivel_estudu=education_level).order_by('naran')
    context = {
        'title': f'Staff by Education - {education_level}',
        'staff': staff,
        'filter_type': 'education',
        'filter_value': education_level,
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffByStatus(request, status):
    staff = Funsionariu.objects.filter(estatus=status).order_by('naran')
    context = {
        'title': f'Staff by Status - {status}',
        'staff': staff,
        'filter_type': 'status',
        'filter_value': status,
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffByPosition(request, position):
    staff = Funsionariu.objects.filter(pozisaun=position).order_by('naran')
    context = {
        'title': f'Staff by Position - {position}',
        'staff': staff,
        'filter_type': 'position',
        'filter_value': position,
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffByDepartment(request, department_id):
    department = DepFun.objects.get(id=department_id)
    staff = Funsionariu.objects.filter(departamento_id=department_id).order_by('naran')
    context = {
        'title': f'Staff by Department - {department.name}',
        'staff': staff,
        'filter_type': 'department',
        'filter_value': department.name,
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffByStudyArea(request, study_area):
    staff = Funsionariu.objects.filter(area_estudu=study_area).order_by('naran')
    context = {
        'title': f'Staff by Study Area - {study_area}',
        'staff': staff,
        'filter_type': 'study_area',
        'filter_value': study_area,
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffByCivilStatus(request, civil_status):
    staff = Funsionariu.objects.filter(estadu_civil=civil_status).order_by('naran')
    context = {
        'title': f'Staff by Civil Status - {civil_status}',
        'staff': staff,
        'filter_type': 'civil_status',
        'filter_value': civil_status,
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffWithClasses(request):
    active_year = Ano.objects.filter(is_active=True).first()
    # Get staff who have class assignments this year
    staff_with_classes = FunsionarioTurma.objects.filter(ano=active_year).values_list('funsionario', flat=True).distinct()
    staff = Funsionariu.objects.filter(id__in=staff_with_classes).order_by('naran')
    context = {
        'title': 'Staff with Classes',
        'staff': staff,
        'filter_type': 'with_classes',
        'filter_value': 'Active Teachers',
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def StaffWithoutClasses(request):
    active_year = Ano.objects.filter(is_active=True).first()
    # Get staff who don't have class assignments this year
    staff_with_classes = FunsionarioTurma.objects.filter(ano=active_year).values_list('funsionario', flat=True).distinct()
    staff = Funsionariu.objects.exclude(id__in=staff_with_classes).order_by('naran')
    context = {
        'title': 'Staff without Classes',
        'staff': staff,
        'filter_type': 'without_classes',
        'filter_value': 'Non-Teaching Staff',
    }
    return render(request, 'report/fun/staff_filtered.html', context)

@login_required()
@allowed_users(allowed_roles=['admin','Tesoreira','Director','Secretario','kurikulum','estudante','professor'])
def AllStaff(request):
    staff = Funsionariu.objects.all().order_by('naran')
    context = {
        'title': 'All Staff Members',
        'staff': staff,
        'filter_type': 'all_staff',
        'filter_value': 'Total Staff',
    }
    return render(request, 'report/fun/staff_filtered.html', context)