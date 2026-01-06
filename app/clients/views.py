from PIL import Image
import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from core.utils import DataMixin
from clients.models import Client, ClientFile, ClientComment
from clients.forms import AddClientForm, AddClientCommentForm, AddClientFileForm

class ClientListPage(DataMixin, LoginRequiredMixin, ListView):
    template_name = "clients/client_list.html"
    title = "Clients"
    context_object_name = "clients"
    
    def get_queryset(self):
        return Client.objects.all()
    
class ClientDetailsPage(DataMixin, LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/client_details.html"
    title = "Client Details"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Client Details - ID #{self.object.pk}"
        context["add_comment_form"] = AddClientCommentForm
        context["add_file_form"] = AddClientFileForm
        return context

class ClientDeletePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("clients:client_list")
    success_message = "Client was deleted successfully"
    title = "Delete Client"
    
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
    title = "Add Client"
    success_url = reverse_lazy("clients:client_list")
    extra_context = {"button_text": "Create"}
    success_message = "Client was created successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Add Client"
        context["allow_to_add"] = self.request.user.teams.first().clients.all().count() < self.request.user.teams.first().plan.max_clients
        return context
    
    def form_valid(self, form):
        client = form.save(commit=False)
        client.created_by = self.request.user
        client.team = self.request.user.userprofile.active_team
        return super().form_valid(form)
    
class ClientUpdatePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, UpdateView):
    model = Client
    template_name = "clients/client_add.html"
    form_class = AddClientForm
    extra_context = {"button_text": "Update"}
    title = "Update Client"
    success_message = "Client was updated successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Edit Client - ID #{self.object.pk}"
        context["allow_to_add"] = True
        return context
    
class ClientCommentAddView(View):
    def post(self, request, *args, **kwargs):
        form = AddClientCommentForm(request.POST)
        
        if form.is_valid():
            pk = kwargs.get("pk")
            
            team = request.user.userprofile.active_team
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client_id = pk
            comment.save()
    
        return redirect("clients:client_details", pk=pk)
    
class ClientFileAddView(View):
    def post(self, request, *args, **kwargs):
        form = AddClientFileForm(request.POST, request.FILES)
        pk = kwargs.get("pk")
        
        if form.is_valid():
            team = request.user.userprofile.active_team
            client_file = form.save(commit=False)
            client_file.team = team
            client_file.created_by = request.user
            client_file.client_id = pk
            try:
                with Image.open(client_file.file) as img:
                    img.verify()
            except (IOError, SyntaxError):
                client_file.is_image = False
            else:
                client_file.is_image = True
            client_file.save()

        return redirect("clients:client_details", pk=pk)
    
class ClientCommentDeleteView(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = ClientComment
    success_message = "Client comment was deleted successfully"
    
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("clients:client_details", kwargs={"pk": self.object.client.pk})
    
class ClientFileDeleteView(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = ClientFile
    success_message = "Client file was deleted successfully"
    
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("clients:client_details", kwargs={"pk": self.object.client.pk})
    
class ClientExportCSVView(View):
    def get(self, request, *args, **kwargs):
        clients = Client.objects.filter(created_by=request.user)
        
        response = HttpResponse(
			content_type="text/csv",
			headers={"Content-Disposition": 'attachment; filename="clients.csv"'}
		)
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Client', 'Description', 'Created at', 'Created by'])
        
        for client in clients:
            writer.writerow([client.pk, client.name, client.description, client.created_at, client.created_by])
            
        return response