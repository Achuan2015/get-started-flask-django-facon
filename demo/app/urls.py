#!/usr/bin/env python

from django.urls import path
from . import views

urlpatterns = [
        path('tokenizer/',views.tokenizer)
        ]
