from typing import Optional, Dict, Any
from django import forms
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, HttpResponseRedirect

menu = [
        {'title' : "Home", 'view_name': 'index'},
        {'title': 'Sign up', 'view_name': 'register'},
        {'title': 'Login', 'view_name': 'login'},
        {'title': 'Profile', 'view_name': None},
        {'title': 'Add task', 'view_name': None},
        {'title': 'All tasks', 'view_name': None},
    ]

for_reg = ['register', 'login']

# Mixins
class RedirectToIndexMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')

class DataMixin:
    default_context = {
        'menu': menu,
        'for_reg': for_reg,
    }

    def get_context_data(self, **kwargs):
        context = self.default_context.copy()
        context.update(kwargs)
        return context
