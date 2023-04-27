"""crime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from user import views
urlpatterns = [
        path('home/', views.home, name='home'),
        path('about_us/', views.about_us, name='about_us'),
        path('error/', views.error, name='error'),
        path('profile/', views.profile, name='profile'),
        path('add_like/', views.add_like, name='add_like'),
        path('dis_like/', views.dis_like, name='dis_like'),

        path('store_report/<int:id>', views.store_report, name='store_report'),
        path('show_profile/<int:id>', views.show_profile, name='show_profile'),
        path('delete_post/<int:id>', views.delete_post, name='delete_post'),


        path('register/', views.register, name='register'),
        path('store_profile/', views.store_profile, name='store_profile'),

        path('security/', views.security, name='security'),
        path('add_post/', views.add_post, name='add_post'),
        path('store_post/', views.store_post, name='store_post'),
        path('view_post/', views.view_post, name='view_post'),
        

        path('edit_profile/', views.edit_profile, name='edit_profile'),
        path('update_profile/<int:id>', views.update_profile, name='update_profile'),
        path('login/', views.login, name='login'),
        path('login_check/', views.login_check, name='login_check'),
        path('logout/', views.logout, name='logout'),


        path('post_details/<int:id>', views.post_details, name='post_details'),


        path('contact_us/', views.contact_us, name='contact_us'),
        path('store_contact/', views.store_contact, name='store_contact'),
        path('store_Quickcontact/', views.store_Quickcontact, name='store_Quickcontact'),
        path('store_feedback/', views.store_feedback, name='store_feedback'),

        path('store_comment/<int:id>', views.store_comment, name='store_comment'),
        path('change_password/', views.change_password, name='change_password'),
        path('change_password_update/', views.change_password_update, name='change_password_update'),

]
