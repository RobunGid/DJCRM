from PIL import Image
import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse

from core.utils import DataMixin
from products.models import Product, ProductComment, ProductFile
from products.forms import AddProductForm, AddProductCommentForm, AddProductFileForm

class ProductAddPage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddProductForm
    model = Product
    template_name = "products/product_add.html"
    title = "Add Product"
    success_url = reverse_lazy("products:product_list")
    extra_context = {"button_text": "Create"}
    success_message = "Product was created successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Add Product"
        context["allow_to_add"] = self.request.user.userprofile.active_team.products.all().count() < self.request.user.userprofile.active_team.plan.max_products
        return context
    
    def form_valid(self, form):
        product = form.save(commit=False)
        product.created_by = self.request.user
        product.team = self.request.user.userprofile.active_team
        return super().form_valid(form)
    
class ProductListPage(DataMixin, LoginRequiredMixin, ListView):
    template_name = "products/product_list.html"
    title = "Products"
    context_object_name = "products"
    
    def get_queryset(self):
        return Product.objects.filter(team=self.request.user.userprofile.active_team).all()
    
class ProductDetailsPage(DataMixin, LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_details.html"
    title = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Product Details - ID #{self.object.pk}"
        context["add_comment_form"] = AddProductCommentForm
        context["add_file_form"] = AddProductFileForm
        return context
    
class ProductUpdatePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "products/product_add.html"
    form_class = AddProductForm
    extra_context = {"button_text": "Update"}
    title = "Update Product"
    success_message = "Product was updated successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Edit Product - ID #{self.object.pk}"
        context["allow_to_add"] = True
        return context
    
class ProductDeletePage(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("products:product_list")
    success_message = "Product was deleted successfully"
    title = "Delete Product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = f"Delete Product - ID #{self.object.pk}"
        return context
    
class ProductCommentAddView(View):
    def post(self, request, *args, **kwargs):
        form = AddProductCommentForm(request.POST)
        pk = kwargs.get("pk")
        
        if form.is_valid():
            team = request.user.userprofile.active_team
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.product_id = pk
            comment.save()
    
        return redirect("products:product_details", pk=pk)
    
class ProductFileAddView(View):
    def post(self, request, *args, **kwargs):
        form = AddProductFileForm(request.POST, request.FILES)
        pk = kwargs.get("pk")
        
        if form.is_valid():
            team = request.user.userprofile.active_team
            product_file = form.save(commit=False)
            product_file.team = team
            product_file.created_by = request.user
            product_file.product_id = pk
            try:
                with Image.open(product_file.file) as img:
                    img.verify()
            except (IOError, SyntaxError):
                product_file.is_image = False
            else:
                product_file.is_image = True
            product_file.save()

        return redirect("products:product_details", pk=pk)
   
class ProductCommentDeleteView(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = ProductComment
    success_message = "Product comment was deleted successfully"
    
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("products:product_details", kwargs={"pk": self.object.product.pk})
    
class ProductFileDeleteView(SuccessMessageMixin, DataMixin, LoginRequiredMixin, DeleteView):
    model = ProductFile
    success_message = "Product file was deleted successfully"
    
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("products:product_details", kwargs={"pk": self.object.product.pk})
    
class ProductExportCSVView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(created_by=request.user)
        
        response = HttpResponse(
			content_type="text/csv",
			headers={"Content-Disposition": 'attachment; filename="products.csv"'}
		)
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Product', 'Description', 'Created at', 'Created by'])
        
        for product in products:
            writer.writerow([product.pk, product.name, product.description, product.created_at, product.created_by])
            
        return response