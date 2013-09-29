import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _t
from hashlib import sha1
import settings as userpure_settings

__all__ = ['UserpureActivationMixin']


class UserpureActivationMixin(models.Model):
    """
    Provides activation email and state info in the form of a mixin.

    Make sure this is a parent right after the base ``Model`` class.
    """
    last_generated = models.DateTimeField(verbose_name=_t('last generated time'),
                                          blank=True,
                                          null=True,
                                          help_text=_t('The last date the activation key has been generated.'))
    activation_key = models.CharField(verbose_name=_t('activation key'),
                                      max_length=32,
                                      blank=True)
    is_active = models.BooleanField(verbose_name=_t('active'),
                                    default=False,
                                    help_text=_t('Describes whether the user has been activated yet or not.'))

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        instance = super(UserpureActivationMixin, self).__init__(*args, **kwargs)
        # Validate email field exists.
        self._meta.get_field_by_name('email')
        return instance

    def initialize_user(self):
        self.last_generated = timezone.now()
        self.is_active = False
        self.activation_key = sha1(self.get_username()).hexdigest()

    def send_activation_email(self,
                              request,
                              subject_template='userpure/emails/activation_email_subject.txt',
                              body_template='userpure/emails/activation_email_body.txt',
                              html_template='userpure/emails/activation_email_body.html'):
        """
        Sends a activation email to the user.

        This email is send when the user wants to activate their newly created
        user.
        """
        context = {'user': self,
                   'activation_days': userpure_settings.USERPURE_ACTIVATION_DAYS,
                   'activation_url':  "%s?activation_key=%s" % (request.build_absolute_uri('/accounts/activation'), self.activation_key)}
        subject = render_to_string(subject_template, context)
        body = render_to_string(body_template, context)
        html_body = render_to_string(html_template, context)
        msg = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_body, "text/html")
        msg.send()

    @property
    def activation_key_expired(self):
        return timezone.now() > self.last_generated + datetime.timedelta(days=userpure_settings.USERPURE_ACTIVATION_DAYS)
