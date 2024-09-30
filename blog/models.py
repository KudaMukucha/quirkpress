from django.db import models
from django.utils  import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name 

class Post(models.Model):
    STATUS_CHOICES = [
        ('DF','Drafted'),
        ('PB','Published')
    ]
    FEATURED_CHOICES =[
        ('Yes','Yes'),
        ('No','No')
    ]
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    body = models.TextField(blank=True,null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=STATUS_CHOICES,default='DF')
    featured = models.CharField(max_length=10,choices=FEATURED_CHOICES, default='No')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_posts')
    tags = TaggableManager()
    image = models.ImageField(upload_to='blog_images',blank=True,null=True)
    

    class Meta:
        ordering =['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes =[
            models.Index(fields=['created'])
        ]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
