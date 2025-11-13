from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Poll(models.Model):
question = models.CharField(max_length=255)
created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
pub_date = models.DateTimeField(auto_now_add=True)

def __str__(self):
return self.question

class Choice(models.Model):
poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
text = models.CharField(max_length=200)

def vote_count(self):
return self.votes.count()

def __str__(self):
return self.text

class Vote(models.Model):
poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
user = models.ForeignKey(User, on_delete=models.CASCADE)
voted_at = models.DateTimeField(auto_now_add=True)

class Meta:
unique_together = ('poll', 'user')

def __str__(self):
return f"{self.user} -> {self.choice}"