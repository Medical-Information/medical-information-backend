from django.urls import path

from about.views import DevelopersView

urlpatterns = [
    path('developers/', DevelopersView.as_view(), name='developers'),
]
