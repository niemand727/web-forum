from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('create_forum/', views.create_forum, name='create_forum'),
    path('forum/<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('forum/<int:forum_id>/create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
