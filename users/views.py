import secrets
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from users.forms import UserRegisterForm, UserProfileUpdateForm
from django.conf import settings
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        self.send_welcome_email(user.email, user.token)
        return super().form_valid(form)

    def send_welcome_email(self, user_email, user_token):
        host = self.request.get_host()
        url = f"http://{host}/email-confirm/{user_token}/"
        subject = 'Добро пожаловать в наш сервис'
        message = f"Спасибо, что зарегистрировались в нашем сервисе! Для подтверждения почты пройдите по ссылке: {url}"
        recipient_list = [user_email]
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class RegisterUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_profile_update.html'
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy('catalog:home')
