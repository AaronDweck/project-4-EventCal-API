from django.urls import path
from .views import EventsListView, EventsDetailView

urlpatterns = [
    path('', EventsListView.as_view()),
    path('<int:event_id>/', EventsDetailView.as_view())
]