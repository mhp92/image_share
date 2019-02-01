from django.urls import path


from . import views




app_name = "classbasedview"

urlpatterns = [

    path('newsfeed/', views.NewsfeedView.as_view(), name='newsfeed'),
    path('newsfeed/detail/<int:id>/', views.NewsfeedDetailView.as_view(), name='newsfeed_detail'),
    path('upload/', views.UploadImageView.as_view(), name='upload'),
    

 
]
