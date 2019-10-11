from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('trending/', views.trending, name="trending"),
    path('passbook/', views.passbook, name="passbook"),
    path('videocreate/',  views.Videocreate.as_view() , name="videocreate"),
    path('authorize/', views.AuthorizeView.as_view(), name='authorize'),
    # path('oauth2callback/', views.Oauth2CallbackView.as_view(), name='oauth2callback'),
    path('blockchainsignup/', views.BlockChainSignUp.as_view(), name='blockchainsignup'),
    path('myvideo/', views.myvideo, name='myvideo'),
    path('hotofferings/', views.hotofferings, name='hotofferings'),
]

# if settings.DEBUG:
#     urlpatterns += static(
#         settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(
#         settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
