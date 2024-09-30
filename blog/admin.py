from django.contrib import admin
from .models import Post,Category,Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','category','publish','status']
    list_filter=['status','category','created','publish']
    search_fields =['title','body']
    prepopulated_fields ={'slug':('title',)}
    date_hierarchy = 'publish'
    ordering =['status','publish']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields =['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display =['name','email','post','created','active']
    list_filter =['active','created','updated']
    search_fields = ['name','email','body']

