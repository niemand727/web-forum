from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('create_forum/', views.create_forum, name='create_forum'),
    path('forum/<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('forum/<int:forum_id>/create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('', views.forum_list, name='forum_list'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
