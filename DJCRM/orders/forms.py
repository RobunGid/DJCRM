from django import forms

from orders.models import Order, OrderComment, OrderFile, OrderItems

class OrderForm(forms.ModelForm):
    class Meta:
        fields = ("status",)
        model = Order
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter order name"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

OrderItemsFormSet = forms.inlineformset_factory(
    Order, OrderItems,
    fields=["product", "quantity"],
    can_delete=False,
    widgets={
        "product": forms.Select(attrs={"class": "form-select"}), 
        "quantity": forms.NumberInput(attrs={"class": "form-select"}), 
            },
    extra=2
)

class AddOrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter comment content", "style": "resize: none;"}),
        }
        
class AddOrderFileForm(forms.ModelForm):
    class Meta:
        model = OrderFile
        fields = ("file", )