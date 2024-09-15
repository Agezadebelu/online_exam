from django.db import models
from django.conf import settings  # Import for linking to the User model

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the teacher who created it

    def __str__(self):
        return self.title