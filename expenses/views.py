from django.shortcuts import render, redirect
from calendar import month_name
from .forms import ExpenseForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
import csv
import openpyxl
from .forms import BudgetForm
from .models import Budget
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Sum
from django.http import JsonResponse
from .models import Budget, Expense


# Create your views here.
@login_required(login_url='login-user')
def index(request):
    today = datetime.today()
    month = today.month
    year = today.year

    budget = Budget.objects.filter(user=request.user, month=month, year=year).first()
    expenses = Expense.objects.filter(user=request.user, date__month=month, date__year=year)

    total_spent = sum(e.amount for e in expenses)
    remaining = budget.amount - total_spent if budget else 0
    percent_used = (total_spent / budget.amount * 100) if budget and budget.amount > 0 else 0

    context = {
        'expenses': expenses,
        'budget': budget,
        'total_spent': total_spent,
        'remaining': remaining,
        'percent_used': round(percent_used, 2),
    }

    return render(request, 'expenses/index.html', context)


@login_required(login_url='login-user')
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # assign current user
            expense.save()
            messages.success(request, 'Added Successfully!')
            return redirect('index')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required(login_url='login-user')
def edit_expense(request, pk):
    try:
        expense = Expense.objects.get(pk=pk, user=request.user)
    except Expense.DoesNotExist:
        raise Http404("Expense not found.")

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Successfully!')
            return redirect('index')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/edit_expense.html', {'form': form})

@login_required(login_url='login-user')
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('index')

    return render(request, 'expenses/delete_expense.html', {'expense': expense})


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login-user')
    else:
        form = RegisterForm()
    return render(request, 'expenses/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'expenses/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login-user')

@login_required(login_url='login-user')
def export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Expenses"

    ws.append(['Amount', 'Description', 'Category', 'Date'])

    # 🔥 Only user-specific expenses
    expenses = Expense.objects.filter(user=request.user)

    for expense in expenses:
        ws.append([
            expense.amount,
            expense.description,
            expense.category,
            expense.date.strftime('%Y-%m-%d')
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=expenses.xlsx'
    wb.save(response)
    return response

@login_required(login_url='login-user')
def expense_summary(request):
    summary = Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))
    data = {
        'labels': [item['category'] for item in summary],
        'data': [item['total'] for item in summary],
    }
    return JsonResponse(data)

@login_required
def budget_view(request):
    today = datetime.today()
    month = request.GET.get('month', today.month)
    year = request.GET.get('year', today.year)

    budget, created = Budget.objects.get_or_create(
        user=request.user, month=month, year=year,
        defaults={'amount': 0}
    )

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget')  # replace with your url name
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'expenses/budget.html', {'form': form, 'budget': budget})

@login_required
def budget_summary_view(request):
    today = datetime.today()
    month = today.month
    year = today.year

    budget = Budget.objects.filter(user=request.user, month=month, year=year).first()
    expenses = Expense.objects.filter(user=request.user, date__month=month, date__year=year)

    total_spent = sum(e.amount for e in expenses)
    remaining = budget.amount - total_spent if budget else 0
    percent_used = (total_spent / budget.amount * 100) if budget and budget.amount > 0 else 0

    return render(request, 'expenses/budget_summary.html', {
        'budget': budget,
        'total_spent': total_spent,
        'remaining': remaining,
        'percent_used': round(percent_used, 2)
    })

@login_required
def dashboard_view(request):
    today = datetime.today()
    month = today.month
    year = today.year

    # Budget for the current user/month
    budget = Budget.objects.filter(user=request.user, month=month, year=year).first()
    expenses = Expense.objects.filter(user=request.user, date__month=month, date__year=year)

    total_spent = sum(e.amount for e in expenses)
    remaining = budget.amount - total_spent if budget else 0
    percent_used = (total_spent / budget.amount * 100) if budget and budget.amount > 0 else 0

    context = {
        'budget': budget,
        'total_spent': total_spent,
        'remaining': remaining,
        'percent_used': round(percent_used, 2),
        # ... add your other context data here ...
    }

    return render(request, 'expenses/index.html', context)

@login_required
def budget_history_view(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-year', '-month')
    history = []

    for b in budgets:
        expenses = Expense.objects.filter(
            user=request.user,
            date__month=b.month,
            date__year=b.year
        )
        total_spent = sum(e.amount for e in expenses)
        percent_used = (total_spent / b.amount * 100) if b.amount > 0 else 0

        history.append({
            'month_name': month_name[b.month],
            'year': b.year,
            'budget': b.amount,
            'spent': total_spent,
            'percent_used': round(percent_used, 2)
        })

    return render(request, 'expenses/budget_history.html', {'history': history})

@login_required
def export_budget_history_csv(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-year', '-month')

    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="budget_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Month', 'Year', 'Budget', 'Spent', 'Percent Used'])

    for b in budgets:
        expenses = Expense.objects.filter(
            user=request.user,
            date__month=b.month,
            date__year=b.year
        )
        total_spent = sum(e.amount for e in expenses)
        percent_used = (total_spent / b.amount * 100) if b.amount > 0 else 0

        writer.writerow([
            month_name[b.month],
            b.year,
            f"{b.amount:.2f}",
            f"{total_spent:.2f}",
            f"{round(percent_used, 2)}%"
        ])

    return response