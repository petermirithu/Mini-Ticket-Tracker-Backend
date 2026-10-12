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

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("status", "priority")

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "Provide at least one of: status or priority."
            )
        return attrs