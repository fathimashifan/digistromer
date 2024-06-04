# forms.py
from django import forms
from .models import VedioGallery
# forms.py


class VedioGalleryForm(forms.ModelForm):
	class Meta:
		model = VedioGallery
		fields =('vedio_material',)
		widgets ={
            'vedio_material':forms.FileInput(attrs={'class': 'w-100', 'd': 6}),
        }
