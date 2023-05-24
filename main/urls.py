from django.urls import path, include
from main import views

urlpatterns = [
    path('api/posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', views.PostRetrieveUpdateDeleteView.as_view(), name='post-retrieve-update-delete'),
]