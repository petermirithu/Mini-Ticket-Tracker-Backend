from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ticket

class TicketApiTests(APITestCase):
    def test_create_ticket(self):
        response = self.client.post(
            reverse("ticket-list-create"),
            {
                "title": "Printer is offline",
                "description": "The reception printer cannot connect.",
                "priority": "high",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], Ticket.Status.OPEN)
        self.assertEqual(response.data["priority"], Ticket.Priority.HIGH)
        self.assertIsNotNone(response.data["updated_at"])
        self.assertIsNotNone(response.data["created_at"])
        self.assertEqual(Ticket.objects.count(), 1)

    def test_list_tickets_filters_by_status_and_paginates(self):
        Ticket.objects.bulk_create(
            [
                Ticket(title="Open one", status=Ticket.Status.OPEN),
                Ticket(title="Open two", status=Ticket.Status.OPEN),
                Ticket(title="Closed one", status=Ticket.Status.CLOSED),
            ]
        )

        response = self.client.get(
            reverse("ticket-list-create"),
            {"status": "open", "page": 1, "limit": 1},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["status"], "open")

    def test_list_tickets_rejects_invalid_status(self):
        response = self.client.get(
            reverse("ticket-list-create"), {"status": "unknown"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)

    def test_patch_ticket_status_and_priority(self):
        ticket = Ticket.objects.create(title="Cannot sign in")

        response = self.client.patch(
            reverse("ticket-detail", args=[ticket.id]),
            {"status": "in_progress", "priority": "high"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "in_progress")
        self.assertEqual(response.data["priority"], "high")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Ticket.Status.IN_PROGRESS)

    def test_patch_ticket_requires_an_allowed_field(self):
        ticket = Ticket.objects.create(title="Cannot sign in")

        response = self.client.patch(
            reverse("ticket-detail", args=[ticket.id]), {}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stats_returns_counts_for_every_status(self):
        Ticket.objects.create(title="First", status=Ticket.Status.OPEN)
        Ticket.objects.create(title="Second", status=Ticket.Status.OPEN)
        Ticket.objects.create(title="Third", status=Ticket.Status.CLOSED)

        response = self.client.get(reverse("ticket-stats"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"open": 2, "in_progress": 0, "closed": 1},
        )