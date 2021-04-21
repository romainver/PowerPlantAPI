from django.urls import path

from . import views

urlpatterns = [
    path('productionplan', views.getproductionplan, name='productionplan'),
]