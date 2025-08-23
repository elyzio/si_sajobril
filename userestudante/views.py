from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from users.decorators import allowed_users
from django.contrib import messages
from django.db.models import Sum
from estudante.models import *
from valor.models import *
from estudante.forms import *


@login_required
@allowed_users(allowed_roles=['estudante'])
def detalho_estudante(request):
    # Get the logged-in user's student record
    est = get_object_or_404(Estudante, user=request.user)
    ano_activo = Ano.objects.filter(is_active=True).last()
    detailestvalor = DetailEst.objects.filter(estudante=est, is_active=True, Ano_Academinco=ano_activo).last()
    print(detailestvalor)
    # Get the student's details for each period
    context = {
     
        'title': f"Detalhes de {est.naran}",
        'est': est,
        'detailestvalor': detailestvalor,
    }
    
    return render(request, "detalho_estudante.html", context)


@login_required
@allowed_users(allowed_roles=['estudante'])
def DetailValoresEstudante(request):
    # Get the logged-in user's group
    group = request.user.groups.first().name
    # Get the Estudante object related to the logged-in user
    estValor = get_object_or_404(Estudante, user=request.user)
    # Fetch the latest DetailEst for the Estudante
    detailestvalor = DetailEst.objects.filter(estudante=estValor, is_active=True).last()
    
    period = Periode.objects.all().order_by('id')
    loopingestudanteVl = []
    for x in period.iterator():
        total_Vl_klass = valor_est.objects.filter(estudante=estValor, periode=x, Turma_id__classe__name='10 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
        total_Vl_klass1 = valor_est.objects.filter(estudante=estValor, periode=x, Turma_id__classe__name='11 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
        total_Vl_klass2 = valor_est.objects.filter(estudante=estValor, periode=x, Turma_id__classe__name='12 Ano').aggregate(Sum('valor_final')).get('valor_final__sum')
        loopingestudanteVl.append({
            'id': x.id,
            'nome_periode': x.nome_periode,
            'total_Vl_klass': total_Vl_klass,
            'total_Vl_klass1': total_Vl_klass1,
            'total_Vl_klass2': total_Vl_klass2,
        })

    context = {
        'group': group,
        'period': period,
        "page": "list",
        'title': f"VALOR ESTUDANTE {estValor.naran}",
        'vl_detail': estValor,
        'estValor': estValor,
        'detailestvalor': detailestvalor,
        'loopingestudanteVl': loopingestudanteVl,
    }
    return render(request, "detailvalor.html", context)

@login_required
@allowed_users(allowed_roles=['estudante'])
def atualizar_dados(request):
    estudante = get_object_or_404(Estudante, user=request.user)
    
    if request.method == 'POST':
        form = est_Form(request.POST, request.FILES, instance=estudante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seus dados foram atualizados com sucesso.')
            return redirect('detalho_estudante')
    else:
        form = est_Form(instance=estudante)
    
    context = {
        'form': form,
        'title': 'Atualizar Dados'
    }
    return render(request, 'formupdateestudanteUser.html', context)

