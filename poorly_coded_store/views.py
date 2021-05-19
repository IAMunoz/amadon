from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    if request.method == 'POST':
        quantity_from_form = int(request.POST["quantity"])
        price_from_form = float(request.POST["price"])
        total_charge = quantity_from_form * price_from_form
        print("Charging credit card...")
        Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
        return redirect(checkout)
    else:
        quantity_ordered = Order.objects.last().quantity_ordered
        total_price = Order.objects.last().total_price
        total_spent = Order.objects.aggregate(suma=Sum('total_price'))
        total_qty = Order.objects.aggregate(items=Sum('quantity_ordered'))
        context ={
            'total': total_price,
            'qty' : quantity_ordered,
            'total_spent' : total_spent.get('suma'),
            'total_qty' : total_qty.get('items')
        }
    return render(request, "store/checkout.html", context)