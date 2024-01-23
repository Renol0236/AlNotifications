from typing import Optional, Dict, Any

from django import forms
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.utils import timezone

import requests

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView

from .forms import UserCreateForm, LoginForm, ProfileUpdateForm
from .models import UserProfile, DiscordProfile, Notifications
from .utils import DataMixin, menu, RedirectToIndexMixin
from .serializers import NotificationsSerializer

# Index View (Main Page)


class IndexView(DataMixin, TemplateView): # Главная страница
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        addc = {
            'title' : 'Главная',
            'style': 'index',
        }

        context = super().get_context_data(**addc)

        return context


# Register View


class RegisterView(DataMixin, RedirectToIndexMixin, View):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    redirect_authenticated_user = True

    def get(self, request):
        form = UserCreateForm()
        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            profile = UserProfile.objects.create(user=user, bio=form.cleaned_data['bio'], profile_picture=form.cleaned_data['profile_picture'])
            profile.save()

            login(request, user)
            return redirect(self.success_url)

        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def get_context_data(self, form, **kwargs):
        addc = {
            'title': 'Sign up',
            'style': 'login',
            'form': form,
        }
        context = super().get_context_data(**addc)
        return context

# Login View


class LoginView(LoginView):

    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')
    form = LoginForm()

    def form_valid(self, form):
        messages.success(self.request, 'Login success')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Login error, invalid password or login')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        addc = {
            'title': 'Log in',
            'style': 'login',
            'form': self.form,
        }
        context = super().get_context_data(**addc)
        return context



# Profile View


class ProfileView(DataMixin, View):
    template_name = 'profile.html'

    def get(self, request, id):
        current_user = get_object_or_404(UserProfile, id=id)
        users_notifications = Notifications.objects.filter(user=id)
        context = self.get_context_data(current_user, user_notifications=users_notifications)
        return render(request, self.template_name, context)

    def get_context_data(self, current_user, user_notifications, **kwargs):
        addc = {
            'title': 'Profile',
            'style': 'profile',
            'UserProfile': current_user,
            'notifications': user_notifications
        }

        context = super().get_context_data(**addc)
        return context

# Profile Update View


class ProfileUpdateView(DataMixin, LoginRequiredMixin, View):
    template_name = 'profile_update.html'

    def get(self, request):
        form = ProfileUpdateForm(instance=request.user.userprofile)
        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile', id=request.user.id)
        else:
            print(form.errors)
            print('1')
        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def get_context_data(self, form, **kwargs):
        addc = {
            'title': 'Profile',
            'style': 'profile',
            'form': form,
        }

        context = super().get_context_data(**addc)
        return context

# Discord o2auth


auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1197441739959566356&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Fdiscord%2Fredirect&scope=identify"

def discord_login(request):
    return redirect(auth_url_discord)

def discord_login_redirect(request):
    code = request.GET.get('code')
    user_data = exchange_discord(code)

    if user_data:
        discord_profile, created = DiscordProfile.objects.update_or_create(
            id=user_data['id'],
            defaults={
                'discord_tag': f"{user_data['username']}#{user_data['discriminator']}",
                'avatar': user_data['avatar'],
                'public_flags': user_data['public_flags'],
                'flags': user_data['flags'],
                'locale': user_data['locale'],
                'mfa_enabled': user_data['mfa_enabled'],
                'last_login': timezone.now(),
                'global_name': user_data['global_name']
            }
        )

        request.user.userprofile.discord_profile = discord_profile
        request.user.userprofile.save()

        return JsonResponse({'user': user_data})
    else:
        return JsonResponse({'error': 'Failed to fetch user data'})

# Константы для конфиденциальных данных


def exchange_discord(code):
    # Подготовка данных для запроса токена
    data = {
        "client_id": '1197441739959566356',
        "client_secret": '8YDjA3IL5xP5eM2gyV2sAFhggAQPflLU',
        "grant_type": 'authorization_code',
        "code": code,
        'redirect_uri': 'http://localhost:8000/oauth2/discord/redirect',
        'scope': 'identify email guilds',
    }

    # Заголовки для запросов
    headers = {
        'Content-type': 'application/x-www-form-urlencoded'
    }

    # Выполнение запроса токена
    with requests.Session() as session:
        response = session.post('https://discord.com/api/oauth2/token', data=data, headers=headers)

        if response.status_code == 200:
            credentials = response.json()
            access_token = credentials['access_token']

            response = session.get('https://discord.com/api/v6/users/@me', headers={'Authorization': f'Bearer {access_token}'})

            if response.status_code == 200:
                user = response.json()
                print(user)
                return user
            else:
                print(f"Ошибка при получении информации о пользователе: {response.status_code}")
        else:
            print(f"Ошибка при обмене кода на токен: {response.status_code}")

    return None

# Notifications API

# View for creating notification


@permission_classes([IsAuthenticated])
class NotificationsCreateView(CreateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    template_name = 'create_notifi.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return redirect('profile', id = request.user.id)

# View for deleting notification


class NotificationsDeleteView(DestroyAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'id'

# Another View (utils)


def LogoutView(request): # View For User Logout
    logout(request)
    return redirect('index')

# Custom Handlers


def customhandler404(request, exception):
    return render(request, '404.html', status=404)

