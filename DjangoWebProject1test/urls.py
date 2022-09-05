"""
Definition of urls for DjangoWebProject1test.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('library/', views.library, name='library'),
    path('libraryStr/<str:user>', views.libraryStr, name='libraryStr'),
    path('showSearch/', views.showSearch, name='showSearch'),
    path('rent/<str:rented>', views.rent, name='rent'),
    path('myRent/', views.myRent, name='myRent'),
    path('returns/', views.returns, name='returns'),
    path('addBook/', views.addBook, name='addBook'),
    path('employeeLogin/', views.employeeLogin, name='employeeLogin'),
    path('rooms/', views.rooms, name='rooms'),
    path('leaveRoom/', views.leaveRoom, name='leaveRoom'),
    path('joinRoom/', views.joinRoom, name='joinRoom'),
]
