from django.shortcuts import render
import random
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    daily_special = [
        'Peppercorn Steak',
        'Pollo Tacos',
        'Garden Greens Salad',
        'Truffle Tortellini',
    ]

    context = {
        'daily_special': random.choice(daily_special),
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    '''Process form asubmission and generate result'''
    template_name = 'restaurant/confirmation.html'
    
    total = 0
    if request.POST:
        selected_items = request.POST.getlist('items[]')
        poke_toppings = request.POST.getlist('poke_toppings[]')

        prices = {
            'Steak+Sushi': 33,
            'Ahi Tuna Poke Bowl': 27,
            'Aburi Salmon Sushi Press': 21,
            'Jumbo Lump Crab Cake': 26,
            'Special' : 25
        }

        for item in selected_items:
            if item in prices:
                total += prices[item]
                
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')
        instructions = request.POST.get('instructions')

        minutes = random.randint(30,60)
        ready_time = timezone.now() + timedelta(minutes=minutes)

        context = {
            'items': selected_items,
            'poke_toppings': poke_toppings,
            'total': total,
            'name': customer_name,
            'email': customer_email,
            'phone_number': customer_phone,
            'instructions': instructions,
            'time': ready_time.strftime("%I:%M %p"),
        }

        return render(request, template_name=template_name, context=context)
    else:
        return redirect('order')