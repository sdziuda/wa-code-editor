from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('compile/', views.compile_no_file, name='compile_no_file'),
    path('compile/<int:file_id>', views.compile_file, name='compile_file'),
    path('<int:file_id>/', views.index, name='index_file'),
    path('delete_file/<int:file_id>', views.delete_file, name='delete_file'),
    path('delete_dir/<int:dir_id>', views.delete_dir, name='delete_dir'),
    path('delete/', views.delete_choose, name='delete_choose'),
    path('add_dir/', views.add_dir_choose, name='add_dir_choose'),
    path('add_file/', views.add_file_choose, name='add_file_choose'),
    path('add_dir/<int:dir_id>', views.add_dir, name='add_dir'),
    path('add_file/<int:dir_id>', views.add_file, name='add_file'),
]
