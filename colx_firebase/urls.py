"""mysite URL Configuration

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

from django.contrib import admin

from django.conf.urls import url 

from . import views

app_name="colx_firebase"
urlpatterns = [

url('signup/',views.signup, name="signup"),
url('login/',views.login, name="login"),
url('logout/',views.logout, name="logout"),
url('sell/',views.sell,name='sell'),
#
url('add_to_cart/',views.add_to_cart,name='add_to_cart'),
url(r'buy/(?P<userid>.+)/(?P<itemid>.+)/$',views.buy,name='buy'),
url('cart/',views.cart,name='cart'),
url('',views.index,name='index'),

]

