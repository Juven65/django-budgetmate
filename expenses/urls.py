from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_expense, name='add-expense'),
    path('edit/<int:pk>/', views.edit_expense, name='edit-expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete-expense'),
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('export/excel/', views.export_excel, name='export-excel'),
    path('summary/', views.expense_summary, name='expense-summary'),
    path('budget/', views.budget_view, name='budget'),
    path('budget-summary/', views.budget_summary_view, name='budget-summary'),
    path('budget-history/', views.budget_history_view, name='budget-history'),
    path('budget-history/export-csv/', views.export_budget_history_csv, name='export-budget-csv'),
]
