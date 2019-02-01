from django import forms

from .models import Image, Comment


class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = [
			'title',
			'image',
		]
		widgets = {
			'title': forms.Textarea(attrs={"class":"form-control", "rows": 1, "cols": 20})

		}



class CommentForm(forms.ModelForm):
	text = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Add a comment...", "rows": "1", "cols": "20"}))
	class Meta:
		model = Comment
		fields = [
			'text'
		]
