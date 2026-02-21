"""
Vercel serverless entry point for Django.
Exposes the WSGI callable as `app` for Vercel's Python runtime.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flightApp.settings")

app = get_wsgi_application()
