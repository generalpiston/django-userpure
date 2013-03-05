from django.conf import settings

USERPURE_ACTIVATION_DAYS = getattr(settings,
                                  'USERPURE_ACTIVATION_DAYS',
                                  3)