from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length = 150)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length = 100)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False,verbose_name='Is publisehd ?')
    image = models.ImageField(upload_to = 'pics/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='Author')
    slug = models.SlugField()
    body = models.TextField(max_length = 900)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:200]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e, %Y')

    def get_absoulate_url(self):
        return reverse('core:details',kwargs ={
            'slug':self.slug
        })
    
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


#for newsletter
class NewsUsers(models.Model):
    email = models.EmailField()
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "NewsUser"
        verbose_name_plural = "NewsUsers"