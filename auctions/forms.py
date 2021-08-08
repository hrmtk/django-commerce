from django import forms
from .models import User, Listing, Bid, Comment, Category

from decimal import Decimal

class NewListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = ["title", "description", "image", "category", "starting_bid",]
		labels = {"title": "Title", "description": "Description", "image" : "Image URL", "category": "Category", "starting_bid": "Starting bid",}
		widgets = {
			"title": forms.TextInput(
				attrs={"class": "form-control"}),
			"description": forms.TextInput(
				attrs={"class": "form-control"}),
			"image": forms.URLInput(
				attrs={"class": "form-control"}),
			"category": forms.Select(
				attrs={"class": "form-control"}),
			"starting_bid": forms.NumberInput(
				attrs={"class": "form-control", "step": ".01"}),
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ["content",]
		labels = {"content": "Comment",}
		widgets = {
			"content": forms.TextInput(
				attrs={
					"class": "form-control"
				}
			),
		}