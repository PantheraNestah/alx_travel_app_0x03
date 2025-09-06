# alx_travel_app/__init__.py

from .Celery import app as celery_app

__all__ = ('celery_app',)