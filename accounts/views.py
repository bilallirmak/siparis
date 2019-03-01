from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
from .signals import user_logged_in
from django.contrib.auth import authenticate, login, logout
from django.utils.http import is_safe_url
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView


# @login_required
# def account_home_view(request):
#     return render(request, 'accounts/home.html')

# class LoginRequiredMixin(object):
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(self, request, *args, **kwargs)


class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('home')

    return render(request, "accounts/form.html", {"form": form, 'title': 'Giriş Yap'})

class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/form.html"
    success_url = '/browse'


    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.sessinon['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('browse')

        return super(LoginView, self).form_invalid(form)






class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/form1.html"
    success_url = '/browse'



    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        return redirect('browse')

def logout_view(request):
    logout(request)
    return redirect('browse')

    # def login_v(self):
    #     request = self.request
    #     form = RegisterForm(request.POST or None)
    #     username = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #
    #     return super(RegisterView, self)


    # def register(self):
    #     request = self.request
    #     form = RegisterForm(request.POST or None)
    #
    #     return render(request, "accounts/form.html", {"form": form,'title': 'Üye Ol'})


# User = get_user_model()
# def register_view(request):
#     form = RegisterForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         # user = form.save(commit=False)
#         # password = form.cleaned_data.get('password1')
#         # user.set_password(password)
#         # user.save()
#         # new_user = authenticate(first_name=user.first_name, password=password)
#         # login(request, new_user)
#
#     return render(request, "accounts/form.html", {"form": form, 'title': 'Üye Ol'})
#



# def login_view(request):
#     form = LoginForm(request.POST or None)
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.sessinon['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('home')
#     return render(request, "accounts/form.html", {"form": form,'title':'Giriş Yap'})


