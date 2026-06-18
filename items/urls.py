from django.urls import path
from . import views
urlpatterns=[
    path('', views.login, name='login'),
    path('main/', views.main, name='main'),
    path('main/items/', views.items, name='items'),
    path('main/items/details/<int:id>/', views.details, name='details'),
    path('main/create/', views.create, name='create'),
    path('main/update/', views.update, name='update'),
    path('main/dealer/', views.dealer, name='dealer'),
    path('main/logout', views.logout, name='logout')
]