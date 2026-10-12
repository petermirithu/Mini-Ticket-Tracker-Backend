from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Ticket
from .serializers import TicketSerializer

class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer    

    def get_queryset(self):
        queryset = Ticket.objects.all()
        ticket_status = self.request.query_params.get("status")
        if ticket_status:
            valid_statuses = {choice.value for choice in Ticket.Status}
            if ticket_status not in valid_statuses:
                raise ValidationError(
                    {"status": f"Must be one of: {', '.join(sorted(valid_statuses))}."}
                )
            queryset = queryset.filter(status=ticket_status)
        return queryset