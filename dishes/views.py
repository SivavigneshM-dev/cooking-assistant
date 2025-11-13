from django.shortcuts import render 
from .models import Dish 

def main(request):
    return render(request, 'main.html')

def dish_list(request):
    all_dishes = Dish.objects.all() 
    
    context = {
        'dishes_list': all_dishes, 
    }
    
    return render(request,'dishes.html', context)

def dish_detail(request, id):
    my_dish = Dish.objects.get(id=id)
    context = {
        'dish': my_dish,
    }
    return render(request,'dish_details.html', context)