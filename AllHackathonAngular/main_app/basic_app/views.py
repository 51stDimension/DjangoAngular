from django.shortcuts import render,get_object_or_404
from basic_app.forms import UserForm,UserExtraForm
from django.views.generic import TemplateView,CreateView,ListView,DetailView,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from basic_app.models import UserModel
from pathlib import Path
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent


class Landingview(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super(Landingview, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            print(BASE_DIR)
            print(self.request.user.user_profile.profile_photo.url)
            finaldir = str(self.request.user.user_profile.profile_photo.url)
            print(finaldir)
            context['photo_dir'] = finaldir

        return context

def signup(request):

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_extra_form = UserExtraForm(data=request.POST)

        if user_form.is_valid() and user_extra_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            extra = user_extra_form.save(commit=False)
            extra.user = user

            if 'profile_photo' in request.FILES:
                print('here')
                extra.profile_photo = request.FILES['profile_photo']

            # if 'pdf' in request.FILES:
            #     extra.pdf = request.FILES['pdf']

            extra.save()

            registered = True

            return render(request,'login.html')

        else:
            print(user_form.errors,user_extra_form.errors)

    else:
        user_form = UserForm()
        user_extra_form = UserExtraForm()

    return render(request,'signup.html',{'user_form':user_form,'user_extra_form':user_extra_form,
    'registered':registered})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('basic_app:landing'))

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse_lazy('basic_app:landing'))
            else:
                return HttpResponseRedirect("ACCOUNT NOT ACTIVE")

        else:
            print("Someone Tried to login and failed")
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request,'login.html')
