from django.db import models

from django.contrib.auth.models import User
from checkout.models import BaseOrderInfo

from django.utils.translation import ugettext_lazy as _


class UserProfile(BaseOrderInfo):
    
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return ''.join([_("User profle for"), self.user.username])
