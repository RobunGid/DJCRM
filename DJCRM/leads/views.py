from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from leads.models import Lead
from leads.forms import AddLeadForm
from leads.utils import DataMixin

# Create your views here.
class AddLeadPage(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddLeadForm
    model = Lead
    template_name = "leads/add_lead.html"
    title = "Add lead"
    success_url = reverse_lazy("dashboard")
    
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        return super().form_valid(form)
    
class LeadListPage(DataMixin, LoginRequiredMixin, ListView):
    template_name = "leads/leads_list.html"
    title = "Leads"
    context_object_name = "leads"
    paginate_by = 10
    
    def get_queryset(self):
        return Lead.objects.all()