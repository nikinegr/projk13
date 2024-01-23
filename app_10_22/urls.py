from django.contrib import admin
from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings


# urlpatterns = [
#     path('', views.Home.as_view(), name='home'),
#     path('project_create/', views. Create_project.as_view(), name='pr'),
#     path('edit project/<int:id>/', views.edit_project),
#     path('login', views.LoginPage.as_view())
# #path('test/', views. TestPage.as_view())
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('profile/<int:id>/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('project_create/', views. Create_project.as_view(), name='pr'),
    path('project/<int:id>/', views.project),
    path('login/', views.login_page, name='login'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit project/<int:id>/', views.edit_project),
    path('comment/<int:comment_id>/', views.comment, name='comment_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('search/', views.user_search, name='search_users'),
    path('searchingUser/', views.SearchPage.as_view(), name='search_users'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('all_posts/', views.main_post, name='main_post')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
