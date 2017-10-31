from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect

from models import Post
from signupModel import SignUpForm


def login_view(request):
    if request.user.is_authenticated():
        messages.warning(request, 'you allready loged in')
        return redirect(main_page_view)
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            if '@' in username:
                try:
                    username = User.objects.get(email=username).username
                except:
                    pass
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(main_page_view)
            else:
                return render(request, 'temp.html')
        else:
            return render(request, 'login.html', )


def signup_view(request):
    if request.user.is_authenticated():
        messages.warning(request, 'you allready loged in')
        return render(request, 'blog.html')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                messages.info(request, 'you have loged in')
                return render(request, 'blog.html', )
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


def main_page_view(request):
    if request.user.is_authenticated():
        userlogedin = True
        username = request.user.get_username()
    else:
        userlogedin = False
        username = ""
    if request.method == 'POST' and request.user.is_authenticated():

        title = request.POST.get('title')
        text = request.POST.get('text')

        Post.objects.create(author=request.user, title=title, text=text)
        return HttpResponseRedirect('/blog')

    else:
        posts = Post.objects.order_by('published_date').all()
        return render(request, 'blog.html',
                      {
                          'posts': posts,
                          'userlogedin': userlogedin,
                          'username': username
                      })


@login_required(login_url='/blog/login/')
def post_view(request, pk):
    post = Post.objects.get(id=pk)
    print post.title
    return render(request, 'post.html', {'post': post})


