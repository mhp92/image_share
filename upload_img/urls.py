from django.urls import path


from . import views


app_name = "upload_img"

urlpatterns = [

    path('upload/', views.image_upload, name='upload'),
    path('newsfeed/', views.newsfeed, name='newsfeed'),
    path('detail/<int:image_id>', views.image_detail_view, name='detail'),
    path('delete/image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('delete/comment/<int:comment_id>/', views.delete_comment, name='delete_comment')


]
