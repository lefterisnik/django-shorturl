# -*- coding: utf-8 -*-
import urlparse
from django.conf import settings
from django.db.models import F, Q
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.base import View, RedirectView, ContextMixin, TemplateView

from social.backends.google import GooglePlusAuth

from .models import *
from .utils import *
from .forms import *


## Some base views

class ShortURLBaseMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(ShortURLBaseMixin, self).get_context_data(**kwargs)
        context.update(
            plus_id=getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
            plus_scope=' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        )
        return context


class ShortURLBaseView(View):

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super(ShortURLBaseView, self).dispatch(request, *args, **kwargs)


## The actual views

class IndexPageView(TemplateView, ShortURLBaseView, ShortURLBaseMixin, FormMixin):
    form_class = ShortURLForm
    template_name = 'shorturl/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data()
        context.update(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = self.get_context_data()
        context.update(form=form)

        if form.is_valid():
            url = form.cleaned_data['url']
            desired_short_url = form.cleaned_data['desired_short_url']

            if desired_short_url:
                if len(create_full_shorturl(request, desired_short_url)) > settings.SHORTURL_MAX_LENGTH:
                    msg = _('The desired short URL %s is more than 23 characters. Please give a shorter short URL.'
                            % create_full_shorturl(request, desired_short_url))
                    form.add_error('desired_short_url', msg)
                else:
                    hash_id = saturate(desired_short_url)

                    # Create the object
                    try:
                        shorturl_obj = ShortURL.objects.get(Q(hash_id=hash_id) | Q(id=hash_id))
                        msg = _('The desired short URL is already taken. Please give a different.')
                        form.add_error('desired_short_url', msg)
                    except ShortURL.DoesNotExist:
                        shorturl_obj = ShortURL.objects.create(hash_id=hash_id, user=request.user, orig_url=url)
                        context.update(obj=shorturl_obj)

            else:
                shorturl_obj = ShortURL.objects.create(user=request.user, orig_url=url)
                if len(create_full_shorturl(request, desired_short_url)) > settings.SHORTURL_MAX_LENGTH:
                    msg = _('Short URL service reaches 23 maximum characters shorting')
                    form.add_error('url', msg)
                    shorturl_obj.delete()
                else:
                    context.update(obj=shorturl_obj)

        return render(request, self.template_name, context)


class RetrieveOriginalPageView(TemplateView, ShortURLBaseView, ShortURLBaseMixin, FormMixin):
    form_class = GetOriginalURLForm
    template_name = 'shorturl/original.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data()
        context.update(form=form, msg=False)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = dict(form=form, msg=True)

        if form.is_valid():
            short_url = form.cleaned_data['short_url']

            if short_url:
                url = urlparse.urlparse(short_url)
                if not check_netloc(request, url.netloc):
                    msg = _('The request short url has different netloc.')
                    form.add_error('short_url', msg)
                else:
                    short_url = short_url.split('/')[-1]
                    id = saturate(short_url)

                    # Get the object
                    try:
                        shorturl_obj = ShortURL.objects.get((Q(hash_id=id) | Q(id=id)) & Q(user=request.user))
                        context.update(obj=shorturl_obj)
                    except ShortURL.DoesNotExist:
                        pass

        return render(request, self.template_name, context)


class RetrieveURLsPageView(ListView, ShortURLBaseView, ShortURLBaseMixin):
    template_name = 'shorturl/urls.html'
    model = ShortURL

    def get_queryset(self):
        queryset = super(RetrieveURLsPageView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class RetrieveURLDetailsPageView(DetailView, ShortURLBaseView, ShortURLBaseMixin):
    template_name = 'shorturl/detail.html'
    model = ShortURL


class OriginalURLRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        id = saturate(kwargs['short_url'])
        shorturl_obj = get_object_or_404(ShortURL, Q(hash_id=id) | Q(id=id))
        shorturl_obj.shorturlinfo.views = F('views')+1
        shorturl_obj.shorturlinfo.save()

        return shorturl_obj.orig_url





