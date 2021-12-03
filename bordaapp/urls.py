from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    # PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ResultListView,
    ResultDetailView
)


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<int:pk>/', PostDetailView, name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('about/', views.about, name='about'),
    path('results', ResultListView.as_view(), name='results'),
    path('results/<int:pk>/', ResultDetailView, name='result_detail'),
]
