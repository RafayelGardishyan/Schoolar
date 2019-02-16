from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('app/home/', views.app_home, name='app_home'),
    path('app/add/', views.add_list, name='add_list'),
    path('app/lists/', views.lists, name='lists'),
    path('app/test/<int:list_id>', views.test, name='test'),
    path('app/delete/<int:list_id>', views.delete, name='test'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/logged_out'}, name='logout'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('register', views.register)
]
