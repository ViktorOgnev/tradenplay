from django import forms
from django.utils.translation import ugettext_lazy as _

from tagging.models import Tag

from .models import Product, ProductReview


class ProductAdminForm(forms.ModelForm):

    """
    ModelForm class to validate product instance
    data before saving from admin interface
    """
    class Meta:
        model = Product

    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError(
                _('Price supplied must be greater than zero.'))
        return self.cleaned_data['price']


class ProductAddToCartForm(forms.Form):

    """
    form class to add items to the shopping cart
    """
    quantity = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'size': '2',
                'value': '1',
                'class': 'quantity'
            }
        ),
        error_messages={
            'invalid': _('Please enter a valid quantity.')},
        min_value=1)

    slug = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        """ override the default so we can set the request """
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        custom validation to check for
        presence of cookies in customer's browser
        """
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Cookies must be enabled."))
        return self.cleaned_data


class ProductReviewForm(forms.ModelForm):

    class Meta:
        model = ProductReview
        exclude = ('user', 'product', 'is_approved', 'date')


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
