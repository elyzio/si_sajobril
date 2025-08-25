from django.urls import path
from .views import *
from .views1 import *

urlpatterns = [
	path('report/<str:pk>/tinan/',select_estudante_tinan_list, name="estudante-tinan-lista"),
	path('report-Estudante-turma-10/<str:pk>/Ano/',select_estudante_turma_list, name="select_estudante_turma_list"),

	path('report/valor_est/turma/<str:turma_id>/periode/<str:periode_id>/', students_by_turma, name='students_by_turma'),
	path('report/report/valor_est/Classe/10-Ano/periode/<int:periode_id>/', students_by_class, name='students_by_class'),
	path('report/report/valor_est/Classe/11-Ano/periode/<int:periode_id>/', students_by_class1, name='students_by_class1'),
	path('report/report/valor_est/Classe/12-Ano/periode/<int:periode_id>/', students_by_class2, name='students_by_class2'),
	path('lista/periodu/valores/Jeral-Klasse/<str:turma_id>/', listValorClassJeral , name='listValorClassJeral'),

	path('report-Estudante-turma-11/<str:pk>/Ano/',select_estudante_turma1_list, name="select_estudante_turma1_list"),
	path('report-Estudante-turma-12/<str:pk>/Ano/',select_estudante_turma2_list, name="select_estudante_turma2_list"),
	path('report/<str:pk>/tinan/Osan',select_estudante_osan_tinan_list, name="estudante-tinan-lista-osan"),
	path('report/<str:pk>/tinan/lista_estudante/Mane',select_estudante_tinan_list_Mane, name="select_estudante_tinan_list_Mane"),
	path('report/<str:pk>/tinan/lista_estudante/Feto',select_estudante_tinan_list_feto, name="select_estudante_tinan_list_feto"),
	path('lista-tabular-etudante/', reporlistaestudante, name="reporlistaestudante"),
	path('lista-Shart-etudante/', report_shart, name="report_shart"),
	path('lista-Shart-etudante/Munisipiu/', shartMunisipiu, name="shartMunisipiu"),
	path('lista-Shart-etudante-propinas/', repor_tb_propinas, name="repor_tb_propinas"),
	path('lista-Shart-etudante-valor/', shartvalor, name="shartvalor"),
	path('dashboard/report//Estudante/Alumi/', EReportListActiveEstudanteAlumiprint, name="EReportListActiveEstudanteAlumiprint"),
	path('dashboard/Lista//Estudante/Alumi/', ListaEstudanteAlumi, name="ListaEstudanteAlumi"),

	# LISTA VALOR TUTI TURMA URL
	path('report-Estudantevalor-turma-10/<str:pk>/Ano/',select_estudante_turma_listValor1, name="select_estudante_turma_listValor1"),
	path('report-Estudantevalor-turma-11/<str:pk>/Ano/',select_estudante_turma_listValor2, name="select_estudante_turma_listValor2"),
	path('report-Estudantevalor-turma-12/<str:pk>/Ano/',select_estudante_turma_listValor3, name="select_estudante_turma_listValor3"),
	# 10 Ano print
	path('Valor-Reportestudate10-ano/periodu/print/<str:idEst>', ReportValorEstudantePeriod_Print, name="ReportValorEstudantePeriod_Print"),
	path('Valor-Reportestudate10-ano/II-periodu/print/<str:idEst>', ReportValorEstudanteIIPeriod_Print, name="ReportValorEstudanteIIPeriod_Print"),
	path('Valor-Reportestudate10-ano/III-periodu/print/<str:idEst>', ReportValorEstudanteIIIPeriod_Print, name="ReportValorEstudanteIIIPeriod_Print"),
	# 11 Ano print
	path('Valor-Reportestudate11-ano/periodu/print/<str:idEst>', ReportValorEstudantePeriod_Print11ano, name="ReportValorEstudantePeriod_Print11ano"),
	path('Valor-Reportestudate11-ano/II-periodu/print/<str:idEst>', ReportValorEstudanteIIPeriod_Print11ano, name="ReportValorEstudanteIIPeriod_Print11ano"),
	path('Valor-Reportestudate11-ano/III-periodu/print/<str:idEst>', ReportValorEstudanteIIIPeriod_Print11ano, name="ReportValorEstudanteIIIPeriod_Print11ano"),

	# 12 Ano print
	path('Valor-Reportestudate12-ano/periodu/print/<str:idEst>', ReportValorEstudantePeriod_Print12ano, name="ReportValorEstudantePeriod_Print12ano"),
	path('Valor-Reportestudate12-ano/II-periodu/print/<str:idEst>', ReportValorEstudanteIIPeriod_Print12ano, name="ReportValorEstudanteIIPeriod_Print12ano"),
	path('Valor-Reportestudate12-ano/III-periodu/print/<str:idEst>', ReportValorEstudanteIIIPeriod_Print12ano, name="ReportValorEstudanteIIIPeriod_Print12ano"),


	path('lista-report-tabular-grafico', listaReport, name="listaReport"),
	path('lista-report-valores-Gerais-Estudantes', listaReportValorClasseJeral, name="listaReportValorClasseJeral"),
	path('report-chart-grafico-Alumni', report_shartAlumni, name="report_shartAlumni"),
	path('report-tabular-Alumni', report_TabularAlumni, name="report_TabularAlumni"),
	path('report-tabular-Professores', report_TabularProf, name="report_TabularProf"),

	# Sajobril Report Grafiku
	path('Student/', ReportStudentStats, name="report-student-stats"),
	path('Funsionariu/', ReportFunStats, name="report-fun-stats"),
	
	# Staff filtered views
	path('staff/all/', AllStaff, name="staff-all"),
	path('staff/gender/<str:gender>/', StaffByGender, name="staff-by-gender"),
	path('staff/municipality/<int:municipality_id>/', StaffByMunicipality, name="staff-by-municipality"),
	path('staff/education/<str:education_level>/', StaffByEducation, name="staff-by-education"),
	path('staff/status/<str:status>/', StaffByStatus, name="staff-by-status"),
	path('staff/position/<str:position>/', StaffByPosition, name="staff-by-position"),
	path('staff/department/<int:department_id>/', StaffByDepartment, name="staff-by-department"),
	path('staff/study-area/<str:study_area>/', StaffByStudyArea, name="staff-by-study-area"),
	path('staff/civil-status/<str:civil_status>/', StaffByCivilStatus, name="staff-by-civil-status"),
	path('staff/with-classes/', StaffWithClasses, name="staff-with-classes"),
	path('staff/without-classes/', StaffWithoutClasses, name="staff-without-classes"),
	
	# Student filtered views
	path('students/active/', StudentsActive, name="students-active"),
	path('students/gender/<str:gender>/', StudentsByGender, name="students-by-gender"),
	path('students/class/<str:class_name>/', StudentsByClass, name="students-by-class"),
	path('students/alumni/', StudentsAlumni, name="students-alumni"),
	path('students/transferred-in/', StudentsTransferredIn, name="students-transferred-in"),
	path('students/transferred-out/', StudentsTransferredOut, name="students-transferred-out"),
	
]