from django.urls import path
from . import views


urlpatterns = [
    path("add/", views.add, name='add'),
    path("transactions/", views.transactions, name='transactions'),
    path("", views.index, name='index')
]