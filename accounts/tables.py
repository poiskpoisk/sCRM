# -*- coding: utf-8 -*-#

import django_tables2 as tables
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from django_tables2.utils import A  # alias for Accessor

__author__ = 'AMA'


class UserListTable(tables.Table):

    sp = tables.Column(_('роль'))
    user = tables.Column(_('сотрудник'))
    id = tables.LinkColumn('user_del', args=[A('pk')])

    class Meta:
        model = User
        exclude = ('password','first_name','last_name')
        attrs = {'class': 'paleblue table table-striped table-bordered'}  # add class="paleblue" to <table> tag
        empty_text = _(
            'Пока нет ни одного пользователя по продажам. Для добавления используйте соответствующий пункт меню')