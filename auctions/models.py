from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	watchlists = models.ManyToManyField('Listing', blank=True, related_name="watchers")
   	
class Listing(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	image = models.CharField(max_length=100, blank=True)
	active = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
	category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="category")
	starting_bid = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
	current_price = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)

	def __str__(self):
		return f"{self.title} {self.description}"


class Bid(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
	bidders = models.ManyToManyField(User, blank=True, related_name="bidders")
	bids = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)

	def __str__(self):
		return f"{self.bids}"
	

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", default=None)
	content = models.CharField(max_length=500, default=None)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing", default=None)

	def __str__(self):
		return f"Commented by {self.author} \n {self.content}"
	

class Category(models.Model):
	categories = models.CharField(max_length=100, default="No category")

	def __str__(self):
		return f"{self.categories}"
