from django.urls import path
from .views import (
    LoanApplicationCreateView,
    UserLoanListView,
    AdminLoanStatusUpdateView,
    AdminFlaggedLoanListView
)

urlpatterns = [
    path('apply/', LoanApplicationCreateView.as_view(), name='apply-loan'),
    path('my-loans/', UserLoanListView.as_view(), name='user-loans'),
    path('admin/update-loan/<int:pk>/', AdminLoanStatusUpdateView.as_view(), name='admin-update-loan'),
    path('admin/flagged-loans/', AdminFlaggedLoanListView.as_view(), name='flagged-loans'),
]