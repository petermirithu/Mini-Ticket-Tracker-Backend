from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "updated_at",
            "created_at",
        )
        read_only_fields = ("id", "updated_at", "created_at")