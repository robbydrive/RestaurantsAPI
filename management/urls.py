from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    url(r'^login/',
        LoginView.as_view(template_name='management/login.html'), name='login'),
    url(r'^logout/',
        LogoutView.as_view(template_name='management/logout.html',
                           next_page=reverse_lazy('management:login')), name='logout'),
    url(r'^categories/(?:(?P<parent_id>\d+)/)?$', CategoriesListView.as_view(), name='categories'),
    url(r'^categories/add/(?:(?P<parent_id>\d+)/)?$', CategoryCreate.as_view(), name='add_category'),
    url(r'^categories/edit/(?P<pk>\d+)/$', CategoryUpdate.as_view(), name='edit_category'),
    url(r'^dishes/(?P<category_id>\d+)/$', DishesListView.as_view(), name='dishes'),
    url(r'^dishes/add/(?:(?P<category_id>\d+)/)?$', DishCreate.as_view(), name='add_dish'),
    url(r'^dishes/edit/(?P<pk>\d+)/$', DishUpdate.as_view(), name='edit_dish'),
    url(r'^orders/$', OrdersListView.as_view(), name='orders'),
    url(r'^orders/edit/(?P<pk>\d+)/$', OrderUpdate.as_view(), name='edit_order'),
    url(r'^$', index, name='index'),
]