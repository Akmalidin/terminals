from django.contrib import admin
from .models import Region, Terminal, Incassation

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}
admin.site.register(Region, RegionAdmin)

class TerminalAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'address', 'rent')
    list_filter = ('region', 'rent')
    search_fields = ('name', 'region__name', 'address')
admin.site.register(Terminal, TerminalAdmin)

class IncassationAdmin(admin.ModelAdmin):
    list_display = ('terminal', 'last_collected', 'next_collection', 'interval_days')
    list_filter = ('terminal', 'last_collected', 'interval_days')
    search_fields = ('terminal__name', 'terminal__region__name', 'terminal__address')
admin.site.register(Incassation, IncassationAdmin)