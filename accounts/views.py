from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse


from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from upload_img.forms import CommentForm

from upload_img.models import Image, Comment

# Create your views here.


# User Profile



def profile_detail(request, user_id):
    comments = Comment.objects.all()
    user = get_object_or_404(User, id=user_id)
    images = user.image_set.all().order_by('-pub_date')

    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            img = request.POST.get('image')
            new_comment = c_form.save(commit=False)
            new_comment.owner = request.user
            new_comment.image = Image.objects.get(id=img)
            
            c_form.save()
            return HttpResponseRedirect(reverse("accounts:profile_detail", args=(user.id,)))

    else:
        c_form = CommentForm()
    context = {'user': user, 'images_temp': images, 'comments': comments, 'c_form': c_form}
    return render(request, 'profile/profile_detail.html', context)



# this function combines two Model Forms UserUpdateForm + ProfileUpdateForm
#todo:
# Update: urls.py
#         edit_profile.html
# delete path and html page for edit_profile_image

def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                            request, 
                            'Profile successfully updated!', 
                            extra_tags='alert alert-success alert-dismissible fade show')
            return HttpResponseRedirect(reverse("accounts:profile_detail", args=(user.id,)))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile/edit_profile.html', context)



def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) #<-- keeps the user logged on after changing the password
            # return redirect('upload_img:newsfeed')
            return HttpResponseRedirect(reverse("accounts:profile_detail", args=(user.id,)))
    else:
        form = PasswordChangeForm(user=request.user) #<--- instance=request.user prefilled the existing data to the form!!

    context = {'user': user, 'form_pw': form}
    return render(request, 'profile/change_password.html', context)



# Registration, Login, Logout


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Wrong user name or password')

    return render(request, 'accounts/login.html', {})


def logout_user(request):
    logout(request)
    # return HttpResponseRedirect(reverse('home'))
    return redirect('home')


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create_user(
                username, email=email, password=password)
            messages.success(
                request, '{}! You successfully registered your account!'.format(user.username))
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form_temp': form})
