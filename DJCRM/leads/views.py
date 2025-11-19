from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from leads.models import Lead
from leads.forms import AddLeadForm
from leads.utils import DataMixin

# Create your views here.
class AddLeadPage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddLeadForm
    model = Lead
    template_name = "leads/add_lead.html"
    title = None
    success_url = reverse_lazy("leads:lead_list")
    extra_context = {"button_text": "Create"}
    success_message = "Lead was created successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Create Lead"
        
        return context
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        return super().form_valid(form)
    
class LeadListPage(DataMixin, LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    title = "Leads"
    context_object_name = "leads"
    paginate_by = 10
    
    def get_queryset(self):
        return Lead.objects.all()
    
class LeadDetailsPage(DataMixin, LoginRequiredMixin, DetailView):
    model = Lead
    template_name = "leads/lead_details.html"
    title = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Lead Details - ID #{self.object.pk}"
        return context
    
class LeadUpdatePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, UpdateView):
    model = Lead
    template_name = "leads/add_lead.html"
    form_class = AddLeadForm
    extra_context = {"button_text": "Update"}
    title = None
    success_message = "Lead was updated successfully"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Edit Lead - ID #{self.object.pk}"
        return context
    
class LeadDeletePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy("leads:lead_list")
    success_message = "Lead was deleted successfully"
    title = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Delete Lead - ID #{self.object.pk}"
        return context