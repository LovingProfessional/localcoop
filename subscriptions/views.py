from django.http import HttpResponse
from django.shortcuts import redirect
from constance import config
from datetime import datetime
from subscriptions.forms import CoopUserForm, LoginForm
import subscriptions.models as m
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, is_authenticated

from django.template.response import SimpleTemplateResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def register_coopuser_view(request):
    #If it's past the deadline to enroll in the coop, redirect
    if config.ENROLLMENT_DEADLINE.ctime() < datetime.now().ctime():
        return redirect('/sorry',permanent=True)
    else:
        return render(request, 'registration.html', {'form':CoopUserForm})

def sorry_past_deadline_view(request):
    return HttpResponse("<p>Sorry, the deadline was " + str(config.ENROLLMENT_DEADLINE) + " :(</p>")

def process_registration(request):
    if request.method == 'POST':
        filledRegForm = CoopUserForm(request.POST)
        if filledRegForm.is_valid():
            #Save the information recieved into a 
            newCoopUser = m.CoopUser()#{{{
            newUser = User()
            data = filledRegForm.cleaned_data
            newUser.username = data['email'][:-13]
            newUser.set_password(data['password'])
            newUser.save()
            newCoopUser.user = newUser
            newCoopUser.firstname = data['firstname']
            newCoopUser.lastname = data['lastname']
            newCoopUser.email = data['email']
            newCoopUser.phone = data['phone']
            newCoopUser.wesid = data['wesid']
            newGroup = m.Group()
            newGroup.save()
            print(newGroup.id)
            newCoopUser.group = newGroup
            print(newCoopUser.group)
            newCoopUser.save()#}}}
            return HttpResponseRedirect('/thanks-for-registering/')
    else:
        filledRegForm = CoopUserForm()
    return render(request, 'registrationtemp.html',{'form':filledRegForm})

def thanks_for_registering(request):
    return HttpResponse("<p>Got it, thanks!</p>")

def login(request):
    if request.user.is_authenticated():
        return HttpRespones("You're already logged in!")
    else:
        return render(request, 'login.html',{'form':LoginForm})

def login_successful(request):
    if request.method == 'POST':
        filledLogin = LoginForm(request.POST)
        if filledLogin.is_valid():
            #Save the information recieved into a 
            data = filledLogin.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            print(user.is_authenticated())
            return HttpResponseRedirect('/user/' + str(data['username']) + '/') #Returns a path to the user's userpage localcoop.com/username/
    else:
        filledLogin = LoginForm()
    return render(request, 'login.html',{'form':filledLogin})
    

def user_page(request, username_string=None):
    if username_string == None:
        if request.user:
            username_string = request.user.username
        else:
            return HttpResponseRedirect('/login/')
    elif not (username_string == request.user.username and request.user.is_authenticated()):
        print("::" + str(request.user))
        from django.http import Http404            
        raise Http404
    user = User.objects.get(username=username_string)
    coopuser = user.coopuser
    sublist = []

    #Prepare the list of titles and choices we're going to need to make this forum
    for sub in coopuser.subscription_set.all():
        sublist.append(str(sub))
        #I'm going to add choices here

    return render(request, 'userpage.html',{'coopuser':coopuser, 'subscriptions':sublist})
