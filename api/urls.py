from django.conf.urls import url
from .views import CategoriesListView, OrdersCreateView

urlpatterns = [
    url(r'^categories/$', CategoriesListView.as_view(), name='categories'),
    url(r'^orders/$', OrdersCreateView.as_view(), name='orders'),
]