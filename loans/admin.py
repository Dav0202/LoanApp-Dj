from django.contrib import admin
from .models import FraudFlag, FraudReason, LoanApplication

admin.site.register(FraudReason)
admin.site.register(FraudFlag)
admin.site.register(LoanApplication)