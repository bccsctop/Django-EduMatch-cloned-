from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
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
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('review/<int:tutor_id>',views.review, name='review'),
    path('review/remove/<int:tutor_id>/<int:review_id>', views.remove_review, name='remove_review'),
    path('about/group',views.about_group, name='about_group'),
    path('about/app',views.about_app, name='about_app'),
    path('friendprofile/<int:tutor_id>',views.friend_profile, name='friend_profile'),
    path('help', views.help_user, name='help_user'),
    path('help/answer/<int:answer_page>', views.answer_user, name='answer_user'),
]