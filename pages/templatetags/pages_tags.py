from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from ..models import SensoryModule

register = template.Library()


@register.filter
def get_display_value(choices, request_key):
    for key, value in choices:
        if key == request_key:
            return value
    return ""


# need to be there for senses to be translatable
pgettext_lazy("sensitivity description", "sound")
pgettext_lazy("sensitivity description", "light")
pgettext_lazy("sensitivity description", "smell")
pgettext_lazy("sensitivity description", "temperature")


@register.filter
def sensitivity_desc(value, sense):
    if value == SensoryModule.SENS_V_LOW:
        return _("I am much less sensitive to %(sense)s than most people.") \
                % {'sense': sense}
    if value == SensoryModule.SENS_LOW:
        return _("I am less sensitive to %(sense)s than most people.") \
                % {'sense': sense}
    if value == SensoryModule.SENS_MED:
        return _("My sensitivity to %(sense)s is average.") \
                % {'sense': sense}
    if value == SensoryModule.SENS_HIGH:
        return _("I am more sensitive to %(sense)s than most people.") \
                % {'sense': sense}
    if value == SensoryModule.SENS_V_HIGH:
        return _("I am much more sensitive to %(sense)s than most people.") \
                % {'sense': sense}
    return ""


@register.filter
def sensitivity_img(value, sense):
    if value == SensoryModule.SENS_V_LOW:
        return "img/very_low_sensitive_{}.svg".format(sense)
    if value == SensoryModule.SENS_LOW:
        return "img/low_sensitive_{}.svg".format(sense)
    if value == SensoryModule.SENS_MED:
        return "img/average_sensitive_{}.svg".format(sense)
    if value == SensoryModule.SENS_HIGH:
        return "img/high_sensitive_{}.svg".format(sense)
    if value == SensoryModule.SENS_V_HIGH:
        return "img/very_high_sensitive_{}.svg".format(sense)
    return ""
