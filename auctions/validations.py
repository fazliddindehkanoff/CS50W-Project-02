from django.core.exceptions import ValidationError

def check_higher_bid(current_bid, new_bid):
    if new_bid < current_bid:
        raise ValidationError(
            _('%(new_bid)s is not higher than current bid'),
            params={'new_bid': new_bid},
        )