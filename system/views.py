from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User
from system.models import Farmer, FarmerInspection


def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Statistics for small boxes
        total_farmers = Farmer.objects.count()
        active_farmers = Farmer.objects.filter(is_active=True).count()
        total_inspections = FarmerInspection.objects.count()
        inspected_farmers = FarmerInspection.objects.values('farmer').distinct().count()

        context['stats'] = {
            'total_farmers': total_farmers,
            'active_farmers': active_farmers,
            'total_inspections': total_inspections,
            'inspected_farmers': inspected_farmers
        }

        return context