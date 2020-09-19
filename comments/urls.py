from django.urls import path,include
from django.conf.urls import include, url
from .views import (
    comment_thread,
    # postComment,
)
app_name = 'comments'

urlpatterns = [
    # path('', homeView,name='home'),
    path('thread/<pk>/', comment_thread,name='thread'),
    # path('subscribe', newsletterSubscribe, name='subscribe'),
]