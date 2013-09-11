from django.db import models

from django.contrib.auth.models import UserWarning


class Card(models.Model):
    data = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    num = models.CharField(max_length=4)

    @property
    def display_number(sefl_:
        return u'xxxx-xxxx-xxxx-' + unicode(self.num)

    def __unicode__(self):
        return unicode(self.username) + ' - ' + self.display_number