from PIL import Image
import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.db.models import Sum, F

from core.utils import DataMixin
from orders.models import Order, OrderComment, OrderFile
from orders.forms import AddOrderCommentForm, AddOrderFileForm, OrderForm, OrderItemsCreateFormSet, OrderItemsUpdateFormSet

class OrderCreatePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, CreateView):
    form_class = OrderForm
    model = Order
    template_name = "orders/order_create.html"
    title = "Create Order"
    success_url = reverse_lazy("orders:order_list")
    extra_context = {"button_text": "Create"}
    success_message = "Order was created successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Create Order"
        context["allow_to_add"] = self.request.user.userprofile.active_team.orders.all().count() < self.request.user.userprofile.active_team.plan.max_orders
        if self.request.POST:
            context['order_items_formset'] = OrderItemsCreateFormSet(self.request.POST)
        else:
            context['order_items_formset'] = OrderItemsCreateFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        order_items_formset = context['order_items_formset']
        if order_items_formset.is_valid():
            order = form.save(commit=False)
            order.created_by = self.request.user
            order.team = self.request.user.userprofile.active_team
            order.save()
            for form in order_items_formset:
                form.instance.order_id = order.pk
                form.instance.save()
            return redirect(order.get_absolute_url())
        return self.form_invalid(form)
        
class OrderListPage(DataMixin, LoginRequiredMixin, ListView):
    template_name = "orders/order_list.html"
    title = "Orders"
    context_object_name = "orders"
    
    def get_queryset(self):
        return Order.objects.filter(team=self.request.user.userprofile.active_team).annotate(
            total_price=Sum(F('orderitems__quantity') * F('orderitems__product__price'))
        ).all()
    
class OrderDetailsPage(DataMixin, LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_details.html"
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Order Details - ID #{self.object.pk}"
        context["add_comment_form"] = AddOrderCommentForm
        context["add_file_form"] = AddOrderFileForm
        return context
    
    def get_queryset(self):
        return super().get_queryset().annotate(
            total_price=Sum(F('orderitems__quantity') * F('orderitems__product__price'))
        )
    
class OrderUpdatePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, UpdateView):
    model = Order
    template_name = "orders/order_create.html"
    form_class = OrderForm
    extra_context = {"button_text": "Update"}
    title = "Update Order"
    success_message = "Order was updated successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Edit Order - ID #{self.object.pk}"
        context["allow_to_add"] = True
        if self.request.POST:
            context['order_items_formset'] = OrderItemsUpdateFormSet(self.request.POST, instance=self.object)
        else:
            context['order_items_formset'] = OrderItemsUpdateFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data()
        order_items_formset = context['order_items_formset']
        if order_items_formset.is_valid():
            print(order_items_formset)
            order_items_formset.instance = self.object
            for form in order_items_formset:
                form.instance.order_id = self.object.pk
                form.instance.save()
            return redirect("orders:order_details", pk=self.object.pk)
        return self.form_invalid(form)
        
class OrderDeletePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy("orders:order_list")
    success_message = "Order was deleted successfully"
    title = "Delete Order"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Delete Order - ID #{self.object.pk}"
        return context
    
class OrderCommentDeleteView(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = OrderComment
    success_message = "Order comment was deleted successfully"
    
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("orders:order_details", kwargs={"pk": self.object.order.pk})
    
class OrderFileDeleteView(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = OrderFile
    success_message = "Order file was deleted successfully"
    
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("orders:order_details", kwargs={"pk": self.object.order.pk})
    
class OrderCommentAddView(View):
    def post(self, request, *args, **kwargs):
        form = AddOrderCommentForm(request.POST)
        pk = kwargs.get("pk")
        
        if form.is_valid():
            team = request.user.userprofile.active_team
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.order_id = pk
            comment.save()
    
        return redirect("orders:order_details", pk=pk)
    
class OrderFileAddView(View):
    def post(self, request, *args, **kwargs):
        form = AddOrderFileForm(request.POST, request.FILES)
        pk = kwargs.get("pk")
        
        if form.is_valid():
            team = request.user.userprofile.active_team
            order_file = form.save(commit=False)
            order_file.team = team
            order_file.created_by = request.user
            order_file.order_id = pk
            try:
                with Image.open(order_file.file) as img:
                    img.verify()
            except (IOError, SyntaxError):
                order_file.is_image = False
            else:
                order_file.is_image = True
            order_file.save()

        return redirect("orders:order_details", pk=pk)
    
class OrderExportCSVView(View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(created_by=request.user)
        
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="orders.csv"'}
        )
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Order', 'Description', 'Created at', 'Created by'])
        
        for order in orders:
            writer.writerow([order.pk, order.name, order.description, order.created_at, order.created_by])
            
        return response