from django.contrib import admin
from .models import Project, ProjectsFollowing

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectsFollowing)
