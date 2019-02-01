from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, View

from upload_img.models import Image, Comment
from upload_img.forms import ImageForm, CommentForm

# Create your views here.



class UploadImageView(CreateView):
	model = Image
	fields = ('title', 'image')
	# form_class = ImageForm
	success_url = reverse_lazy('classbasedview:newsfeed')
	template_name = 'class_image_upload.html'

# different NewsfeedView Versions for testing

# @login_required <--- doesn't work as expected
# class NewsfeedView(ListView):
# 	model = Image
# 	template_name = 'class_newsfeed.html'
# 	context_object_name = 'images_temp'




# class NewsfeedView(ListView):
# 	form_class = CommentForm
# 	context_object_name = 'c_form'

# 	def comment_form(self):
# 		return CommentForm

# 	def get_queryset_images(self):
# 		return Image.objects.all().order_by('-pub_date')

# 	def get_queryset_comments(self):
# 		return Comment.objects.all()
		
# 	def get(self, request):
# 		return render(
# 			request, 'class_newsfeed.html',
# 			{'images_temp': self.get_queryset_images(), 
# 			'comments': self.get_queryset_comments(), 
# 			'c_form': self.comment_form()}
# 			)
	
# from joincfe youtube tutorial

class NewsfeedView(ListView):
	queryset = Image.objects.all().order_by('-pub_date')
	template_name = 'class_newsfeed.html'
	context_object_name = 'images_temp'

class NewsfeedDetailView(DetailView):
	# queryset = Image.objects.all()
	template_name = 'class_newsfeed_detail.html'
	context_object_name = 'image'
	
	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Image, id=id_)
