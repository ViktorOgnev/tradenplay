from django import forms
from django.utils.translation import ugettext_lazy as _

from search.models import SearchTerm


class SearchForm(forms.ModelForm):

    class Meta:
        model = SearchTerm

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        default_text = _("Search")
        self.fields['q'].widget.attrs['value'] = default_text
        self.fields['q'].widget.attrs['onfocus'] = ''.join(
            ["if (this.value == '",
             str(default_text),
             "') this.value = '';"
             ]
        )

    include = ('q', )
