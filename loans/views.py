from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import LoanApplication, FraudFlag, FraudReason
from .serializers import LoanApplicationSerializer
from datetime import timedelta

class LoanApplicationCreateView(generics.CreateAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        now = timezone.now()
        recent_loans = LoanApplication.objects.filter(user=user, date_applied__gte=now - timedelta(hours=24))
        email_domain = user.email.split('@')[-1]
        domain_user_count = User.objects.filter(email__iendswith=email_domain).distinct().count()

        fraud_reasons = []

        if recent_loans.count() >= 3:
            fraud_reasons.append('Too many loans in 24 hours')

        if serializer.validated_data['amount_requested'] > 5000000:
            fraud_reasons.append('High amount requested')

        if domain_user_count > 10:
            fraud_reasons.append('Email domain used by many users')

        loan = serializer.save(user=user)
        if fraud_reasons:
            loan.status = 'flagged'
            loan.save()

            for reason in fraud_reasons:
                fraud_obj, _ = FraudReason.objects.get_or_create(code=reason, defaults={'description': reason})
                FraudFlag.objects.create(loan_application=loan, reason=fraud_obj)

            send_mail(
                subject="Loan Application Flagged",
                message=f"User {user.email} Loan #{loan.id} was flagged for: {', '.join(fraud_reasons)}",
                from_email="noreply@loansystem.com",
                recipient_list=["admin@loansystem.com"],
                fail_silently=False
            )


class UserLoanListView(generics.ListAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoanApplication.objects.filter(user=self.request.user)

class AdminFlaggedLoanListView(generics.ListAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = LoanApplication.objects.filter(status='flagged')    

class AdminLoanStatusUpdateView(generics.UpdateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['patch']    

    def patch(self, request, *args, **kwargs):
        loan = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ['approved', 'rejected', 'flagged']:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        loan.status = new_status
        loan.save()
        return Response(self.get_serializer(loan).data)
