from django import forms
from .models import Product, Order, Expense, StockEntry, Invoice

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_amount']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date']

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ['product', 'quantity_change', 'notes']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['order', 'invoice_number', 'due_date']