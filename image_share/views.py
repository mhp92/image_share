from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import Profile

def home_view(request):
	users = User.objects.all()
	context = {'users':users}
	return render(request, 'home.html', context)


