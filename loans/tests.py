# loans/tests.py
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
from .models import LoanApplication

class LoanSubmissionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass123")
        client = APIClient()
        resp = client.post("/auth/login/", {"username": "alice", "password": "pass123"}, format="json")
        self.token = resp.data["token"]
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_successful_loan_application(self):
        url = "/api/loans/apply/"
        data = {"amount_requested": "100000.00", "purpose": "Test purchase"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(float(response.data["amount_requested"]), 100000.00)


class FraudDetectionTests(APITestCase):
    def setUp(self):
        domain = "spam.com"
        for i in range(12):
            User.objects.create_user(username=f"user{i}", email=f"user{i}@{domain}", password="pass123")
        self.user = User.objects.get(username="user0")
        client = APIClient()
        resp = client.post("/auth/login/", {"username": self.user.username, "password": "pass123"}, format="json")
        self.token = resp.data["token"]
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_flag_high_amount_and_email_domain_and_rapid_submissions(self):
        url = "/api/loans/apply/"
        resp1 = self.client.post(url, {"amount_requested": "6000000.00", "purpose": "Big spend"}, format="json")
        self.assertEqual(resp1.data["status"], "flagged")

        loan1 = LoanApplication.objects.get(id=resp1.data["id"])
        reasons1 = {f.reason.code for f in loan1.fraud_flags.all()}
        self.assertIn("High amount requested", reasons1)

        for _ in range(3):
            self.client.post(url, {"amount_requested": "10000.00", "purpose": "Small spend"}, format="json")

        resp5 = self.client.post(url, {"amount_requested": "10000.00", "purpose": "Another spend"}, format="json")
        self.assertEqual(resp5.data["status"], "flagged")

        loan5 = LoanApplication.objects.get(id=resp5.data["id"])
        reasons5 = {f.reason.code for f in loan5.fraud_flags.all()}
        self.assertIn("Too many loans in 24 hours", reasons5)
        self.assertIn("Email domain used by many users", reasons5)