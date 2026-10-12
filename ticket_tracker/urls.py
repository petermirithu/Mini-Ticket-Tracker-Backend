from django.urls import path
from .views import TicketListCreateView, TicketDetailView, TicketStatsView

urlpatterns = [
    path("tickets", TicketListCreateView.as_view(), name="ticket-list-create"),    
    path("tickets/<int:pk>", TicketDetailView.as_view(), name="ticket-detail"),
    path("tickets/stats", TicketStatsView.as_view(), name="ticket-stats"),
]
