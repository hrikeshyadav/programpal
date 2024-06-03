
from django.urls import path, include
from proapp.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [  
    # path('index/<pk>',index),
    path('home',home),
    path('index',index),
    path('login',ulogin),
    path('signup',signup),
    path('logout',ulogout),
    path('sample',sample),
    path('create-room',CreateRoom),
    path('update_room/<pk>',updateRoom),
    path('room/<pk>',room),
    path('deleteRoom/<pk>',deleteRoom),
    # path('delete/<pk>',delete),
    path('deleteMessage/<pk>',deleteMessage),
    path('userProfile/<pk>',userProfile),
    # path('updateUser/<pk>',updateUser),
    path('room/<int:pk>/', room, name='room'),
    


    path('courses',courses),
    # path('viewcard',viewcard),
    path('product_detail/<pid>',product_detail),
    path('orderc/<uid>',orderc),
    path('placeorder',placeorder),
    path('makepayment/<uid>',makepayment),
    path('fetchorder',fetchorder),
    path('paymentsucess',paymentsucess),
   

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) ## += means for creating new file statically