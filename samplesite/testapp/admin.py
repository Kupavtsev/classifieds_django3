from dataclasses import fields
from django.contrib import admin
from .models import *

class MesureAdmin(admin.ModelAdmin):
    list_display = ('mesurment',)

class TestIDAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SpareAdmin(admin.ModelAdmin):
    list_display = ('name',)

class MachineAdmin(admin.ModelAdmin):
    fields = ['name', 'spares']
    list_display = ('name', 'get_spares')

    def get_spares(self, obj):
        return "\n".join([s.name for s in obj.spares.all()])

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('is_activated', 'user')


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Mesure, MesureAdmin)

admin.site.register(TestID, TestIDAdmin)

admin.site.register(Spare, SpareAdmin)
admin.site.register(Machine, MachineAdmin)
