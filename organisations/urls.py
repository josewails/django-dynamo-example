from django.urls import path

from . import views

urlpatterns = [
    path('create', views.OrganisationCreateView.as_view(), name='organisation_create'),
    path('', views.OrganisationListView.as_view(), name='organisation_list'),
    path('projects/<str:organisation_id>', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<str:organisation_id>/<str:project_type>/<str:project_id>', views.ProjectDetailView.as_view(),
         name='project_detail'),
    path('employees/<str:organisation_id>/<str:project_id>', views.ProjectEmployeeListView.as_view(),
         name='project_employees'),
    path('projects/<str:organisation_id>/<str:employee_id>', views.EmployeeProjectListView.as_view(),
         name='employee_projects')
]
