#from django.shortcuts import render
from django.urls import path
from.import views


urlpatterns=[
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('faq',views.faq,name='faq'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),

   
]

