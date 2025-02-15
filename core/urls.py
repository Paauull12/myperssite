from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cv/', views.cvpage, name='cv'),
    path('mediatii/', views.meditatiimock, name='meditatii'),
    path('contact/', views.contact, name='contact'),
]