from django import forms

from .models import Item, SwapRequest


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "category",
            "condition",
            "exchange_type",
            "location",
            "image",
        ]


class SwapRequestForm(forms.ModelForm):
    class Meta:
        model = SwapRequest
        fields = ["message"]

