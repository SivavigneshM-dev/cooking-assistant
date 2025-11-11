from django.shortcuts import render

from .models import Dish 

def dish_detail(request, id):
    
    my_dish = Dish.objects.get(id=id)
    
    context = {
        'dish': my_dish,
    }
    
    return render(request, 'dish_details.html', context)

def dish_list(request):
    all_dishes = Dish.objects.all()
    
    context = {
        'dish_list': all_dishes,
    }
    
    return render(request, 'dishess.html', context)