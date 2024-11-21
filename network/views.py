from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import NewPostForm
from .models import User, Post, Follow


def index(request):

    all_posts = Post.objects.all().order_by('-post_date')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    # Initilize post_form in the context
    post_form = NewPostForm()

    # Handle POST request and autenticated user
    if request.method =="POST" and request.user.is_authenticated:
        action = request.POST.get("action")
        if action == "new_post":
            return create_post(request)
    
    return render(request, "network/index.html", {
        "post_form": post_form,
        "posts": all_posts,
        "page_obj": page_obj,
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
    user_profile = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(post_author=user_profile)
    number_of_posts = len(user_posts)
    followed = user_profile.following.all()
    followers = user_profile.followers.all()
    number_of_following = len(followed)
    number_of_followers = len(followers)

    #forms
    #form_follow = FollowUserForm()

    if request.method == "POST" and request.user.is_authenticated:
        action = request.POST.get("action")
        if action == "follow":
            return follow_user(request, username)
        
    is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists() if request.user.is_authenticated else False

    context = {
        "user_profile": user_profile,
        "user_posts": user_posts,
        "number_of_posts": number_of_posts,
        "number_of_following": number_of_following,
        "number_of_followers": number_of_followers,
        "is_following": is_following,
    }

    return render(request, "network/profile.html", context)

@login_required
def follow_user(request, username):
    user_profile = get_object_or_404(User,username=username)
    user = request.user
    # check if user does not already follow the current user profile
    if Follow.objects.filter(follower=user, following=user_profile).exists():
        # Unfollow
        Follow.objects.filter(follower=user, following=user_profile).delete()
    else:
        # Follow
        Follow.objects.create(follower=user, following=user_profile)

    print(f"Redirecting to profile of: {username}")
    return HttpResponseRedirect(reverse("profile", kwargs={"username":username}))


def following_view(request, username):
    user = get_object_or_404(User, username=username)
    followed_users = user.following.all()
    post_by_followed_users = Post.objects.filter(post_author__in=followed_users)

    return render(request, "network/following.html", {
        "post_by_followed_users": post_by_followed_users,
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
