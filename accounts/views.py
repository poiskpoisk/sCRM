from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django_tables2 import RequestConfig
from django.contrib.auth import views as auth_views, logout
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.db.models import F
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site

from registration.backends.default.views import RegistrationView
from registration.models import RegistrationProfile
from registration.users import UserModel
from registration import signals

from accounts.forms import MyRegistrationFormUniqueEmail, MyAuthenticationForm
from accounts.tables import UserListTable
from crm.mixin import SomeUtilsMixin, add_lang
from crm.models import SalesPerson
from guardian.decorators import permission_required
from globalcustomer.models import Client
from simpleCRM.settings import DEBUG


class MyTemplateView(TemplateView, SomeUtilsMixin):
    template_name = 'accounts/activation_complete.html'

    def get(self, request, *args, **kwargs):
        # Set language as is tenant language
        rec = Client.objects.get(pk=request.tenant.pk)
        translation.deactivate_all()
        translation.activate(rec.lang)
        # if the form updated we need to clear message query
        self.clearMsg(request)
        return super().get(self, request, *args, **kwargs)


class MyRegistrationView(RegistrationView, SomeUtilsMixin):
    form_class = MyRegistrationFormUniqueEmail
    template_name = 'accounts/registration_form.html'

    def register(self, form):

        domen = get_current_site(self.request).name

        if domen.count('.') == 1:
            schema_name = self.request.tenant.schema_name
            if DEBUG:
                domen += ':8000'
            site_full = schema_name + '.' + domen
            site = get_current_site(self.request)
            site.domain=site_full
            site.name=site_full
        else:
            site = get_current_site(self.request)

        if hasattr(form, 'save'):
            new_user_instance = form.save()
        else:
            new_user_instance = (UserModel().objects
                                 .create_user(**form.cleaned_data))

        new_user = RegistrationProfile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

    def get_success_url(self, user=None):
        return reverse('registration_complete')

    def get(self, request, *args, **kwargs):
        # Set language as is tenant language
        rec = Client.objects.get(pk=request.tenant.pk)
        translation.deactivate_all()
        translation.activate(rec.lang)
        # if the form updated we need to clear message query
        self.clearMsg(request)
        return super().get(self, request, *args, **kwargs)


@login_required
@permission_required('auth.add_user', accept_global_perms=True)
@add_lang
def tableUser(request):
    # add somme data from related tables
    queryset = User.objects.annotate(sp=F('salesperson__role'))
    queryset = queryset.annotate(user=F('salesperson__first_name'))

    for q in queryset:
        # convert one symbol name to people friendly value
        for choice in SalesPerson.ROLE_CHOICES:
            if q.sp == choice[0]:
                q.sp = choice[1]

    table = UserListTable(queryset)
    RequestConfig(request).configure(table)
    filter = 'NONFILTER'
    return render(request, 'crm/common_table_list.html', {'table': table, 'filter': filter})


class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/user_del.html'

    def get_success_url(self):
        return reverse('userlist')

    @method_decorator(login_required())
    @method_decorator(permission_required('auth.delete_user', accept_global_perms=True))
    def get(self, request, *args, **kwargs):
        try:
            translation.activate(request.user.salesperson.lang)
        except:
            pass
        return super().get(self, request, *args, **kwargs)


class MyLogin(TemplateView, SomeUtilsMixin):
    template_name = 'accounts/login.html'

    def post(self, request, *args, **kwargs):

        resp = auth_views.login(request, template_name='accounts/login.html', authentication_form=MyAuthenticationForm)
        if not request.user.groups.filter(name='admin').exists() and str(request.user) != 'AnonymousUser':
            try:
                sp = SalesPerson.objects.get(user=request.user)
            except:
                messages.error(request, _("Учетная запись пользователя должна быть связанна с записью персонала"
                                          " или иметь статус АДМИНИСТРАТОРА."))
                logout(request)
                return HttpResponseRedirect(reverse('login'))
        return resp

    def get(self, request, *args, **kwargs):
        # Set language as is tenant language
        rec = Client.objects.get(pk=request.tenant.pk)
        translation.deactivate_all()
        translation.activate(rec.lang)
        # if the form updated we need to clear message query
        self.clearMsg(request)
        resp = auth_views.login(request, template_name='accounts/login.html', authentication_form=MyAuthenticationForm)
        return resp
