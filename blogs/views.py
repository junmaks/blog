from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import *
from .models import Blogs, Subscribers
from django.contrib.auth import login, logout

# Create your views here.
def index(request):
    posts = Blogs.objects.all()
    users = User.objects.all()
    context = {
        'posts': posts,
        'title': 'All posts',
        'users': users
    }
    return render(request=request, template_name='blogs/index.html',
                  context=context)


def get_users(request, username):
    users = User.objects.all()
    user_name = User.objects.get(username=username)
    posts = Blogs.objects.filter(author_id=int(user_name.pk))
    context = {
        'posts': posts,
        'users': users,
        'user_name': user_name,
    }
    return render(request=request, template_name='blogs/userblog.html',
                  context=context)


def get_my_blog(request, username):

    users = User.objects.all()
    user_name = User.objects.get(username=username)
    posts = Blogs.objects.filter(author_id=int(user_name.pk))
    followers = Subscribers.objects.filter(user_to=user_name.pk)
    context = {
        'posts': posts,
        'users': users,
        'user_name': user_name,
        'followers': followers
    }
    return render(request=request, template_name='blogs/my_blog.html',
                  context=context)


def add_post(request, username, ):
    if request.method == 'POST':
        form = PostForm(request.POST)
        user = User.objects.get(username=username)
        print(user.pk)
        if form.is_valid():
            # print(form.cleaned_data) cleaned_data - словарь
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            Blogs.objects.create(title=title, content=content, author_id=user.pk, )
            return redirect('home')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request=request, template_name='blogs/new_post.html', context=context)


def view_post(request, post_id):
    # post = Blogs.objects.get(id=post_id)
    post_item = get_object_or_404(Blogs, pk=post_id) # возвращает 404, если объект модели не найден
    context = {
        'post_item': post_item,
    }
    return render(request=request, template_name='blogs/view_post.html', context=context)


def get_subscriptions(request, username):
    users = User.objects.all()
    user_name = User.objects.get(username=username)
    # posts = Blogs.objects.filter(author_id=int(user_name.pk))
    subscriptions = Subscribers.objects.filter(user_from=user_name.pk)
    subscriptionss = subscriptions.values_list('user_to', flat=True)
    print(subscriptionss)
    posts_list = []
    for post in subscriptionss:
        posts = Blogs.objects.filter(author_id=int(post))
        posts_list.append(posts)
        print(post)
    context = {
        'posts_list': posts_list,
        'user_name': user_name,
        'subscriptions': subscriptions,
    }
    return render(request=request, template_name='blogs/my_subscriptions.html', context=context)

def user_login(request):
    users = User.objects.all()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request=request, user=user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request=request, template_name='blogs/login.html', context={'form': form, 'users': users})


def user_logout(request):
    logout(request)
    return redirect('login')