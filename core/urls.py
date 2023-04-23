"""
URL mappings for the core API.
"""
from django.urls import path

from core.views import FindingListView


urlpatterns = [
    path('findings/', FindingListView.as_view(), name='finding-list'),
]
