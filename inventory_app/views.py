from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from .models import Product, Order, Expense, StockEntry, Invoice
from .forms import ProductForm, OrderForm, ExpenseForm, StockEntryForm, InvoiceForm
from .utils import generate_pdf
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def dashboard(request):
    products = Product.objects.all()[:5]
    orders = Order.objects.all().order_by('-order_date')[:5]
    expenses = Expense.objects.all().order_by('-date')[:5]
    context = {
        'products': products,
        'orders': orders,
        'expenses': expenses,
    }
    return render(request, 'inventory_app/dashboard.html', context)

# Product views
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory_app/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory_app/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory_app/product_form.html', {'form': form})

# Order views
@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'inventory_app/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'inventory_app/order_detail.html', {'order': order})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()
            messages.success(request, 'Order created successfully.')
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'inventory_app/order_form.html', {'form': form})

# Expense views
@login_required
def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'inventory_app/expense_list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense recorded successfully.')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'inventory_app/expense_form.html', {'form': form})

# Stock views
@login_required
def stock_list(request):
    stock_entries = StockEntry.objects.all().order_by('-date')
    return render(request, 'inventory_app/stock_list.html', {'stock_entries': stock_entries})

@login_required
def stock_entry_create(request):
    if request.method == 'POST':
        form = StockEntryForm(request.POST)
        if form.is_valid():
            stock_entry = form.save()
            product = stock_entry.product
            product.quantity += stock_entry.quantity_change
            product.save()
            messages.success(request, 'Stock entry recorded successfully.')
            return redirect('stock_list')
    else:
        form = StockEntryForm()
    return render(request, 'inventory_app/stock_entry_form.html', {'form': form})

# Invoice views
@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_date')
    return render(request, 'inventory_app/invoice_list.html', {'invoices': invoices})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'inventory_app/invoice_detail.html', {'invoice': invoice})

@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'inventory_app/invoice_form.html', {'form': form})

@login_required
def invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    context = {'invoice': invoice, 'currency': settings.CURRENCY}
    pdf = generate_pdf('inventory_app/invoice_pdf.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    return response