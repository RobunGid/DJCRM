from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from core.utils import DataMixin
from clients.models import Client
from clients.forms import AddClientForm
from teams.models import Team

# Create your views here.
class ClientListPage(DataMixin, LoginRequiredMixin, ListView):
    template_name = "clients/client_list.html"
    title = "Clients"
    context_object_name = "clients"
    
    def get_queryset(self):
        return Client.objects.all()
    
class ClientDetailsPage(DataMixin, LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/client_details.html"
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Client Details - ID #{self.object.pk}"
        return context

class ClientDeletePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("clients:client_list")
    success_message = "Client was deleted successfully"
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Delete Client - ID #{self.object.pk}"
        return context

    def post(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=kwargs["pk"])
        if client.has_lead():
            client.lead.converted_to_client = False
            client.lead.save()
        return super().post(request, *args, **kwargs)
    
class ClientAddPage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddClientForm
    model = Client
    template_name = "clients/client_add.html"
    title = None
    success_url = reverse_lazy("clients:client_list")
    extra_context = {"button_text": "Create"}
    success_message = "Client was created successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Add Client"
        return context
    
    def form_valid(self, form):
        client = form.save(commit=False)
        client.created_by = self.request.user
        client.team = Team.objects.filter(created_by=self.request.user).first()
        return super().form_valid(form)
    
class ClientUpdatePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, UpdateView):
    model = Client
    template_name = "clients/client_add.html"
    form_class = AddClientForm
    extra_context = {"button_text": "Update"}
    title = None
    success_message = "Client was updated successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Edit Client - ID #{self.object.pk}"
        return context