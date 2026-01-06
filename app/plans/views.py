from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from core.utils import DataMixin
from plans.models import Plan

class PlanListPage(DataMixin, LoginRequiredMixin, ListView):
    template_name = "plans/plan_list.html"
    title = "Plans"
    model = Plan
    context_object_name = "plans"
    
class PlanDetailsPage(DataMixin, LoginRequiredMixin, DetailView):
    model = Plan
    template_name = "plans/plan_details.html"
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Plan Details - ID #{self.object.pk}"
        return context