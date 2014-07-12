from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from datetime import datetime
from outcumbent.models import *

navmenu = [{'title': 'Post New Topic', 'path': '/topic?activity=addpost'},]

votedict = {'disapprove': 0,
            'approve': 1,
            'complicated': 2}

def home(request):
    title = 'Home'
    return render_to_response('home.html',
                              dict(title=title, navmenu=navmenu),
                              context_instance=RequestContext(request))

def loginpage(request):
    title = 'Login'
    flash = ""
    form = AuthenticationForm
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/', context_instance=RequestContext(request))
            else:
                flash = "Account is Disabled."
        else:
            flash = "Invalid Login."
    return render_to_response('login.html',
                              dict(title=title, navmenu=navmenu, form=form, flash=flash),
                              context_instance=RequestContext(request))

def logoutpage(request):
    logout(request)
    return redirect("/login/", context_instance=RequestContext(request))

@login_required(login_url='/login/')
def topic(request):
    title='Topics'
    flash = ""
    if request.method=="POST":
        if Topic.objects.filter(URL=request.POST[u'url']):
                pass
        else:
            timestamp = datetime.now()
            t = Topic(URL=request.POST[u'url'],
                      poster=request.user,
                      dateCreated=timestamp)
            t.save()
            TopicRemark(topic=t,
                        remarks=request.POST[u'remarks'],
                        writer=request.user,
                        dateCreated=timestamp).save()
            TopicVote(topic=t,
                      vote=votedict[request.POST[u'vote']],
                      voter=request.user,
                      dateCreated=timestamp).save()

    return render_to_response("topic.html",
                              dict(title=title,
                                   navmenu=navmenu,
                                   flash=flash),
                              context_instance=RequestContext(request),
                              )

def register(request):
    title='Register'
    form = UserCreationForm(data=request.POST)
    tags = Tag.objects.all()

    if request.user.is_authenticated():
        return redirect("/", context_instance=RequestContext(request))

    if request.method=="POST":
        try:
            user = form.save(commit=True)
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/', context_instance=RequestContext(request))

        except Exception as exc:
            pass


    return render_to_response("register.html",
                              dict(title=title,
                                   navmenu=navmenu,
                                   form=form,
                                   tags=tags,
                                   qdict=request.POST if request.POST else ""),
                              context_instance=RequestContext(request))


def api(request):
    if request.POST:
        pass


def profile(request):
    pass