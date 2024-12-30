from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_employees/', views.dashboard_employees, name='dashboard_employees'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),

    path('approve_document/<int:document_id>/', views.approve_document, name='approve_document'),
    path('reject_document/<int:document_id>/', views.reject_document, name='reject_document'),
    

    path('edit_document/<int:document_id>/', views.edit_document, name='edit_document'),
    path('upload/', views.upload_file, name='upload_file'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('Financedash/', views.Financedash, name='Financedash'),
     path('itdash/', views.itdash, name='itdash'),
    
]
