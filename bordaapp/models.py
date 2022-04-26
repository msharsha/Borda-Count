from ssl import Options
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="admin")
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True,blank=True)
    allowed_users = models.TextField(default='')
    answered_users = models.TextField(default='_')
    options = models.TextField(blank=False)

    class Meta:
        ordering = ('-date_posted', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Submission(models.Model):
    options = models.TextField(blank=False)
    preferences = models.TextField(blank=True, default="")
    post_id = models.ForeignKey('bordaapp.Post', on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.options

    def preferenceMap(self):
        options = self.options.split(',');
        preferences = self.preferences.split(',');
        prefs = {}
        for idx, option in enumerate(options):
            prefs[option] = int(preferences[idx])
        return prefs
