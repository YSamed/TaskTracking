from django.contrib import admin
from .models import Task, Category , Project

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'category')
    list_filter = ( 'due_date', 'category')
    search_fields = ['title', 'description', 'category']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('title',)  # Bu örnekte sadece 'title' alanı için filtre ekledim, gerekirse diğer alanları da ekleyebilirsiniz
    search_fields = ['title', 'description']