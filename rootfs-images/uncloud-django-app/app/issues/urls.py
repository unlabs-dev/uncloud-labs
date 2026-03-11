from django.urls import path
from . import views

urlpatterns = [
    path('', views.issue_list, name='issue_list'),
    path('issues/new/', views.issue_create, name='issue_create'),
    path('issues/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issues/<int:pk>/edit/', views.issue_edit, name='issue_edit'),
    path('issues/<int:pk>/delete/', views.issue_delete, name='issue_delete'),
    path('issues/<int:pk>/comments/add/', views.comment_add, name='comment_add'),
]
