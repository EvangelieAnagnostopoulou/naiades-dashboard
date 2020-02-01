from django.contrib.auth import logout as logout_fn
from django.shortcuts import render, redirect
from django.urls import reverse


def logout(request):
    # clear session
    logout_fn(request)

    return redirect(reverse('login'))
