from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    # path('tags/', views.all_tags, name='all_tags'),
    path('create/', views.create, name='create'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('tags/<slug:tag>/', views.per_tag, name='posts_by_tag'),
    path('', views.home, name='home'),
    path('<slug:slug>', views.detail, name='detail'),
]
