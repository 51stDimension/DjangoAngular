from django.urls import path
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    path('website/',views.Landingview.as_view(),name="landing"),
    path('login/',views.user_login,name="login"),
    path('signup/',views.signup,name="create_user"),
    path('logout/',views.user_logout,name="logout"),
]
