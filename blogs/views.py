from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import *
from .models import Blogs, Subscribers
from django.contrib.auth import login, logout
from django.core.mail import send_mail

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


def get_users(request, username, auth_user_id):
    users = User.objects.all()
    user_id = User.objects.get(username=username)
    subscription = Subscribers.objects.filter(user_to=user_id).filter(user_from=auth_user_id).exclude(user_to=auth_user_id).count()
    print(subscription)
    user_name = User.objects.get(username=username)
    posts = Blogs.objects.filter(author_id=int(user_name.pk))
    context = {
        'posts': posts,
        'users': users,
        'user_id': user_id,
        'subscription': subscription,
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


def add_post(request, auth_username, ):
    if request.method == 'POST':
        form = PostForm(request.POST)
        user = User.objects.get(username=auth_username)
        subscribers = Subscribers.objects.filter(user_to=user.pk).values_list('user_from', flat=True)
        subscribers_data = User.objects.filter(pk__in=subscribers).values_list('email', flat=True)

        for subs_email in subscribers_data:
            send_mail('New post', 'У пользователя {name} новый пост'.format(name=auth_username), 'maxba95@mail.ru', [subs_email], fail_silently=False)
        print(subscribers)
        if form.is_valid():
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
    users = User.objects.all()
    post_item = get_object_or_404(Blogs, pk=post_id) # возвращает 404, если объект модели не найден
    context = {
        'post_item': post_item,
        'users': users
    }
    return render(request=request, template_name='blogs/view_post.html', context=context)


def get_subscriptions(request, username):
    users = User.objects.all()
    user_name = User.objects.get(username=username)
    subscriptions = Subscribers.objects.filter(user_from=user_name.pk)
    subscriptions_id = subscriptions.values_list('user_to', flat=True)
    posts = Blogs.objects.filter(author_id__in=subscriptions_id)
    print(posts)
    context = {
        'posts': posts,
        'users': users,
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


def add_subscribe(request, user_id, auth_user_id):
    print(user_id, auth_user_id)
    Subscribers.objects.create(user_from_id=auth_user_id, user_to_id=user_id, )
    return redirect('home')


def remove_subscribe(request, user_id, auth_user_id):
    subs_id = Subscribers.objects.filter(user_to=user_id).filter(user_from=auth_user_id)
    subs_id.delete()
    return redirect('home')
