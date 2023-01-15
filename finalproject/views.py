
from projects.models import Project
from django.shortcuts import  render, redirect
from .forms import NewUserForm, NewFeedbackForm
from .models import Profile, Prediction
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import pandas as pd
from .functions import calculate_score
from datetime import datetime
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

def userprofile_request(request,):
	profile = Profile.objects.get(profile_name = request.user.username)
	#predictions
	followed_query = "select * from follow_table where follower = '{follower}'"
	followed_df = pd.read_sql(followed_query.format(follower = request.user.username), DB_ENGINE)
	followed_df = followed_df.drop_duplicates(['follower', 'followed'], keep = 'last')
	followed_list = followed_df[followed_df['isfollow']=="Follow"]["followed"].tolist()
	followed_profiles = Profile.objects.filter(profile_name__in=followed_list)

	follower_query = "select * from follow_table where followed = '{followed}'"
	follower_df = pd.read_sql(follower_query.format(followed = profile.profile_name), DB_ENGINE)
	follower_df = follower_df.drop_duplicates(['follower', 'followed'], keep = 'last')
	follower_list = follower_df[follower_df['isfollow']=="Follow"]["follower"].tolist()


	predictions = Prediction.objects.filter(user = request.user.username)
	profile = Profile.objects.get(profile_name = request.user.username)

	profile_info = {
		"profile_name": profile.profile_name,
		"score": profile.score,
		"followed_profiles": followed_profiles,
		"follower_count":len(follower_list),
		"predictions": predictions
	}
	
	return render(request, 'user_profile.html', context=profile_info)

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

def searchuser_request(request,):
	if request.method == "POST":
		data=request.POST
		page_type = data.get("page-type")
		profile = Profile.objects.filter(profile_name = data.get("other-username")).first()
		if profile:
			follow_select_query = '''
				select * from follow_table where follower = '{follower}' and followed='{followed}'
				'''
			follow_df = pd.read_sql(follow_select_query.format(follower = request.user.username, followed=profile.profile_name), 
					DB_ENGINE)
			if follow_df.empty:
				last_operation = "Unfollow"
			else:
				last_operation = follow_df["isfollow"].iloc[-1]
			if page_type =="search_page":
				if last_operation == "Follow":
					follow_type = "Unfollow"
				else:
					follow_type = "Follow"


				followed_query = "select * from follow_table where follower = '{follower}'"
				followed_df = pd.read_sql(followed_query.format(follower = profile.profile_name), DB_ENGINE)
				followed_df = followed_df.drop_duplicates(['follower', 'followed'], keep = 'last')
				followed_list = followed_df[followed_df['isfollow']=="Follow"]["followed"].tolist()
				followed_profiles = Profile.objects.filter(profile_name__in=followed_list)

				follower_query = "select * from follow_table where followed = '{followed}'"
				follower_df = pd.read_sql(follower_query.format(followed = profile.profile_name), DB_ENGINE)
				follower_df = follower_df.drop_duplicates(['follower', 'followed'], keep = 'last')
				follower_list = follower_df[follower_df['isfollow']=="Follow"]["follower"].tolist()
		

				predictions = Prediction.objects.filter(user = profile.profile_name)


				user_info = {
					"profile_name": profile.profile_name,
					"score": profile.score,
					"follow": follow_type,
					"followed_profiles": followed_profiles,
					"follower_count": len(follower_list),
					"predictions": predictions}


				return render(request, 'other_profiles.html', context=user_info)
		
		
			elif page_type == "follow_page":
				if last_operation == "Follow":
					insert_operation = "Unfollow"
				else:
					insert_operation = "Follow"
				follow_db_list = ['2022-12-11', request.user.username, profile.profile_name, insert_operation]
				follow_db_df = pd.DataFrame([follow_db_list], columns=["create_date", "follower", "followed","isfollow"])
				follow_db_df.to_sql('follow_table', DB_ENGINE, if_exists='append')
				follow_type = last_operation


				followed_query = "select * from follow_table where follower = '{follower}'"
				followed_df = pd.read_sql(followed_query.format(follower = profile.profile_name), DB_ENGINE)
				followed_df = followed_df.drop_duplicates(['follower', 'followed'], keep = 'last')
				followed_list = followed_df[followed_df['isfollow']=="Follow"]["followed"].tolist()
				followed_profiles = Profile.objects.filter(profile_name__in=followed_list)


				follower_query = "select * from follow_table where followed = '{followed}'"
				follower_df = pd.read_sql(follower_query.format(followed = profile.profile_name), DB_ENGINE)
				follower_df = follower_df.drop_duplicates(['follower', 'followed'], keep = 'last')
				follower_list = follower_df[follower_df['isfollow']=="Follow"]["follower"].tolist()

				predictions = Prediction.objects.filter(user = profile.profile_name)

				user_info = {
				"profile_name": profile.profile_name,
				"score": profile.score,
				"follow": follow_type,
				"followed_profiles": followed_profiles,
				"follower_count": len(follower_list),
				"predictions": predictions}
				print(follow_df)
				return render(request, 'other_profiles.html', context=user_info)
		else:
			print("This profile does not exist")
	return render(request, 'search_user.html')

def shareprediction_request(request,):
	stock_df = pd.read_sql('select distinct stock_name from stock_prices', DB_ENGINE)
	stock_list = stock_df['stock_name'].to_list()
	context = {
		'stock_list' : stock_list,
	}
	if request.method == "POST":
		data=request.POST
		prediction_info = {
		"selected_stock": data.get("selectitem"),
		"buy_price": data.get("buy-price"),
		"sell_price": data.get("sell-price"),
		"money_amount": data.get("money-amount"),
		"profile": Profile.objects.get(profile_name = request.user.username)}
		prediction = Prediction(user = request.user.username, prediction_date = "2022-12-11", stock_name = prediction_info["selected_stock"], buy_price = prediction_info["buy_price"], sell_price = prediction_info["sell_price"], money_amount = prediction_info["money_amount"])
		if prediction_info["buy_price"] != "" and prediction_info["sell_price"] != "" and prediction_info["money_amount"] != "":
			prediction.save()
			calculate_score(prediction_info)
		else:
			print("fields have null values")
		
	return render(request, 'share_prediction.html', context)

def sharefeedback_request(request,):
	if request.method == "POST":
		form = NewFeedbackForm(request.POST)
		if form.is_valid():
			feedback = form.cleaned_data['feedback']
			#messages.info(request, f"Your feedback is sent.")
	else:
		form = NewFeedbackForm()
	return render(request, 'share_feedback.html', context={"feedback_form":form})


