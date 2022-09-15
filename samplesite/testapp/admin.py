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
    fields = ['name']
    list_display = ('name', 'get_spares')

    def get_spares(self, obj):
        return "\n".join([s.name for s in obj.spares.all()])

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('is_activated', 'user')


# class KitAdmin(admin.ModelAdmin):
#     list_display = ('machine', 'spare', 'count')

class NoteAdmin(admin.ModelAdmin):
    list_display = ('content', 'content_type', 'object_id', 'content_object')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('content',)

class PrivateMessageAdmin(admin.ModelAdmin):
    # list_display = ('user',)
    list_display = ('user', 'message')



admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Mesure, MesureAdmin)

admin.site.register(TestID, TestIDAdmin)

admin.site.register(Spare, SpareAdmin)
admin.site.register(Machine, MachineAdmin)
# admin.site.register(Kit, KitAdmin)
admin.site.register(Note, NoteAdmin)


admin.site.register(Message, MessageAdmin)
admin.site.register(PrivateMessage, PrivateMessageAdmin)
