from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer, TicketUpdateSerializer
from .pagination import TicketPagination

class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    pagination_class = TicketPagination

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

class TicketDetailView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketUpdateSerializer
    http_method_names = ["patch", "options"]

    def patch(self, request, *args, **kwargs):
        ticket = self.get_object()
        serializer = self.get_serializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TicketSerializer(ticket).data, status=status.HTTP_200_OK)    