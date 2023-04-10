# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

from db.base.models import DateTimeModelMixin


class Thread(DateTimeModelMixin):
    participants = models.ManyToManyField(
        'users.User',
        verbose_name=_('participants'),
        related_name='threads',
    )
    creator = models.OneToOneField(
        'users.User',
        verbose_name=_('creator'),
        related_name='created_thread',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Thread')
        verbose_name_plural = _('Threads')


class Message(DateTimeModelMixin):
    thread = models.ForeignKey(
        to=Thread,
        verbose_name=_('thread'),
        related_name='messages',
        on_delete=models.CASCADE,
    )
    sender = models.ForeignKey(
        'users.User',
        verbose_name=_('sender'),
        related_name='sent_messages',
        on_delete=models.CASCADE,
    )
    text = models.TextField(_('text'))
    is_read = models.BooleanField(_('is read'), default=False)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
