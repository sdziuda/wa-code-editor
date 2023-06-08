from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('compile/', views.compile_no_file, name='compile_no_file'),
    path('compile/<int:file_id>', views.compile_file, name='compile_file'),
    path('save/<int:file_id>', views.save_asm, name='save_asm'),
    path('save_file/<int:file_id>', views.save_file, name='save_file'),
    path('<int:file_id>/', views.index, name='index_file'),
    path('delete_file/<int:file_id>', views.delete_file, name='delete_file'),
    path('delete_file_no/<int:file_id>', views.delete_file_no, name='delete_file_no'),
    path('delete_dir/<int:dir_id>', views.delete_dir, name='delete_dir'),
    path('delete_dir_no/<int:dir_id>', views.delete_dir_no, name='delete_dir_no'),
    path('delete/', views.delete_choose, name='delete_choose'),
    path('add_dir/', views.add_dir_choose, name='add_dir_choose'),
    path('add_file/', views.add_file_choose, name='add_file_choose'),
    path('add_dir/<int:dir_id>', views.add_dir, name='add_dir'),
    path('add_file/<int:dir_id>', views.add_file, name='add_file'),
]
