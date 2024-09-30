from django.shortcuts import render
import random
import time

# Create your views here.
def main(request):
    return render(request, 'main.html')

def order(request):
    menu_items = [
        {'name': 'Pizza', 'price': 12},
        {'name': 'Gold Leaf Truffle Butter Chicken Sandwich', 'price': 999},
        {'name': 'Fettucine Alfredo', 'price': 15},
        {'name': 'Salad', 'price': 10}
    ]

    special_items = [
        {'name': 'Mac and Cheese', 'price': 10},
        {'name': 'Fish and Chips', 'price': 10},
        {'name': 'Caesar Salad', 'price': 10}
    ]
    daily_special = random.choice(special_items)

    pizza_addons = [
        {'name': 'Extra Cheese', 'price': 2},
        {'name': 'Mushrooms', 'price': 1},
        {'name': 'Banana Peppers', 'price': 2}
    ]
    return render(request, 'order.html', {
        'menu_items': menu_items,
        'daily_special': daily_special,
        'pizza_addons': pizza_addons
    })


def confirmation(request):
    selected_items = request.POST.getlist('items')
    selected_addons = request.POST.getlist('pizza_addons')

    customer_name = request.POST.get('name')
    customer_phone = request.POST.get('phone')
    customer_email = request.POST.get('email')
    special_instructions = request.POST.get('instructions')

    menu_prices = {
        'Pizza': 12, 
        'Gold Leaf Truffle Butter Chicken Sandwich': 999, 
        'Fettucine Alfredo': 15, 
        'Salad': 10, 
        'Daily Special': 10
    }

    addon_prices = {
        'Extra Cheese': 2,
        'Mushrooms': 1,
        'Banana Peppers': 2
    }

    ordered_items = []
    total = 0

    for item in selected_items:
        item_price = menu_prices[item]
        ordered_item = {'name': item, 'price': item_price}

        if item == 'Pizza' and selected_addons:
            addons_list = [{'name': addon, 'price': addon_prices[addon]} for addon in selected_addons]
            ordered_item['addons'] = addons_list
            total += sum([addon['price'] for addon in addons_list])  
        
        ordered_items.append(ordered_item)
        total += item_price  


    ready_time = time.time() + random.randint(1800, 3600)

    return render(request, 'confirmation.html', {
        'customer_name': customer_name,
        'customer_phone': customer_phone,
        'customer_email': customer_email,
        'special_instructions': special_instructions,
        'ordered_items': ordered_items,
        'total': total,
        'ready_time': time.strftime('%H:%M:%S', time.localtime(ready_time))
    })

