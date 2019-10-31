from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('app/home/', views.app_home, name='app_home'),
    path('app/add/', views.add_list, name='add_list'),
    path('app/add/folder', views.add_folder, name='add_folder'),
    path('app/edit/<int:list>', views.edit_list, name='edit_list'),
    path('app/lists/', views.lists, name='lists'),
    path('app/view/folder/<int:folder_id>', views.view_folder, name='view_folder'),
    path('app/test/<int:list_id>', views.test, name='test'),
    path('app/delete/<int:list_id>', views.delete, name='test'),
    path('app/delete/folder/<int:folder_id>', views.delete_folder, name='delete_dolder'),
    path('app/test/register/', views.register_results, name='register_results'),
    path('app/result/<int:result_id>', views.results, name='results_page'),
    path('user/profile/', views.profile, name='user_profile'),
    path('user/profile/edit/', views.edit_profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), {'next_page': '/logged_out'}, name='logout'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('register', views.register),
    path('app/api/getlangcode', views.get_language_code, name="api/getlangcode"),
    path('app/folder/add/<int:folder_id>', views.add_to_folder, name='add_to_folder'),
    path('app/experimental/quick_learn', views.quick_learn, name="quick_learn")
]
