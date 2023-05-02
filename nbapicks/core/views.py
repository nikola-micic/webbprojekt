from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from core.models import Team, Game, Pick, CustomUser
import datetime
from core.forms import LoginForm, UserCreateForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def index(request):
    date_yesterday = datetime.date.today() - datetime.timedelta(days=1)
    date_today = datetime.date.today()
    date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    past_games_yesterday = Game.objects.filter(date=date_yesterday, winner__isnull=False)
    past_games_today = Game.objects.filter(date=date_today, winner__isnull=False)
    past_games = past_games_yesterday.union(past_games_today)
   
    upcoming_games_today = Game.objects.filter(date=date_today)
    upcoming_games_tomorrow = Game.objects.filter(date=date_tomorrow)
    upcoming_games = upcoming_games_today.union(upcoming_games_tomorrow)
    context = {'past_games': past_games, 'upcoming_games': upcoming_games}
    
    return render(request, "index.html", context)


def teams(request):
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'teams.html', context)

def teamsaz(request):
    teams = Team.objects.order_by('name')
    context = {'teams': teams}
    return render(request, 'teams.html', context)

def teamsza(request):
    teams = Team.objects.order_by('-name')
    context = {'teams': teams}
    return render(request, 'teams.html', context)


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome")
            return redirect(request.GET.get("next", "predictions"))
    else:
        form = LoginForm(request)
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect("index")

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'djangobre7@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
                    
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request, "password_reset.html", context={"password_reset_form":password_reset_form})


def register_user(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Success!")
            return redirect("login")
        else:
            return render(request, "register.html", {"form": form}, status=400)
    form = UserCreateForm()
    return render(request, "register.html", {"form": form})


def leaderboards(request):
    most_picks = CustomUser.objects.filter(total_picks__gte=3).order_by("-total_picks")[:10]
    most_successful = CustomUser.objects.filter(total_picks__gte=3).order_by("-successful_picks")[:10]
    highest_rate = CustomUser.objects.filter(total_picks__gte=3).order_by("-success_rate")[:10]
    
    return render(request, "leaderboards.html", {"most_successful": most_successful, "most_picks": most_picks, "highest_rate": highest_rate})

def leaderboards_detail(request, table):
    if table == "most-picks":
        title = "Users with most picks"
        most_picks = CustomUser.objects.filter(total_picks__gte=3).order_by("-total_picks")
        if most_picks.count() >= 50:
            paginator = Paginator(most_picks, 50)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "leaderboards_detail.html", {"title": title, "page_obj": page_obj})
        else:
            paginator = Paginator(most_picks, most_picks.count())
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "leaderboards_detail.html", {"title": title, "page_obj": page_obj})
        
    elif table == "most-successful":
        title = "Users with most successful picks"
        most_successful = CustomUser.objects.filter(total_picks__gte=3).order_by("-successful_picks")
        if most_successful.count() >= 50:
            paginator = Paginator(most_successful, 50)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "leaderboards_detail.html", {"title": title, "page_obj": page_obj})
        else:
            paginator = Paginator(most_successful, most_successful.count())
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "leaderboards_detail.html", {"title": title, "page_obj": page_obj})
        
    elif table == "highest-rate":
        title = "Users with highest predict rate"
        highest_rate = CustomUser.objects.filter(total_picks__gte=3).order_by("-success_rate")
        if highest_rate.count() >= 50:
            paginator = Paginator(highest_rate, 50)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "leaderboards_detail.html", {"title": title, "page_obj": page_obj})
        else:
            paginator = Paginator(highest_rate, highest_rate.count())
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "leaderboards_detail.html", {"title": title, "page_obj": page_obj})
    else:
        return render(request, "leaderboards_detail.html", status=400)


@login_required(login_url="login")
def predictions(request):
    user_picks = Pick.objects.filter(user=request.user)
    for pick in user_picks:
        if pick.game.date < datetime.date.today():
            user_picks = user_picks.exclude(id=pick.id)

    past_user_picks = Pick.objects.filter(user=request.user, successful_pick__isnull=False)
    for pick in past_user_picks:
        if datetime.date.today() - pick.game.date > datetime.timedelta(days=3):
            past_user_picks = past_user_picks.exclude(id=pick.id)
    past_user_picks = reversed(past_user_picks)
    
    date_today = datetime.date.today()
    date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    upcoming_games_today = Game.objects.filter(date=date_today)
    upcoming_games_tomorrow = Game.objects.filter(date=date_tomorrow)
    for pick in user_picks:
        upcoming_games_today = upcoming_games_today.exclude(id=pick.game.id)
        upcoming_games_tomorrow = upcoming_games_tomorrow.exclude(id=pick.game.id)

    upcoming_games = upcoming_games_today.union(upcoming_games_tomorrow)

    if request.method == "POST":
        user_pick = Pick()
        user_pick.user = request.user
        for k, v in request.POST.items():
            if "game" in k:
                try:
                    user_pick.game = Game.objects.get(id=v)
                except:
                    return render(request, 'predictions.html', {'upcoming_games': upcoming_games, 'user_picks': user_picks, 'past_user_picks': past_user_picks})

            if "team" in k:
                try:
                    user_pick.team_picked = Team.objects.get(name=v)
                except:
                    return render(request, 'predictions.html', {'upcoming_games': upcoming_games, 'user_picks': user_picks, 'past_user_picks': past_user_picks})
            
        try:
            Pick.objects.get(user=request.user, game=user_pick.game)
            Pick.objects.filter(user=request.user, game=user_pick.game).update(team_picked=user_pick.team_picked)
            return redirect("predictions")
        except:
            user_pick.save()
            user = CustomUser.objects.get(id=request.user.id)
            CustomUser.objects.filter(id=user.id).update(total_picks = user.total_picks + 1)
            return redirect("predictions")

    return render(request, 'predictions.html', {'upcoming_games': upcoming_games, 'user_picks': user_picks, 'past_user_picks': past_user_picks})


@login_required(login_url="login")
def pick_history(request):
    past_user_picks = Pick.objects.filter(user=request.user, successful_pick__isnull=False).order_by("-id")
    picks_length = past_user_picks.count()
    if past_user_picks.count() >= 10:
        paginator = Paginator(past_user_picks, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "pick_history.html", {"page_obj": page_obj})
    elif past_user_picks.count() < 10 and past_user_picks.count()>0:
        paginator = Paginator(past_user_picks, past_user_picks.count())
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "pick_history.html", {"page_obj": page_obj})
    else:
         return redirect("predictions")



''' Used as a base, thought it could be used for more detailed view upon expanding data in the future
@login_required(login_url="login")
def predict_game(request, game_id):
    game = Game.objects.get(id=game_id)
    user_pick = Pick()
    user_pick.user = request.user
    user_pick.game = game
    if request.method == "POST":
            for k, v in request.POST.items():
                if "team_picked" in k:
                    try:
                        user_pick.team_picked = Team.objects.get(name=v)
                    except:
                        return render(request, 'predict_game.html', {'game': game})
            try:
                Pick.objects.get(user=request.user, game=game)
                Pick.objects.filter(user=request.user, game=game).update(team_picked=user_pick.team_picked)
                return redirect("predictions")
            except:
                user_pick.save()
                return redirect("predictions")
            
    return render(request, 'predict_game.html', {'game': game})
'''


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message!")
            form = ContactForm()
            return render(request, 'contact.html', {"form": form})
        else:
            return render(request, 'contact.html', {"form": form})
    form = ContactForm()
    return render(request, 'contact.html', {"form": form})
