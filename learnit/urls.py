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
    path('app/test/register/', views.register_results, name='register_results'),
    path('app/result/<int:result_id>', views.results, name='results_page'),
    path('user/profile/', views.profile, name='user_profile'),
    path('user/profile/edit/', views.edit_profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), {'next_page': '/logged_out'}, name='logout'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('register', views.register)
]
