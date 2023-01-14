
from projects.models import Project
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm 
import pandas as pd
from .config import DB_ENGINE


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			profile = Profile(profile_name = user.username, score = 100)
			profile.save()
			login(request, user)
			#messages.success(request, "Registration successful.")
			return redirect("user_profile")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			profile = Profile.objects.get(profile_name = user.username)
			if user is not None:
				login(request, user)
				#messages.info(request, f"You are now logged in as {username}.")
				return redirect("user_profile")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def scoreboard_request(request,):
	user_profiles = Profile.objects.all()
	profile_list = []
	for user_profile in user_profiles:
		profile_list.append([user_profile.profile_name, user_profile.score])
	profile_list.sort(key = lambda x: x[1], reverse=True)
	context = {'profiles': profile_list}
	#profile = Profile.objects.get(profile_name = request.user.username)
	#context = {'profile': profile}
	return render(request, 'scoreboard.html', context)

def userprofile_request(request,):
	return render(request, 'user_profile.html')

def shareprediction_request(request,):
	stock_df = pd.read_sql('select distinct stock_name from stock_prices', DB_ENGINE)
	stock_list = stock_df['stock_name'].to_list()
	context = {
		'stock_list' : stock_list,
	}
	return render(request, 'share_prediction.html', context)


