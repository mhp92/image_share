from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Image, Comment

# for the exmple 1
from django.views.generic import ListView, CreateView


from .forms import ImageForm, CommentForm

# Create your views here.

#---------related to image_upload.html Vitor Freitas part2------------
@login_required
def image_upload(request):
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			new_image = form.save(commit=False)
			new_image.owner = request.user
			form.save()
			return redirect('upload_img:newsfeed')
	else:
		form = ImageForm()

	context = {'form': form}
	return render(request, 'image_upload.html', context)


def delete_image(request, image_id):

	image = get_object_or_404(Image, id=image_id)
	if request.user != image.owner:
		return redirect('/')

	if request.method == 'POST':
		image.delete()
		messages.success(
								request, 
								'Post successfully deleted!', 
								extra_tags='alert alert-success alert-dismissible fade show')

		return HttpResponseRedirect(reverse("accounts:profile_detail", args=(image.owner.id,)))
	return render(request, 'delete_image_confirm.html', {'image': image})


def delete_comment(request, comment_id):

	comment = get_object_or_404(Comment, id=comment_id)
	if request.user != comment.owner:
		return redirect('/')

	if request.method == 'POST':
		comment.delete()
		messages.success(
								request, 
								'Comment successfully deleted!', 
								extra_tags='alert alert-success alert-dismissible fade show')

		return redirect('upload_img:newsfeed')
	return render(request, 'delete_comment_confirm.html', {'comment': comment})


@login_required
def newsfeed(request):
	images = Image.objects.all().order_by('-pub_date') #[:6] #limit this line 
	reply_id = request.POST.get('comment_id')
	img_r_id = request.POST.get('image_r_id')
	img_id = request.POST.get('image_id')

	c_form = CommentForm(request.POST)
	if c_form.is_valid():
		if request.method == 'POST':
			if img_id:
				new_comment = c_form.save(commit=False)
				new_comment.owner = request.user
				new_comment.image = Image.objects.get(id=img_id)

				c_form.save()
				return redirect('upload_img:newsfeed')
			if reply_id:
				new_reply = c_form.save(commit=False)
				new_reply.owner = request.user
				new_reply.image = Image.objects.get(id=img_r_id)
				new_reply.reply = Comment.objects.get(id=reply_id)

				c_form.save()
				return redirect('upload_img:newsfeed')
	else:
		c_form = CommentForm()
		
		

	context = {'images_temp': images, 'c_form': c_form}
	return render(request, 'newsfeed.html', context)



@login_required
def image_detail_view(request, image_id):
	image = get_object_or_404(Image, id=image_id)

# comment on image
	if request.method == 'POST':
		c_form = CommentForm(request.POST)
		if c_form.is_valid():
			new_comment = c_form.save(commit=False)
			new_comment.owner = request.user
			new_comment.image = image
			c_form.save()
			return redirect('upload_img:newsfeed')

	else:
		c_form = CommentForm()

	context = {'image': image, 'c_form': c_form}
	return render(request, 'image/image_detail.html', context)















