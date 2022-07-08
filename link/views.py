from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from link.features import littlelink, checklink
from link.forms import UserAuthForm, UserRegForm, LinkForm
from link.models import Links


class RegForm(CreateView):
    template_name = 'register.html'
    form_class = UserRegForm

    def get_success_url(self):
        path = reverse('start', kwargs={'slug': self.request.user.username})
        return path

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse_lazy('start', kwargs={'slug': self.object.username}))


class AuthForm(LoginView):
    template_name = 'auth.html'
    form_class = UserAuthForm

    def get_success_url(self):
        path = reverse('start', kwargs={'slug': self.request.user.username})
        return path


class StartPage(ListView):
    template_name = 'base.html'
    model = User

def logou(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/')

class UserPage(LoginRequiredMixin, CreateView):
    login_url = "/auth/"
    template_name = "user.html"
    model = User
    form_class = LinkForm
    context_object_name = "objs"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.inlink and checklink(self.object.inlink , self.request.user.pk):
            print(littlelink(self.object.inlink))
            self.object.onlink = littlelink(self.object.inlink)
            self.object.user_id = self.request.user.pk
            self.object.save()
        return HttpResponseRedirect(reverse_lazy('start', kwargs={'slug': self.request.user.username}))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = User.objects.get(pk=self.request.user.pk).links.all().order_by('-id')
        return context


class DeleteLink(DeleteView):
    model = Links

    def get_success_url(self):
        return reverse_lazy('start', kwargs={'slug': self.request.user.username})

    def form_valid(self, form):
        success_url = self.get_success_url()
        if self.object.user_id == self.request.user.pk:
            self.object.delete()
        return HttpResponseRedirect(success_url)


def redirectPage(request, link):
    try:
        userlinks = request.user.links.get(onlink=link)
        return redirect(userlinks.inlink)
    except Links.DoesNotExist:
        return redirect(reverse_lazy('start', kwargs={'slug': request.user.username}))


