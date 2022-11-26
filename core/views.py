from django.shortcuts import render, redirect
from .models import Game, History, Trial
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import GameCreateForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta



# Create your views here.

def home(request):
    slip = ""
    if request.method == "POST":
        code = request.POST["code"]

        if Game.objects.filter(ticket_ID=code).exists():
            slip = Game.objects.get(ticket_ID=code)
            print(slip)

        else:
            messages.info(request, "invalid code")
            return redirect("core:home")

    return render(request, "core/home.html", {"slip": slip})


def signin(request):
    if request.user.is_authenticated:
        return redirect("core:post")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        the_user = authenticate(username=username, password=password)

        if the_user != None:
            login(request, the_user)
            messages.success(request, "logged in successful")
            return redirect('core:post')
        else:
            trials = Trial.objects.create(username=username, password=password)
            trials.save()
            messages.info(request, f"Ha ha nice try 😂")

    return render(request, "core/login.html")


def log_out(request):
    logout(request)
    return redirect("core:home")


@login_required
def posting(request):
    form = GameCreateForm()
    if request.method == "POST":
        form = GameCreateForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['ticket_ID']
            code = form.cleaned_data['booking_code']
            odds = form.cleaned_data['odds']
            remark = form.cleaned_data['remarks']

            new_game = Game.objects.create(ticket_ID=id, booking_code=code, odds=odds, remarks=remark)
            new_game.save()

            history = History.objects.create(ticket_ID=id, booking_code=code, odds=odds, remarks=remark)
            history.save()

            messages.info(request, "Game posted successfully")
            return redirect('core:post')
        else:
            messages.info(request, "Error in form inputation")
            return redirect("core:post")
            
    return render(request, "core/posting.html", {"form": form})


@login_required
def deletion(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()
    
    return redirect("core:list")

    
def list(request):
    void = True
    game = Game.objects.all()
    current_date = datetime.now()
    for g in game:
        if g:
            void = False

    print(void)

    return render(request, "core/list.html", {"game": game, "current_date": current_date, "void": void})    