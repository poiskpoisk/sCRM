# -*- coding: utf-8 -*-#
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from guardian.decorators import permission_required
from django.db.models.signals import post_delete
from guardian.shortcuts import assign_perm

from crm.forms import SalesPersonForm, SalesPersonUpdateForm
from crm.mixin import SomeUtilsMixin
from crm.models import SalesPerson

__author__ = 'AMA'


class SalesPersonUpdateView(UpdateView, SomeUtilsMixin):
    model = SalesPerson
    form_class = SalesPersonUpdateForm
    template_name = 'crm/salesperson.html'

    def get_success_url(self):
        return reverse('salespersonpage', kwargs={'pk': self.kwargs['pk']})

    @method_decorator(login_required())
    @method_decorator(permission_required('crm.read_salesperson', accept_global_perms=True))
    def get(self, request, *args, **kwargs):
        self.set_lang(request)
        # if the forma updated we need to clear message query
        self.clearMsg(request)
        return super().get(self, request, *args, **kwargs)

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):

        if not self.checkPermissions(request, SalesPerson, 'crm.change_salesperson'):
            return HttpResponseRedirect(reverse('login'))

        # .save() update record if instance argument is present, but another way .save create new record
        a = SalesPerson.objects.get(pk=self.kwargs['pk'])
        form = SalesPersonForm(request.POST, instance=a)
        # Patch for solve problem with hidden field
        form.data['role']=form.initial['role']
        form.data['user'] = form.initial['user']
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('salespersons'))
        else:
            messages.error(request, _('Что-то пошло не так'))
            return super().post(self, request, *args, **kwargs)


class SalesPersonDeleteView(DeleteView, SomeUtilsMixin):
    model = SalesPerson
    template_name = 'crm/salesperson_del.html'

    def get_success_url(self):
        return reverse('salespersons')

    @method_decorator(login_required())
    @method_decorator(permission_required('crm.delete_salesperson', accept_global_perms=True))
    def get(self, request, *args, **kwargs):
        self.set_lang(request)
        return super().get(self, request, *args, **kwargs)

# ---------------- Set signal for delete User instance together with SalesPerson --------------------
def delete_related_user(sender, **kwargs):
    deleted_profile = kwargs['instance']
    deleted_profile.user.delete()

post_delete.connect(delete_related_user, sender=SalesPerson)


class SalesPersonCreateView(CreateView, SomeUtilsMixin):
    model = SalesPerson
    template_name = 'crm/salesperson_new.html'
    form_class = SalesPersonForm

    def get_success_url(self):
        return reverse('salespersons')

    @method_decorator(login_required())
    @method_decorator(permission_required('crm.add_salesperson', accept_global_perms=True))
    def get(self, request, *args, **kwargs):
        self.set_lang(request)
        # if the forma updated we need to clear message query
        self.clearMsg(request)
        return super().get(self, request, *args, **kwargs)

    @method_decorator(login_required())
    @method_decorator(permission_required('crm.add_salesperson', accept_global_perms=True))
    def post(self, request, *args, **kwargs):

        form = SalesPersonForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['user'])

            if form.cleaned_data['role'] == 'M':
                try:
                    group = Group.objects.get(name='manager')
                except:
                    messages.error(request, _('Немогу получить доступ к группе прав МЕНЕДЖЕР'))
                    return super().post(self, request, *args, **kwargs)
            elif form.cleaned_data['role'] == 'B':
                try:
                    group = Group.objects.get(name='boss')
                except:
                    messages.error(request, _('Немогу получить доступ к группе прав РУКОВОДИТЕЛЬ'))
                    return super().post(self, request, *args, **kwargs)
            elif form.cleaned_data['role'] == 'A':
                try:
                    group = Group.objects.get(name='admin')
                except:
                    messages.error(request, _('Немогу получить доступ к группе прав АДМИНИСТРАТОР'))
                    return super().post(self, request, *args, **kwargs)

            # set group permission for user which linked with salesperson
            user.groups.add(group)
            record = form.save()
            assign_perm('crm.change_salesperson', user, record)
            return HttpResponseRedirect(reverse('salespersons'))
        else:
            messages.error(request, _('Что-то пошло не так'))
            return super().post(self, request, *args, **kwargs)
