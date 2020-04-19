from django.urls import path

from . import views

app_name = 'form'

urlpatterns = [
    path('personal-info/', views.PersonalInfoView.as_view(), name='personal_info'),
    path('thanks/', views.thanks, name='thanks'),
    path('pdf-image/', views.pdf_collector, name='pdf')
]
