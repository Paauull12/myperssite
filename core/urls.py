from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cv/', views.cvpage, name='cv'),
    path('contact/', views.contact, name='contact'),
    path('meditatii/', include('meditatii.urls')),
]