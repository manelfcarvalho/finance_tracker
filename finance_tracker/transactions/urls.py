# transactions/urls.py
from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('view/', views.view_transactions, name='view_transactions'),
    path('analyze/', views.analyze, name='analyze'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

