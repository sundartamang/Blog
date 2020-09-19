from django.urls import path,include
from django.conf.urls import include, url
from .views import (
    homeView,
    contact,
    blogDetail,
    archive,
    category,
    # newsletterSubscribe,
    # postComment,
)
app_name = 'core'

urlpatterns = [
    path('', homeView,name='home'),
    path('contact/', contact,name='contact'),
    path('category/<slug>/', category,name='category'),
    path('archive/', archive,name='archive'),
    path('details/<slug>/', blogDetail,name='details'),
    # path('subscribe', newsletterSubscribe, name='subscribe'),
    # path('post-comment/<slug>/', postComment,name='post-comment'),
]