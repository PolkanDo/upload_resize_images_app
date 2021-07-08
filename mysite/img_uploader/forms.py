from django import forms

from .models import Image


class ResizeImageForm(forms.ModelForm):
    """Resize image form"""
    class Meta:
        model = Image
        fields = ('width', 'height')
        labels = {
                'width': 'Width',
                'height': 'Height',
            }


class NewImageForm(forms.Form):
    """New image's form"""
    Link = forms.CharField(
        label='Link',
        required=False,
        help_text='Insert a link to the image'
    )
    Image = forms.ImageField(
        label='Image',
        required=False,
        help_text='Select an image'
    )
