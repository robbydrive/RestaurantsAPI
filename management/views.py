from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView
from api.models import Category, Dish, Order

LOGIN_URL_NAME = 'management:login'


def index(request):
    return HttpResponseRedirect(reverse_lazy('management:categories'))


@method_decorator(permission_required('api.view_categories', login_url=reverse_lazy(LOGIN_URL_NAME)),
                  name='dispatch')
class CategoriesListView(ListView):
    def get_queryset(self):
        try:
            self.parent = Category.objects.get(pk=self.kwargs.get('parent_id', None))
        except ObjectDoesNotExist:
            self.parent = None
        return Category.objects.filter(parent=self.parent)

    def get_context_data(self, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['parent_category'] = self.parent
        return context


@method_decorator(permission_required('api.view_categories', login_url=reverse_lazy(LOGIN_URL_NAME)),
                  name='dispatch')
class DishesListView(ListView):
    def get_queryset(self):
        return Dish.objects.filter(category_id=self.kwargs.get('category_id', None))


@method_decorator(permission_required('api.view_orders', login_url=reverse_lazy(LOGIN_URL_NAME)),
                  name='dispatch')
class OrdersListView(ListView):
    model = Order


@method_decorator(permission_required('api.create_categories', login_url=reverse_lazy(LOGIN_URL_NAME)),
                  name='dispatch')
class CategoryCreate(CreateView):
    model = Category
    fields = ['name', 'parent']

    def get_initial(self):
        try:
            parent = Category.objects.get(pk=self.kwargs.get('parent_id', None))
        except ObjectDoesNotExist:
            parent = None
        return {
            'parent': parent
        }

    def get_context_data(self, **kwargs):
        context = super(CategoryCreate, self).get_context_data(**kwargs)
        context['is_creating'] = True
        return context

    def get_success_url(self):
        if self.get_form().instance.parent:
            kwargs = {'parent_id': self.get_form().instance.parent.id}
        else:
            kwargs = {}
        return reverse('management:categories', kwargs=kwargs)


@method_decorator(permission_required('api.edit_categories', login_url=reverse_lazy(LOGIN_URL_NAME)),
                  name='dispatch')
class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'parent']

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdate, self).get_context_data(**kwargs)
        context['is_creating'] = False
        return context

    def get_success_url(self):
        if self.get_form().instance.parent:
            kwargs = {'parent_id': self.get_form().instance.parent.id}
        else:
            kwargs = {}
        return reverse('management:categories', kwargs=kwargs)


@method_decorator(permission_required('api.create_categories', login_url=reverse_lazy(LOGIN_URL_NAME)),
                  name='dispatch')
class DishCreate(CreateView):
    model = Dish
    fields = ['name', 'price', 'category']

    def get_initial(self):
        try:
            category = Category.objects.get(pk=self.kwargs.get('category_id', None))
        except ObjectDoesNotExist:
            category = None
        return {
            'category': category
        }

    def get_context_data(self, **kwargs):
        context = super(DishCreate, self).get_context_data(**kwargs)
        context['is_creating'] = True
        return context

    def get_success_url(self):
        return reverse('management:dishes', kwargs={'category_id': self.get_form().instance.category.id})


@method_decorator(permission_required('api.edit_categories', login_url=reverse_lazy(LOGIN_URL_NAME)),
                  name='dispatch')
class DishUpdate(UpdateView):
    model = Dish
    fields = ['name', 'price', 'category']

    def get_context_data(self, **kwargs):
        context = super(DishUpdate, self).get_context_data(**kwargs)
        context['is_creating'] = False
        return context

    def get_success_url(self):
        return reverse('management:dishes', kwargs={'category_id': self.get_form().instance.category.id})


@method_decorator(permission_required('api.edit_orders', login_url=reverse_lazy(LOGIN_URL_NAME)),
                  name='dispatch')
class OrderUpdate(UpdateView):
    model = Order
    fields = ['status']

    def get_success_url(self):
        return reverse('management:orders')