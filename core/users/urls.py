from django.urls import path
from .views import signup, signin, signout, profile

app_name = 'user'


urlpatterns = [
    path('register/', signup, name='register'),
    # Users Login
    path('login/', signin, name='login'),
    path('profile/', profile, name='profile'),  # User profile

    path('logout/', signout, name='logout'),
]

