# transactions/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm  # criaremos esse formulário
from django.db.models import Sum , Q, F, DecimalField, FloatField
from django.db.models.functions import Coalesce , TruncMonth
from django.db.models.expressions import ExpressionWrapper
from django.contrib.auth.decorators import login_required
from decimal import Decimal

def home(request):
    return render(request, 'transactions/home.html')

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # Salva associando ao usuário logado
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transactions:dashboard')  # Redireciona após salvar
        else:
            print(form.errors)  # Debug: veja os erros no console
    else:
        form = TransactionForm()
    
    return render(request, 'transactions/add_transaction.html', {'form': form})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions/view_transactions.html', {'transactions': transactions})

@login_required
def analyze(request):
    income_total = Transaction.objects.filter(user=request.user, transaction_type='income') \
                    .aggregate(total=Sum('amount'))['total'] or 0
    expense_total = Transaction.objects.filter(user=request.user, transaction_type='expense') \
                     .aggregate(total=Sum('amount'))['total'] or 0
    balance = income_total - expense_total
    context = {
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
    }
    return render(request, 'transactions/analyze.html', context)

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transactions:view_transactions')
    return render(request, 'transactions/confirm_delete.html', {'transaction': transaction})

@login_required
def dashboard(request):
    # 1. Calcula os totais gerais
    financial_data = Transaction.objects.filter(user=request.user).aggregate(
        total_income=Coalesce(Sum('amount', filter=Q(transaction_type='income')), Decimal(0)),
        total_expense=Coalesce(Sum('amount', filter=Q(transaction_type='expense')), Decimal(0)),
    )
    
    # Calcula o saldo
    balance = financial_data['total_income'] - financial_data['total_expense']

    # 2. Resumo por categoria (evita divisão por zero e garante DecimalField)
    category_summary = []
    if financial_data['total_expense'] != 0:
        category_summary = (
            Transaction.objects
            .filter(user=request.user, transaction_type='expense')
            .values('category')
            .annotate(
                total=Sum('amount', output_field=DecimalField()),  # Garante DecimalField
                percentage=ExpressionWrapper(
                    (Sum('amount', output_field=DecimalField()) / financial_data['total_expense']) * Decimal(100),
                    output_field=DecimalField()  # Agora, ambos os lados são DecimalField
                )
            )
            .order_by('-total')[:5]
        )

    # 3. Últimas transações
    last_transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]

    # 4. Comparação mensal (garantindo DecimalField)
    monthly_comparison = (
        Transaction.objects
        .filter(user=request.user)
        .annotate(month=TruncMonth('date'))  # Agrupa por mês
        .values('month')
        .annotate(
            income=Coalesce(Sum('amount', filter=Q(transaction_type='income')), Decimal(0)),
            expense=Coalesce(Sum('amount', filter=Q(transaction_type='expense')), Decimal(0)),
            balance=ExpressionWrapper(
                F('income') - F('expense'),
                output_field=DecimalField()  # Agora, tudo é DecimalField
            )
        )
        .order_by('-month')[:6]  # Últimos 6 meses
    )

    context = {
        'income_total': financial_data['total_income'],
        'expense_total': financial_data['total_expense'],
        'balance': balance,
        'category_summary': category_summary,
        'last_transactions': last_transactions,
        'monthly_comparison': monthly_comparison,
    }
    
    return render(request, 'transactions/dashboard.html', context)