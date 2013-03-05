from django.db import models
from django.contrib.auth import get_user_model

__all__ = ['UserpureActivationManager']


class UserpureActivationManager(models.Manager):
    def create_user(self, *args, **kwargs):
        """
        Creates a new user.

        Takes a variable amount of arguments with variable keywords.
        Creates user and populates an :class:UserpureActivationMixin instance.

        :return: New user.
        """
        new_user = super(UserpureActivationManager, self).objects.create_user(*args, **kwargs)
        new_user.initialize()
        new_user.save()
 
        return new_user

    def activate(self, activation_key):
        """
        Activate a user by activation key.

        :param activation_key: SHA1 key to send to a user.

        :return: User that has been confirmed.
        """
        try:
            user = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return None
        if not user.activation_key_expired:
            user.is_active = True
            user.save()
            return user
        return None

    def expired(self):
        """
        :return: A list containing the expired users.
        """
        return filter(lambda user: not user.activation_key_expired, get_user_model().objects.filter(is_active=False))
