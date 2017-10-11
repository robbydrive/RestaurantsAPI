from django.contrib import admin
from .models import Restaurant, Order, Dish, Category, OrderDish

models = [Restaurant, Order, Dish, Category, OrderDish]
admin.site.register(models)