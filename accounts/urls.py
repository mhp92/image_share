
from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.user_registration, name="register"),
    path(
    	'profile_detail/<int:user_id>/', 
    	views.profile_detail, 
    	name='profile_detail'
    	),
    path(
    	'profile_detail/edit_profile/<int:user_id>/', 
    	views.edit_profile, 
    	name="edit_profile"
    	),
    path(
    	'profile_detail/edit_profile/change_password/<int:user_id>/', 
    	views.change_password, 
    	name="change_password"
    	)
]
