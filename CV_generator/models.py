from django.db import models
import os
# Create your models here.
class CV(models.Model):
   
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    phone = models.PositiveIntegerField(max_length=14)
    address = models.CharField(max_length=200)
    about = models.TextField(max_length=200)
    education = models.TextField(max_length=100)
    experience = models.TextField(max_length=100)
    skills = models.CharField(max_length=100)
    interests = models.TextField(max_length=100)
    achievements = models.TextField(max_length=100)
    references = models.TextField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        # Delete the file from the file system when the object is deleted
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(CV, self).delete(*args, **kwargs)
    
    
    '''
    SKILL_CHOICES = (
    ('ms_word', 'Microsoft Word'),
    ('office', 'Microsoft Office Suite'),
    ('excel', 'Microsoft Excel'),
    ('google_workspace', 'Google Workspace'),
    ('graphics', 'Graphics Design'),
    ('accountant', 'Accounting'),
    ('cooking', 'Cooking'),
    ('gaming', 'Gaming'),
    ('pc_expert', 'PC Expertise'),
    ('python', 'Python'),
    ('Django', 'Django'),
)
'''