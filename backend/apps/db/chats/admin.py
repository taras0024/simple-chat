# -*- coding: utf-8 -*-
from django.contrib import admin

from db.chats.models import Message, Thread


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('id',)
    inlines = (MessageInline,)
