from .models import Item
from django import forms



class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title']
    

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description']
    