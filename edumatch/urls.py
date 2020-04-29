"""edumatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
#from django.urls import include, path
from django.contrib import admin
from django.urls import path, include
from edu import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.home_page, name='homepage'),
    path('register', views.register, name='register'),
    path('match-result/', views.match_result, name='match_result'),
    path('match-request/send/<int:tutor_id>', views.send_match_request, name='send_match_request'),
    path('match-request/cancel/<int:tutor_id>', views.cancel_match_request, name='cancel_match_request'),
    path('match-request/accept/<int:tutor_id>', views.accept_match_request, name='accept_match_request'),
    path('match-request/reject/<int:tutor_id>', views.reject_match_request, name='reject_match_request'),
    path('match-request/unfriend/<int:tutor_id>', views.unfriend, name='unfriend'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile', views.view_profile, name='view_profile'),
    path('chat/', include('chat.urls')),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('review/<int:tutor_id>',views.review, name='review'),
    path('review/remove/<int:tutor_id>/<int:review_id>', views.remove_review, name='remove_review'),
    path('about/group',views.about_group, name='about_group'),
    path('about/app',views.about_app, name='about_app'),
    path('friendprofile/<int:tutor_id>',views.friend_profile, name='friend_profile'),
    path('help', views.help_user, name='help_user'),
    path('help/answer/<int:answer_page>', views.answer_user, name='answer_user'),
]