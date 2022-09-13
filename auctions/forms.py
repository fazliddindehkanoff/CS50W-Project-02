from django.forms import ModelForm

from .models import Listing


class ListingForm(ModelForm):

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(ListingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Listing
        fields = ("title", "description", "price", "category", "link")

    def save(self, commit=True):
        listing = super(ListingForm, self).save(commit=False)
        listing.owner_id = self.user.pk
        listing.save()
        return listing