from django import forms

from products.models import Product, ProductComment, ProductFile

class AddProductForm(forms.ModelForm):
    class Meta:
        fields = ("name", "description", "status", "weight", "price", "stock_quantity")
        model = Product
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter product name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter product description"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter product price in $"}),
            "weight": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter product weight in gramms"}),
            "stock_quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter product weight in gramms"}),
            "status": forms.Select(attrs={"class": "form-select"}),
		}
        
class AddProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter comment content", "style": "resize: none;"}),
		}
        
class AddProductFileForm(forms.ModelForm):
    class Meta:
        model = ProductFile
        fields = ("file", )