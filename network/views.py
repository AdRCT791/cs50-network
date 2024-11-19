from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import NewPostForm
from .models import User, Post


def index(request):

    all_posts = Post.objects.all().order_by('-post_date')

    # Initilize post_form in the context
    post_form = NewPostForm()

    # Handle POST request and autenticated user
    if request.method =="POST" and request.user.is_authenticated:
        action = request.POST.get("action")
        if action == "new_post":
            return create_post(request)
    
    return render(request, "network/index.html", {
        "post_form": post_form,
        "posts": all_posts
    })

@login_required
def create_post (request):
    # Initialize form
    post_form = NewPostForm(request.POST)

    # Check if form is valid
    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.post_author = request.user
        post.post_text = post.post_text.capitalize()
        post.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "network/index.html", {
        "post_form": post_form
    })


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(post_author=user)

    return render(request, "network/profile.html", {
        "user": user,
        "user_posts": user_posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
