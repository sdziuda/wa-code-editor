from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:file_id>/', views.index, name='index_file'),
    path('delete_file/<int:file_id>', views.delete_file, name='delete_file'),
    path('delete_dir/<int:dir_id>', views.delete_dir, name='delete_dir'),
    path('add_dir/<int:dir_id>', views.add_dir, name='add_dir'),
    path('add_file/<int:dir_id>', views.add_file, name='add_file'),
]
