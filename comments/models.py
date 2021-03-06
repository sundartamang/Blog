from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
#for comment
class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager,self).filter(parent=None)
        return qs
    def filter_by_instance(self,instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type,object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    timestamp      = models.DateTimeField(auto_now_add=True)
    content        = models.TextField()

    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    parent         = models.ForeignKey("self", blank=True,null=True,on_delete=models.CASCADE)

    objects        = CommentManager()

    # class Meta:
    #     ordering = ['-timestamp']
    
    def get_absoulate_url(self):
        return reverse('core:details',kwargs ={
            'slug':self.slug
        })

    def __str__(self):
        return self.user.username

    def children(self): #replies
        return Comment.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True