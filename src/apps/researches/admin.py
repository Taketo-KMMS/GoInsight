from django.contrib import admin

from .models import Project, ProjectCustomerAttr, Research


class ResearchInline(admin.TabularInline):
    model = Research
    extra = 2


class ProjectCustomerAttrInline(admin.TabularInline):
    model = ProjectCustomerAttr
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    inlines = [ResearchInline, ProjectCustomerAttrInline]
    list_display = ("id", "name", "store_category")
