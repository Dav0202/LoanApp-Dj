from django.urls import path, include
from users.views import RegisterView, CustomLoginView, LogoutView
 
 
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),    
]