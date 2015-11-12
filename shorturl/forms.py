# -*- coding:utf-8 -*-
import re
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .models import *
from .utils import *

char_regex = r'^([a-zA-Z0-9]+)$'


class BaseShortURLForm(forms.BaseForm):

    def as_bootstrap(self):
        """
        Returns this form rendered as HTML with bootstrap style
        """
        return self._html_output(
            normal_row='<div%(html_class_attr)s>%(label)s%(field)s<br/>%(errors)s%(help_text)s</div>',
            error_row='<div class="alert alert-success" role="alert">%s</div>',
            row_ender='</div>',
            help_text_html='<p class="help-block">%s</p>',
            errors_on_separate_row=False)


class ShortURLForm(forms.Form, BaseShortURLForm):
    url = forms.URLField(max_length=200,
                         label=_('Url (*)'),
                         widget=forms.TextInput(attrs={'class': 'form-control'}),
                         help_text=_('Enter a long URL to make short'))
    desired_short_url = forms.CharField(max_length=settings.SHORTURL_MAX_LENGTH,
                                        required=False,
                                        widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        help_text=_('Enter a desired short name without domain'))

    def clean(self):
        """
        Clean form
        """
        cleaned_data = super(ShortURLForm, self).clean()
        desired_short_url = cleaned_data.get('desired_short_url')

        if not re.match(char_regex, desired_short_url) and desired_short_url:
            msg = _('The desired short URL must contain only the above characters: a-z, A-Z and 0-9')
            self.add_error('desired_short_url', msg)



class GetOriginalURLForm(forms.Form, BaseShortURLForm):
    short_url = forms.URLField(max_length=settings.SHORTURL_MAX_LENGTH,
                               label=_('Short URL (*)'),
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               help_text=_('Enter the searching short url'))