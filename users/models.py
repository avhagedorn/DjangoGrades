from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

'''
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=CASCADE)
	activity = models.JSONField(default=list)

	def __str__(self):
		return self.user.username
'''