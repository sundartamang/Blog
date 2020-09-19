from django.contrib import admin
from .models import Post,Category,NewsUsers

#Register your models here.
admin.site.register(Post)
admin.site.register(Category)
class NewsletterAdmin(admin.ModelAdmin):
    list_display =('email','date_added',)
admin.site.register(NewsUsers, NewsletterAdmin)


    