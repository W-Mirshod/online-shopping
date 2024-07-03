from django.urls import path

from shopping.views.views import home_page, detail_page, about_page, add_product, add_comment, add_order, update_product
from shopping.views.auth import login_page, logout_page, logout_view, sign_up

urlpatterns = [
    path('', home_page, name='index'),
    path('category/<str:en_slug>/', home_page, name='category'),
    path('add_comment/<slug:en_slug>', add_comment, name='add_comment'),
    path('detail/<slug:en_slug>', detail_page, name='details'),
    path('add_product/', add_product, name='add_product'),
    path('update_product/<slug:en_slug>', update_product, name='update_product'),
    path('add_order/<slug:en_slug>', add_order, name='add_order'),
    path('about/', about_page, name='about'),

    path('login/', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout_page/', logout_page, name='logout_page'),
    path('register/', sign_up, name='register'),
]
