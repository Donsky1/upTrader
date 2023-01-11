from django.contrib import admin

from .models import TreeMenu, GlobalMenu


class TreeMenuAdminInline(admin.TabularInline):
    model = TreeMenu
    extra = 0


@admin.register(GlobalMenu)
class GlobalMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    inlines = [TreeMenuAdminInline, ]


@admin.register(TreeMenu)
class TreeMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'global_parent')
    list_display_links = ('id', 'name')