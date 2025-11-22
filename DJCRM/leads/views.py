from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, DetailView, TemplateView, UpdateView, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from core.utils import DataMixin
from leads.models import Lead, LeadComment
from leads.forms import AddLeadForm, AddLeadCommentForm
from clients.models import Client, ClientComment
from teams.models import Team

class LeadAddPage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddLeadForm
    model = Lead
    template_name = "leads/lead_add.html"
    title = "Add Lead"
    success_url = reverse_lazy("leads:lead_list")
    extra_context = {"button_text": "Create"}
    success_message = "Lead was created successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Add Lead"
        context["allow_to_add"] = self.request.user.teams.first().leads.all().count() < self.request.user.teams.first().plan.max_leads
        return context
    
    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        lead.team = Team.objects.filter(created_by=self.request.user).first()
        return super().form_valid(form)
    
class LeadListPage(DataMixin, LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    title = "Leads"
    context_object_name = "leads"
    
    def get_queryset(self):
        return Lead.not_clients.all()
    
class LeadDetailsPage(DataMixin, LoginRequiredMixin, DetailView):
    model = Lead
    template_name = "leads/lead_details.html"
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Lead Details - ID #{self.object.pk}"
        context["add_comment_form"] = AddLeadCommentForm
        return context
    
class LeadUpdatePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, UpdateView):
    model = Lead
    template_name = "leads/lead_add.html"
    form_class = AddLeadForm
    extra_context = {"button_text": "Update"}
    title = "Update Lead"
    success_message = "Lead was updated successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Edit Lead - ID #{self.object.pk}"
        context["allow_to_add"] = True
        return context
    
class LeadDeletePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy("leads:lead_list")
    success_message = "Lead was deleted successfully"
    title = "Delete Lead"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Delete Lead - ID #{self.object.pk}"
        return context
    
class LeadConvertToClientPage(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = "leads/lead_convert_to_client.html"
    success_message = "Lead was converted to client successfully"
    title = "Convert Lead to Client"
    
    def post(self, request, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=kwargs["pk"])
        team = Team.objects.filter(created_by=request.user).first()
        
        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=team
        )
        
        lead.converted_to_client = True
        lead.client = client
        comments = lead.comments.all()
        for comment in comments:
            ClientComment.objects.create(
				created_by=comment.created_by,
				content=comment.content,
				client=client,
				team=team
			)
            
        
        client.save()
        lead.save()  
        messages.success(request, self.success_message)
        return redirect("leads:lead_list")
    
class LeadCommentAddView(View):
    def post(self, request, *args, **kwargs):
        form = AddLeadCommentForm(request.POST)
        
        if form.is_valid():
            pk = kwargs.get("pk")
            
            team = Team.objects.filter(created_by=request.user).first()
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()
    
        return redirect("leads:lead_details", pk=pk)