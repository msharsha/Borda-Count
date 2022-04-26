from django.contrib import admin
from .models import Post, Submission


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_posted', 'deadline')
    readonly_fields = ['answered_users']
    list_display_links = ('id', 'title')
    list_filter = ('author', 'date_posted')
    search_fields = ('title', 'content', 'author')
    list_per_page = 20

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'options', 'preferences', 'submitted_by','submitted_date')
    list_filter = ['submitted_by', 'post_id', 'submitted_date']
    search_fields = ['submitted_by']
    list_per_page = 20

admin.site.register(Post, PostAdmin)
admin.site.register(Submission, SubmissionAdmin)