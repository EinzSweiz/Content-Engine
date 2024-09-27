from .models import Item
from django import forms



class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title']
    
class ItemPatcheForm(forms.Form):
    title = forms.CharField(required=False)
    status = forms.CharField(required=False)
class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'status']

class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'status']
    